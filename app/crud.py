import logging
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, time

# Récupération du logger configuré dans main.py
logger = logging.getLogger("codrive")

def get_user_daily_rides_count(db: Session, user_id: str):
    today_min = datetime.combine(datetime.today(), time.min)
    today_max = datetime.combine(datetime.today(), time.max)
    
    return db.query(models.Ride).filter(
        models.Ride.user_id == user_id,
        models.Ride.created_at >= today_min,
        models.Ride.created_at <= today_max
    ).count()

def create_ride(db: Session, ride: schemas.RideCreate, user_id: str):
    # Vérification du quota
    count = get_user_daily_rides_count(db, user_id)
    
    if count >= 4:
        # LOG DE SÉCURITÉ : Très important pour le DevSecOps
        logger.warning(f"SÉCURITÉ - QUOTA ATTEINT : L'utilisateur '{user_id}' a tenté de dépasser la limite de 4 trajets.")
        return None
    
    # Création du trajet
    db_ride = models.Ride(
        **ride.model_dump(), 
        user_id=user_id
    )
    
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    
    # LOG MÉTIER : On trace le succès
    logger.info(f"MÉTIER - TRAJET CRÉÉ : Utilisateur '{user_id}' de {ride.departure_zone} vers {ride.destination_zone}")
    
    return db_ride