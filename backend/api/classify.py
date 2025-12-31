"""
Route API pour la classification automatique de documents
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from auth_utils import get_current_active_user
from services.ml_service import MLService

router = APIRouter()
ml_service = MLService()

@router.post("/classify", response_model=schemas.ClassifyResponse)
async def classify_document(
    request: schemas.ClassifyRequest,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Classifie automatiquement un document
    
    Args:
        request: Requête contenant l'ID du document
        db: Session de base de données
        
    Returns:
        Catégorie prédite, score de confiance et toutes les prédictions
    """
    # Récupérer le document
    document = db.query(models.Document).filter(
        models.Document.id == request.document_id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    
    # Vérifier que le texte a été extrait
    if not document.extracted_text or len(document.extracted_text.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Le texte du document n'a pas été extrait. Veuillez d'abord effectuer l'OCR."
        )
    
    try:
        # Prédire la catégorie
        category, confidence, all_predictions = ml_service.predict(document.extracted_text)
        
        # Mettre à jour le document
        document.category = category
        document.confidence = confidence
        
        db.commit()
        
        return schemas.ClassifyResponse(
            document_id=document.id,
            category=category,
            confidence=confidence,
            all_predictions=all_predictions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la classification: {str(e)}"
        )

@router.post("/classify/batch")
async def classify_batch_documents(
    document_ids: list[int],
    db: Session = Depends(get_db)
):
    """
    Classifie plusieurs documents en une seule requête
    
    Args:
        document_ids: Liste des IDs de documents
        db: Session de base de données
        
    Returns:
        Liste des résultats de classification
    """
    results = []
    
    for doc_id in document_ids:
        document = db.query(models.Document).filter(
            models.Document.id == doc_id
        ).first()
        
        if document and document.extracted_text:
            try:
                category, confidence, all_predictions = ml_service.predict(
                    document.extracted_text
                )
                
                # Mettre à jour le document
                document.category = category
                document.confidence = confidence
                
                results.append({
                    "document_id": doc_id,
                    "category": category,
                    "confidence": confidence,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "document_id": doc_id,
                    "error": str(e),
                    "success": False
                })
        else:
            results.append({
                "document_id": doc_id,
                "error": "Document non trouvé ou texte non extrait",
                "success": False
            })
    
    db.commit()
    
    return {
        "total": len(document_ids),
        "successful": sum(1 for r in results if r.get("success")),
        "failed": sum(1 for r in results if not r.get("success")),
        "results": results
    }

@router.get("/classify/categories")
async def get_categories():
    """
    Retourne la liste des catégories disponibles
    
    Returns:
        Liste des catégories
    """
    return {
        "categories": ml_service.categories,
        "model_info": ml_service.get_model_info()
    }

@router.get("/classify/feature-importance/{category}")
async def get_feature_importance(category: str, top_n: int = 10):
    """
    Retourne les mots les plus importants pour une catégorie
    
    Args:
        category: Nom de la catégorie
        top_n: Nombre de mots à retourner
        
    Returns:
        Dictionnaire des mots importants
    """
    if category not in ml_service.categories:
        raise HTTPException(
            status_code=400,
            detail=f"Catégorie invalide. Catégories disponibles: {ml_service.categories}"
        )
    
    try:
        importance = ml_service.get_feature_importance(category, top_n)
        return {
            "category": category,
            "top_features": importance
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'extraction des features: {str(e)}"
        )
