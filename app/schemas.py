from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Ce qu'on reçoit quand on crée un trajet
class RideCreate(BaseModel):
    departure_zone: str
    destination_zone: str
    price: float
    departure_time: datetime

# Ce qu'on renvoie à l'utilisateur (avec l'ID et la date de création)
class Ride(RideCreate):
    id: int
    user_id: str
    created_at: datetime

    model_config = {
    "from_attributes": True
}