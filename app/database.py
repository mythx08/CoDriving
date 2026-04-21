import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# On vérifie si on est en train de tester
IS_TESTING = os.getenv("TESTING", "false").lower() == "true"

if IS_TESTING:
    # Base de données temporaire en mémoire pour les tests GitHub
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Ta config PostgreSQL habituelle
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/codrive")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()