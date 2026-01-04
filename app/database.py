from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/workemon_db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class RequestResponse(Base):
    __tablename__ = 'request_responses'

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)  # email, telegram, api
    content = Column(Text)
    prompt = Column(Text)
    llm_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)