import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. On récupère l'URL depuis l'environnement, sinon SQLite par défaut
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_temp.db")

# 2. Configuration du moteur (adaptée selon la DB)
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # check_same_thread est nécessaire uniquement pour SQLite
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()