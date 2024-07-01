from sqlalchemy.orm import Session
from .models import OperationStatus, SessionLocal
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_operation(db: Session, operation_type: str, details: str = None) -> OperationStatus:
    operation = OperationStatus(operation_type=operation_type, status="Running", details=details, started_at=datetime.utcnow())
    db.add(operation)
    db.commit()
    db.refresh(operation)
    return operation

def update_operation_status(db: Session, operation_id: int, status: str, message: str = None):
    operation = db.query(OperationStatus).filter(OperationStatus.id == operation_id).first()
    operation.status = status
    operation.completed_at = datetime.utcnow()
    if message:
        operation.message = message
    db.commit()
    db.refresh(operation)
    return operation

def get_operations(db: Session):
    return db.query(OperationStatus).all()
