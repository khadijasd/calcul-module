# 📊 Module de Calcul de Score - FastAPI

Ce projet expose une API FastAPI permettant de calculer le score et l’écart entre les compétences d’un employé et celles requises par une fiche de poste.

---

## 🧱 Structure du projet

```bash
calcul_module/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── calcul.py         # Endpoints pour le calcul de score
│   ├── core/
│   │   └── config.py             # Paramètres globaux (seuils, configs)
│   ├── models/
│   │   ├── fiche_employe.py      # Modèle de données Employé
│   │   └── fiche_poste.py        # Modèle de données Fiche de poste
│   ├── services/
│   │   └── score.py              # Logique métier : calculs, écarts
│   ├── utils/
│   │   └── helpers.py            # Fonctions utilitaires
│   └── main.py                   # Point d’entrée de l’app FastAPI
├── requirements.txt              # Dépendances Python
├── Dockerfile                    # Image Docker
├── .dockerignore                 # Fichiers ignorés par Docker
├── README.md                     # Documentation du projet





## ⚙️ Préparation de l'environnement local

```bash
# Cloner le projet
git clone https://github.com/khadijasd/calcul-module.git
cd calcul_module

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/macOS

# Ajouter les dépendances dans requirements.txt
fastapi
uvicorn

# Installer les dépendances
pip install -r requirements.txt


🚀 Lancer l’application en local
uvicorn app.main:app --reload

Ensuite, aller sur :

🧪 Swagger Docs : http://localhost:8000/docs

✅ Route test : http://localhost:8000/api/v1/ping

🐳 Utilisation avec Docker

#Construire l’image Docker
docker build -t calcul-api .

#Lancer le conteneur
docker run -p 8000:8000 calcul-api