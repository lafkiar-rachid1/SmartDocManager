"""
Configuration de la connexion à la base de données PostgreSQL
Utilise SQLAlchemy pour gérer les connexions et sessions
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# URL de connexion PostgreSQL depuis .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/smartdoc_db")

# Créer le moteur de base de données
# echo=True affiche les requêtes SQL (utile pour le débogage)
engine = create_engine(DATABASE_URL, echo=True)

# Créer une factory de sessions
# autocommit=False: les transactions doivent être explicitement validées
# autoflush=False: les objets ne sont pas automatiquement synchronisés
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles déclaratifs
Base = declarative_base()

def get_db():
    """
    Générateur de session de base de données
    Utilisé comme dépendance dans FastAPI
    Assure la fermeture de la session après utilisation
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
