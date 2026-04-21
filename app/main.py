import logging
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

# 1. Configuration du logging pour qu'il soit visible dans les logs Docker
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("codrive")

# Création des tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="CoDrive API",
    description="Système de covoiturage avec monitoring et quotas",
    version="1.1.0"
)

# 2. Middleware pour logger automatiquement toutes les requêtes HTTP
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Appel API: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Réponse API: Statut {response.status_code}")
    return response

@app.post("/rides/", response_model=schemas.Ride, status_code=status.HTTP_201_CREATED)
def create_ride(
    ride: schemas.RideCreate, 
    user_id: str, 
    db: Session = Depends(database.get_db)
):
    db_ride = crud.create_ride(db=db, ride=ride, user_id=user_id)
    if db_ride is None:
        raise HTTPException(
            status_code=403, 
            detail="Limite de 4 trajets par jour atteinte. Usage professionnel détecté."
        )
    return db_ride

@app.get("/health")
def health_check():
    return {"status": "online", "message": "CoDrive est opérationnel et surveillé"}