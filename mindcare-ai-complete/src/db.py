import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DB_URL = os.getenv("DB_URL", "sqlite:///mindcare.db")

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    ts = Column(DateTime, default=datetime.utcnow)
    role = Column(String(10))          # 'user' or 'ai'
    text = Column(Text)
    emotion = Column(String(32), nullable=True)
    confidence = Column(Float, nullable=True)

def init_db():
    Base.metadata.create_all(engine)
