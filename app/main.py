from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError

from . import crud, models, schemas, database, auth_utils

# Création automatique des tables (Utile pour le développement)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="CoDrive API - Secured Edition")

# Configuration pour récupérer le token dans les headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dépendance pour la base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- LOGIQUE DE SÉCURITÉ (Middleware) ---

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Session invalide ou expirée",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Décoder le token JWT
        payload = jwt.decode(token, auth_utils.SECRET_KEY, algorithms=[auth_utils.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    # --- POINT 3 : VÉRIFICATION MENSUELLE ---
    # Si l'utilisateur n'a pas été vérifié depuis plus de 30 jours
    if user.last_verified_at:
        expiry_limit = datetime.utcnow() - timedelta(days=30)
        if user.last_verified_at < expiry_limit:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Votre vérification mensuelle a expiré. Veuillez valider votre email académique/pro."
            )
            
    return user

# --- ROUTES D'AUTHENTIFICATION ---

@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth_utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Le token dure 30 jours (aligné sur ta règle de vérification)
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """Permet de vérifier les infos de l'utilisateur connecté"""
    return current_user

# --- ROUTES DES TRAJETS (TRIPS) ---

@app.get("/trips/", response_model=list[schemas.Trip])
def read_trips(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Tout le monde peut voir les trajets disponibles"""
    trips = crud.get_trips(db, skip=skip, limit=limit)
    return trips

@app.post("/trips/", response_model=schemas.Trip)
def create_trip(
    trip: schemas.TripCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    POINT 1 : Seul un utilisateur connecté et vérifié peut créer un trajet.
    L'ID du créateur est récupéré automatiquement depuis le Token.
    """
    return crud.create_trip(db=db, trip=trip, user_id=current_user.id)