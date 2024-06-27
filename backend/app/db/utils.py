from sqlalchemy.orm import Session
from .models import OperationStatus, SessionLocal
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_operation(db: Session, operation_type: str):
    db_operation = OperationStatus(operation_type=operation_type, status="Running")
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation

def update_operation_status(db: Session, operation_id: int, status: str, details: str = None):
    db_operation = db.query(OperationStatus).filter(OperationStatus.id == operation_id).first()
    db_operation.status = status
    db_operation.completed_at = datetime.utcnow()
    db_operation.duration = (db_operation.completed_at - db_operation.started_at).total_seconds()
    db_operation.details = details
    db.commit()
    db.refresh(db_operation)
    return db_operation

def get_operations(db: Session):
    return db.query(OperationStatus).all()
