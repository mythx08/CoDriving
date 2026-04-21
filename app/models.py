from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base
import datetime

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # Identifiant du conducteur
    
    # Zones au lieu de coordonnées GPS
    departure_zone = Column(String, nullable=False) 
    destination_zone = Column(String, nullable=False)
    
    price = Column(Float)
    departure_time = Column(DateTime)
    
    # Pour le quota des 4 trajets/jour
    created_at = Column(DateTime, default=datetime.datetime.utcnow)