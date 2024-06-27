import subprocess
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from app import settings
from pymongo import MongoClient

logger = logging.getLogger('app')

def dump_and_restore_collection(collection_name, dump_dir, db_name, atlas_uri, mongo_uri):
    dump_file = os.path.join(dump_dir, f"{collection_name}.gz")
    try:
        # Dump the collection
        dump_command = [
            "mongodump",
            f"--uri={atlas_uri}",
            f"--db={db_name}",
            f"--collection={collection_name}",
            "--gzip",
            f"--archive={dump_file}"
        ]
        subprocess.run(dump_command, check=True)
        logger.info(f"Dumped collection {collection_name} to {dump_file}")

        # Restore the collection
        restore_command = [
            "mongorestore",
            f"--uri={mongo_uri}",
            "--gzip",
            f"--archive={dump_file}",
            f"--nsInclude={db_name}.{collection_name}"
        ]
        subprocess.run(restore_command, check=True)
        logger.info(f"Restored collection {collection_name} from {dump_file}")

        # Clean up the dump file
        if os.path.exists(dump_file):
            os.remove(dump_file)
            logger.info(f"Cleaned up dump file {dump_file}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error during dumping/restoring collection {collection_name}: {e}")
        raise

def drop_target_database(db_name: str, mongo_uri: str):
    try:
        client = MongoClient(mongo_uri)
        client.drop_database(db_name)
        logger.info("Dropped target database before restore")
    except Exception as e:
        logger.error(f"Error dropping target database: {e}")
        raise

def migrate(db_name: str, atlas_uri: str, mongo_uri: str):
    client = MongoClient(atlas_uri)
    db = client[db_name]
    collections = db.list_collection_names()

    dump_dir = '/dumps'

    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    try:
        logger.info(f"Starting migration from Atlas to Railway for database {db_name}")

        # Drop target database before restore
        drop_target_database(db_name, mongo_uri)

        with ThreadPoolExecutor(max_workers=4) as executor:
            # Sequentially dump, restore, and clean up collections
            tasks = [executor.submit(dump_and_restore_collection, col, dump_dir, db_name, atlas_uri, mongo_uri) for col in collections]
            for task in tasks:
                task.result()

        logger.info(f"Migration for database {db_name} complete")

    except Exception as e:
        logger.error(f"Error during migration for database {db_name}: {e}")
        raise
