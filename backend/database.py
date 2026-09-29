"""SQLAlchemy + SQLite setup for the Syngenta MVP."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

_DATA_DIR = Path(__file__).parent / "data"
_DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{_DATA_DIR / 'syngenta.db'}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create tables and add newly introduced columns to old SQLite files."""
    from models import Advisory, Campaign, Farmer, Prediction  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_columns()


def _ensure_sqlite_columns():
    """Tiny migration helper suitable for this single-file SQLite MVP."""
    additions = {
        "farmers": {
            "tehsil_block": "VARCHAR",
            "village": "VARCHAR",
            "connectivity": "VARCHAR",
            "literacy_level": "VARCHAR",
            "high_value_farmer": "BOOLEAN DEFAULT 0",
        },
        "campaigns": {
            "sms_message": "TEXT",
            "whatsapp_message": "TEXT",
            "voice_script": "TEXT",
            "rag_summary": "TEXT",
            "audio_file": "VARCHAR",
        },
        "predictions": {
            "rag_summary": "TEXT",
        },
        "advisories": {
            "audio_file": "VARCHAR",
        },
    }
    with engine.begin() as conn:
        for table, columns in additions.items():
            existing = {row[1] for row in conn.exec_driver_sql(f"PRAGMA table_info({table})")}
            for name, ddl in columns.items():
                if name not in existing:
                    conn.exec_driver_sql(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}")
