import logging
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from app.dependencies import get_api_key
from app.tasks.migrate import migrate
from app.tasks.backup import backup
from app.tasks.restore import restore

from sqlalchemy.orm import Session
from typing import List
from app.db.schemas import OperationStatus, MigrateRequest, BackupRequest, RestoreRequest
from app.db.utils import create_operation, update_operation_status, get_operations, get_db

logger = logging.getLogger('app')
app = FastAPI()

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/health")
def health():
    logger.info("Health endpoint called")
    return {"message": "I am healthy!"}

@app.post("/migrate/{db_name}")
async def migrate_db(
    db_name: str,
    request: MigrateRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    logger.info(f"Migrate endpoint called for db: {db_name}")
    operation = create_operation(db, "migrate")
    try:
        background_tasks.add_task(migrate, db_name, request.atlas_uri, request.mongo_uri, operation.id, logger)
        return {"message": f"Migration for database {db_name} has been started in the background."}
    except Exception as e:
        update_operation_status(db, operation.id, "Failed", str(e))
        logger.error(f"Error initiating migration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/backup")
async def backup_db(
    request: BackupRequest,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    logger.info("Backup endpoint called")
    operation = create_operation(db, "backup")
    try:
        backup_name = backup(request.mongo_uri)
        update_operation_status(db, operation.id, "Complete")
        return {"message": f"Backup {backup_name} complete"}
    except Exception as e:
        update_operation_status(db, operation.id, "Failed", str(e))
        logger.error(f"Error during backup: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/restore/{backup_name}")
async def restore_db(
    backup_name: str,
    request: RestoreRequest,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    logger.info(f"Restore endpoint called for backup: {backup_name}")
    operation = create_operation(db, "restore")
    try:
        restore(backup_name, request.mongo_uri)
        update_operation_status(db, operation.id, "Complete")
        return {"message": f"Restore for backup {backup_name} complete"}
    except Exception as e:
        update_operation_status(db, operation.id, "Failed", str(e))
        logger.error(f"Error during restore: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/operations", response_model=List[OperationStatus])
async def get_operations_endpoint(api_key: str = Depends(get_api_key), db: Session = Depends(get_db)):
    logger.info("Operations endpoint called")
    return get_operations(db)
