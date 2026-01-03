"""
Route API pour le téléversement de documents
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import os
import shutil
from datetime import datetime
from dotenv import load_dotenv
from auth_utils import get_current_active_user

load_dotenv()

router = APIRouter()

STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage/documents")

@router.post("/upload", response_model=schemas.UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Téléverse un document (PDF, PNG, JPG)
    
    Args:
        file: Fichier à téléverser
        db: Session de base de données
        
    Returns:
        Informations sur le document téléversé
    """
    # Vérifier le type de fichier
    allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté. Extensions autorisées: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Créer un nom de fichier unique avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(STORAGE_PATH, safe_filename)
        
        # Créer le dossier de stockage s'il n'existe pas
        os.makedirs(STORAGE_PATH, exist_ok=True)
        
        # Sauvegarder le fichier
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Déterminer le type de fichier
        file_type = "PDF" if file_extension == '.pdf' else "IMAGE"
        
        # Créer l'entrée dans la base de données
        db_document = models.Document(
            filename=file.filename,
            filepath=file_path,
            file_type=file_type,
            user_id=current_user.id
        )
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        return schemas.UploadResponse(
            message="Document téléversé avec succès",
            document_id=db_document.id,
            filename=file.filename,
            filepath=file_path,
            file_type=file_type
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du téléversement: {str(e)}"
        )

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Supprime un document
    
    Args:
        document_id: ID du document à supprimer
        db: Session de base de données
        
    Returns:
        Message de confirmation
    """
    # Récupérer le document
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé ou accès refusé")
    
    try:
        # Supprimer le fichier physique
        if os.path.exists(document.filepath):
            os.remove(document.filepath)
        
        # Supprimer de la base de données
        db.delete(document)
        db.commit()
        
        return {"message": "Document supprimé avec succès", "document_id": document_id}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )

@router.get("/documents", response_model=list[schemas.DocumentResponse])
async def get_all_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Récupère tous les documents de l'utilisateur connecté
    
    Args:
        skip: Nombre de documents à ignorer (pagination)
        limit: Nombre maximum de documents à retourner
        db: Session de base de données
        
    Returns:
        Liste de documents
    """
    documents = db.query(models.Document).filter(
        models.Document.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return documents

@router.get("/documents/{document_id}", response_model=schemas.DocumentResponse)
async def get_document(
    document_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Récupère un document spécifique
    
    Args:
        document_id: ID du document
        db: Session de base de données
        
    Returns:
        Document avec ses métadonnées
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    
    return document
@router.get("/documents/{document_id}/image")
async def get_document_image(
    document_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Récupère l'image d'un document
    
    Args:
        document_id: ID du document
        db: Session de base de données
        current_user: Utilisateur connecté
        
    Returns:
        Fichier image
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    
    # Vérifier que c'est bien une image
    if document.file_type != 'IMAGE':
        raise HTTPException(status_code=400, detail="Ce document n'est pas une image")
    
    # Construire le chemin du fichier
    file_path = os.path.join(STORAGE_PATH, document.filepath)
    
    print(f"DEBUG - STORAGE_PATH: {STORAGE_PATH}")
    print(f"DEBUG - document.filepath: {document.filepath}")
    print(f"DEBUG - file_path complet: {file_path}")
    print(f"DEBUG - Fichier existe: {os.path.exists(file_path)}")
    
    if not os.path.exists(file_path):
        # Essayer aussi avec un chemin absolu direct
        if os.path.exists(document.filepath):
            file_path = document.filepath
        else:
            raise HTTPException(
                status_code=404, 
                detail=f"Fichier image non trouvé. Chemin: {file_path}"
            )
    
    # Retourner le fichier
    return FileResponse(file_path, media_type=f"image/{document.filepath.split('.')[-1]}")