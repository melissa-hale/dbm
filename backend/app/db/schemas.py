from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OperationStatusBase(BaseModel):
    operation_type: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration: Optional[float] = None
    details: Optional[str] = None

class OperationStatusCreate(OperationStatusBase):
    pass

class OperationStatus(OperationStatusBase):
    id: int

    class Config:
        orm_mode = True

class MigrateRequest(BaseModel):
    atlas_uri: str
    mongo_uri: str

class BackupRequest(BaseModel):
    mongo_uri: str

class RestoreRequest(BaseModel):
    mongo_uri: str
    minio_addr: Optional[str] = None