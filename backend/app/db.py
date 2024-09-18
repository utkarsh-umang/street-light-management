import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_USER = os.getenv('STREET_SMART_DATABASE_USER')
POSTGRES_PASSWORD = os.getenv('STREET_SMART_DATABASE_PASSWORD')
POSTGRES_DB = os.getenv('STREET_SMART_DATABASE_NAME')
POSTGRES_HOST = os.getenv('STREET_SMART_DATABASE_HOST')

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DECLARATIVE_BASE = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
