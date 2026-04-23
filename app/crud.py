from sqlalchemy.orm import Session
from . import models, schemas, auth_utils

# --- LOGIQUE UTILISATEURS ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Hachage du mot de passe avant enregistrement
    hashed_pwd = auth_utils.get_password_hash(user.password)
    
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_pwd,
        full_name=user.full_name
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- LOGIQUE TRAJETS (Gardée de la version précédente) ---

def get_trips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trip).offset(skip).limit(limit).all()

def create_trip(db: Session, trip: schemas.TripCreate, user_id: int):
    # On lie maintenant le trajet à l'ID de l'utilisateur connecté
    db_trip = models.Trip(**trip.model_dump(), owner_id=user_id)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip