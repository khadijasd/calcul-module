# 1. Image de base légère avec Python
FROM python:3.10-slim

# 2. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 3. Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier le dossier "app" dans le conteneur
COPY ./app ./app

# 5. Exposer le port sur lequel Uvicorn va tourner
EXPOSE 8000

# 6. Commande pour lancer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
