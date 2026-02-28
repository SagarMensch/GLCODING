from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variable for DB URL (Rule 5: Engineer for Reversibility)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres.ysrsniznvwionmzcrzeh:Messiejfnvjrbgbndfg@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres"
)

# Create engine for Postgres
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_size=10, 
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
