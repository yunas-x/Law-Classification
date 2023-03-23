from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection string
SQLALCHEMY_DATABASE_URL = "sqlite:///./logs.db"

Engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Default session maker 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

# A base class for tables
Base = declarative_base()