import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tracenest import logger

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@postgres:5432/loktathya")

logger.info("Initializing SQLAlchemy database engine", database_host="postgres:5432", database_name="loktathya", pool_pre_ping=True)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("Database SessionLocal factory created")

def get_db():
    logger.debug("Opening new database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.debug("Closing database session")
        db.close()
