# 1. Utiliser une image Python légère (slim) pour réduire la taille et la surface d'attaque
FROM python:3.11-slim

# 2. Définir le dossier de travail
WORKDIR /code

# 3. Copier les dépendances et les installer
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. Copier le code de l'application
COPY ./app /code/app

# 5. Sécurité : Créer un utilisateur "non-root"
# En production, on ne fait jamais tourner un conteneur en mode administrateur (root)
RUN useradd -m appuser
USER appuser

# 6. Lancer le serveur uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]