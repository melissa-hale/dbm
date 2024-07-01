import asyncio
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from sqlalchemy.orm import Session
from app.db.utils import create_operation, update_operation_status, get_db

def run_command(command, logger):
    logger.info(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logger.error(f"Command failed: {' '.join(command)}\nstdout: {result.stdout.decode()}\nstderr: {result.stderr.decode()}")
        raise subprocess.CalledProcessError(result.returncode, command)
    logger.info(f"Command succeeded: {' '.join(command)}\nstdout: {result.stdout.decode()}\nstderr: {result.stderr.decode()}")
    return result.stdout, result.stderr

async def dump_collection(executor, collection_name, dump_dir, db_name, atlas_uri, logger):
    dump_file = os.path.join(dump_dir, f"{collection_name}.gz")
    dump_command = [
        "mongodump",
        f"--uri={atlas_uri}",
        f"--db={db_name}",
        f"--collection={collection_name}",
        "--gzip",
        f"--archive={dump_file}"
    ]
    await asyncio.get_event_loop().run_in_executor(executor, run_command, dump_command, logger)
    logger.info(f"Dumped collection {collection_name} to {dump_file}")
    return dump_file

async def restore_collection(executor, dump_file, db_name, mongo_uri, logger):
    restore_command = [
        "mongorestore",
        f"--uri={mongo_uri}",
        "--gzip",
        f"--archive={dump_file}",
        f"--nsInclude={db_name}.*"
    ]
    await asyncio.get_event_loop().run_in_executor(executor, run_command, restore_command, logger)
    logger.info(f"Restored collection from {dump_file}")

async def delete_dump_file(dump_file, logger):
    if os.path.exists(dump_file):
        os.remove(dump_file)
        logger.info(f"Cleaned up dump file {dump_file}")

async def drop_target_database(db_name: str, mongo_uri: str, logger):
    logger.info(f"Dropping target database {db_name} on {mongo_uri}")
    client = MongoClient(mongo_uri)
    client.drop_database(db_name)
    logger.info(f"Dropped target database {db_name}")

async def migrate_collection(executor, collection_name, dump_dir, db_name, atlas_uri, mongo_uri, db: Session, logger):
    operation = create_operation(db, "migrate", details=collection_name)
    try:
        logger.info(f"Starting migration for collection {collection_name}")
        dump_file = await dump_collection(executor, collection_name, dump_dir, db_name, atlas_uri, logger)
        await restore_collection(executor, dump_file, db_name, mongo_uri, logger)
        await delete_dump_file(dump_file, logger)
        update_operation_status(db, operation.id, "Complete")
        logger.info(f"Migration complete for collection {collection_name}")
    except Exception as e:
        logger.error(f"Error during migrating collection {collection_name}: {e}")
        update_operation_status(db, operation.id, "Failed", str(e))

async def migrate(db_name: str, atlas_uri: str, mongo_uri: str, operation_id: int, logger):
    logger.info(f"Starting migration for database {db_name} from {atlas_uri} to {mongo_uri}")
    client = MongoClient(atlas_uri)
    db_instance = client[db_name]
    collections = db_instance.list_collection_names()
    logger.info(f"Found collections: {collections}")

    dump_dir = '/dumps'
    os.makedirs(dump_dir, exist_ok=True)
    logger.info(f"Created dump directory {dump_dir}")

    await drop_target_database(db_name, mongo_uri, logger)

    db: Session = next(get_db())
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = [migrate_collection(executor, col, dump_dir, db_name, atlas_uri, mongo_uri, db, logger) for col in collections]
        await asyncio.gather(*tasks)

    update_operation_status(db, operation_id, "Complete")
    logger.info(f"Migration for database {db_name} complete")
