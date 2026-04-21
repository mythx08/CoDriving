import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. On récupère l'URL de la base depuis les variables d'environnement (.env)
# Si elle n'est pas définie, on utilise une valeur par défaut (utile pour le dev local)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://user:password@db:5432/codrive"
)

# 2. L'engine (le moteur) gère la connexion physique à PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. SessionLocal permet de créer des sessions de travail avec la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base est la classe dont tous nos modèles (Ride, User, etc.) vont hériter
# Utilisation de la nouvelle méthode SQLAlchemy 2.0
Base = declarative_base()

# 5. Dépendance (Dependency Injection) pour FastAPI
# Cette fonction ouvre une session DB pour chaque requête et la ferme à la fin
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()