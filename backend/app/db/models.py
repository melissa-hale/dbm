import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


os.makedirs('/data/db', exist_ok=True)
DATABASE_URL = "sqlite://///data/db/ops.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class OperationStatus(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    operation_type = Column(String, index=True)
    status = Column(String, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)
    details = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)
