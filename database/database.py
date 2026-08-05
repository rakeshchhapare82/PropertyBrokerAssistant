import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL not found. Please add it to your .env file."
    )

# SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    future=True,
)

# Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


@contextmanager
def get_db():
    """
    Database session context manager.

    Usage:
        with get_db() as db:
            db.execute(...)
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def execute_query(query: str, params: dict | None = None):
    """
    Execute INSERT/UPDATE/DELETE queries.
    """
    with get_db() as db:
        db.execute(text(query), params or {})


def fetch_one(query: str, params: dict | None = None):
    """
    Fetch one record.
    """
    with get_db() as db:
        result = db.execute(text(query), params or {})
        row = result.mappings().first()
        return dict(row) if row else None


def fetch_all(query: str, params: dict | None = None):
    """
    Fetch multiple records.
    """
    with get_db() as db:
        result = db.execute(text(query), params or {})
        return [dict(row) for row in result.mappings().all()]


def test_connection():
    """
    Returns True if the database connection is successful.
    """
    try:
        with get_db() as db:
            db.execute(text("SELECT 1"))
        return True
    except Exception as ex:
        print(ex)
        return False