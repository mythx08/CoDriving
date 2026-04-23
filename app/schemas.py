from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime

# Liste des domaines autorisés (Tu pourras en ajouter d'autres)
ALLOWED_DOMAINS = ["inpt.ac.ma", "intelcia.com", "um6p.ma"]

class UserBase(BaseModel):
    email: EmailStr

    @field_validator('email')
    @classmethod
    def validate_pro_email(cls, v: str):
        domain = v.split('@')[-1]
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(f"Accès refusé. Seuls les emails de ces domaines sont autorisés : {', '.join(ALLOWED_DOMAINS)}")
        return v

class UserCreate(UserBase):
    password: str
    full_name: str

class UserOut(UserBase):
    id: int
    is_active: bool
    last_verified_at: datetime

    class Config:
        from_attributes = True

# --- Mise à jour de Trip ---
class TripBase(BaseModel):
    destination: str
    date: str

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True