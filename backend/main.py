"""
Point d'entrée principal de l'application FastAPI
Configure le serveur, CORS, et les routes
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Importer les routes API
from api import upload, ocr, classify, stats, auth

# Importer les modèles et la base de données
from database import engine, Base
import models

# Charger les variables d'environnement
load_dotenv()

# Créer les tables dans la base de données
# Si les tables existent déjà, elles ne seront pas recréées
Base.metadata.create_all(bind=engine)

# Créer le dossier de stockage s'il n'existe pas
STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage/documents")
os.makedirs(STORAGE_PATH, exist_ok=True)

# Initialiser l'application FastAPI
app = FastAPI(
    title="Smart Document Manager API",
    description="API de gestion intelligente des documents avec OCR et classification IA",
    version="1.0.0",
    docs_url="/docs",  # Documentation Swagger
    redoc_url="/redoc"  # Documentation ReDoc alternative
)

# Configuration CORS pour permettre les requêtes depuis le frontend
# En production, remplacer "*" par l'URL spécifique du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines (à restreindre en production)
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

# Monter le dossier de stockage pour servir les fichiers statiques
# Accessible via /storage/documents/nom_fichier.pdf
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

# Enregistrer les routes de l'API
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(ocr.router, prefix="/api", tags=["OCR"])
app.include_router(classify.router, prefix="/api", tags=["Classification"])
app.include_router(stats.router, prefix="/api", tags=["Statistiques"])

@app.get("/")
async def root():
    """
    Route racine de l'API
    Retourne un message de bienvenue et l'état du serveur
    """
    return {
        "message": "Bienvenue sur l'API Smart Document Manager",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    Point de vérification de la santé du serveur
    Utile pour le monitoring et les tests
    """
    return {
        "status": "healthy",
        "database": "connected",
        "storage": "available"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Configuration du serveur
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    # Lancer le serveur
    print(f"🚀 Serveur démarré sur http://{host}:{port}")
    print(f"📚 Documentation disponible sur http://{host}:{port}/docs")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Rechargement automatique en développement
        log_level="info"
    )
