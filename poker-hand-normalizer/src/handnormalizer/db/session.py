from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parents[3]
DATABASE_URL = f"sqlite:///{BASE_DIR / 'handnormalizer.db'}"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False, future=True)

