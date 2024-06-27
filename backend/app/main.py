from fastapi import FastAPI, Depends, HTTPException
from app.dependencies import get_api_key
from app.tasks.migrate import migrate
from app.tasks.backup import backup
from app.tasks.restore import restore

from sqlalchemy.orm import Session
from typing import List
from app.db.schemas import OperationStatus, MigrateRequest, BackupRequest, RestoreRequest
from app.db.utils import create_operation, update_operation_status, get_operations, get_db

app = FastAPI()

@app.get("/health")
def health():
    return {"message": "I am healthy!"}

@app.post("/migrate/{db_name}")
async def migrate_db(
    db_name: str,
    request: MigrateRequest,  # Use Pydantic model for request body
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    operation = create_operation(db, "migrate")
    try:
        migrate(db_name, request.atlas_uri, request.mongo_uri)
        update_operation_status(db, operation.id, "Complete")
        return {"message": f"Migration for database {db_name} complete"}
    except Exception as e:
        update_operation_status(db, operation.id, "Failed", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/backup")
async def backup_db(
    request: BackupRequest,  # Use Pydantic model for request body
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    operation = create_operation(db, "backup")
    try:
        backup_name = backup(request.mongo_uri)
        update_operation_status(db, operation.id, "Complete")
        return {"message": f"Backup {backup_name} complete"}
    except Exception as e:
        update_operation_status(db, operation.id, "Failed", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/restore/{backup_name}")
async def restore_db(
    backup_name: str,
    request: RestoreRequest,
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    operation = create_operation(db, "restore")
    try:
        restore(backup_name, request.mongo_uri)
        update_operation_status(db, operation.id, "Complete")
        return {"message": f"Restore for backup {backup_name} complete"}
    except Exception as e:
        update_operation_status(db, operation.id, "Failed", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/operations", response_model=List[OperationStatus])
async def get_operations_endpoint(api_key: str = Depends(get_api_key), db: Session = Depends(get_db)):
    return get_operations(db)
