FROM python:3.10-bullseye

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev libssl-dev curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances Python avec options robustes pour connexion lente
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    --default-timeout=1000 \
    --retries 10 \
    --timeout 1000 \
    --progress-bar off \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# Télécharger modèle spaCy (optionnel si déjà dans requirements.txt)
RUN python -m spacy download en_core_web_sm

# Copier le code source
COPY app ./app

# Lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
