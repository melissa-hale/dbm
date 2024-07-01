import os
import datetime
import subprocess
import logging
from minio import Minio
from app import settings

logger = logging.getLogger('app')

def backup(mongo_uri: str):
    minio_client = Minio(
        settings.MINIO_ADDR,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False
    )

    # Generate backup file name based on current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"backup_{timestamp}.gz"
    
    try:
        logger.info(f"Starting backup from Mongo to MinIO as {backup_file}")

        # Run mongodump command
        dump_command = [
            "mongodump",
            f"--uri={mongo_uri}",
            "--gzip",
            f"--archive={backup_file}"
        ]
        subprocess.run(dump_command, check=True)
        logger.info("Database dump complete")

        # Upload the backup to MinIO
        minio_client.fput_object(
            settings.MINIO_BUCKET,
            backup_file,
            backup_file,
        )
        logger.info(f"Backup {backup_file} uploaded to MinIO")

        return backup_file

    except subprocess.CalledProcessError as e:
        logger.error(f"Error during backup: {e}")
        raise
    finally:
        # Clean up the backup file
        if os.path.exists(backup_file):
            os.remove(backup_file)
            logger.info(f"Cleaned up backup file {backup_file}")
