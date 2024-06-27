import os
import subprocess
import logging
from minio import Minio
from app import settings

logger = logging.getLogger('app')

def restore(backup_name: str, mongo_uri: str):

    required_vars = ["MINIO_ACCESS_KEY", "MINIO_SECRET_KEY", "MINIO_ADDR"]

    missing_vars = [var for var in required_vars if not getattr(settings, var, None)]
    if missing_vars:
        raise Exception(f"Missing required environment variables: {', '.join(missing_vars)}")

    minio_client = Minio(
        settings.MINIO_ADDR,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False
    )

    backup_file = f"{backup_name}.gz"
    try:
        logger.info(f"Starting restore from MinIO to Railway using {backup_file}")

        # Download the backup from MinIO
        minio_client.fget_object(
            "backups",
            backup_file,
            backup_file,
        )
        logger.info(f"Backup {backup_file} downloaded from MinIO")

        # Run mongorestore command
        restore_command = [
            "mongorestore",
            f"--uri={mongo_uri}",
            "--gzip",
            "--drop",
            f"--archive={backup_file}"
        ]
        subprocess.run(restore_command, check=True)
        logger.info(f"Database restore from {backup_file} complete")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error during restore: {e}")
        raise
    finally:
        # Clean up the backup file
        if os.path.exists(backup_file):
            os.remove(backup_file)
            logger.info(f"Cleaned up backup file {backup_file}")
