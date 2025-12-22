from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABSE_URL = "postgresql://postgres:Joshua10!@localhost:5432/jiralite"

engine = create_engine(DATABSE_URL)

SesionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

base = declarative_base()