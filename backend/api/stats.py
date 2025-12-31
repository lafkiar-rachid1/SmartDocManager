"""
Route API pour les statistiques et l'export de données
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
import schemas
from auth_utils import get_current_active_user
from datetime import datetime, timedelta
import pandas as pd
import io

router = APIRouter()

@router.get("/stats", response_model=schemas.StatsResponse)
async def get_statistics(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retourne les statistiques de l'utilisateur connecté
    
    Args:
        db: Session de base de données
        
    Returns:
        Statistiques complètes
    """
    try:
        # Nombre total de documents de l'utilisateur
        total_documents = db.query(models.Document).filter(
            models.Document.user_id == current_user.id
        ).count()
        
        # Documents par catégorie
        category_counts = db.query(
            models.Document.category,
            func.count(models.Document.id)
        ).filter(
            models.Document.category.isnot(None),
            models.Document.user_id == current_user.id
        ).group_by(models.Document.category).all()
        
        documents_by_category = {
            category: count for category, count in category_counts
        }
        
        # Confiance moyenne
        avg_confidence = db.query(
            func.avg(models.Document.confidence)
        ).filter(
            models.Document.confidence.isnot(None),
            models.Document.user_id == current_user.id
        ).scalar() or 0.0
        
        # Total de mots extraits
        total_words = db.query(
            func.sum(models.DocumentMetadata.word_count)
        ).join(models.Document).filter(
            models.Document.user_id == current_user.id
        ).scalar() or 0
        
        # Documents par type de fichier
        type_counts = db.query(
            models.Document.file_type,
            func.count(models.Document.id)
        ).filter(
            models.Document.user_id == current_user.id
        ).group_by(models.Document.file_type).all()
        
        documents_by_type = {
            file_type: count for file_type, count in type_counts
        }
        
        # Documents récents (7 derniers jours)
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_documents = db.query(models.Document).filter(
            models.Document.created_at >= seven_days_ago,
            models.Document.user_id == current_user.id
        ).count()
        
        return schemas.StatsResponse(
            total_documents=total_documents,
            documents_by_category=documents_by_category,
            average_confidence=round(avg_confidence, 4),
            total_words_extracted=total_words,
            documents_by_type=documents_by_type,
            recent_documents=recent_documents
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul des statistiques: {str(e)}"
        )

@router.get("/stats/categories")
async def get_category_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Retourne des statistiques détaillées par catégorie
    
    Args:
        db: Session de base de données
        current_user: Utilisateur connecté
        
    Returns:
        Liste de statistiques par catégorie
    """
    try:
        # Nombre total de documents classés
        total_classified = db.query(models.Document).filter(
            models.Document.category.isnot(None),
            models.Document.user_id == current_user.id
        ).count()
        
        if total_classified == 0:
            return {"message": "Aucun document classé", "categories": []}
        
        # Stats par catégorie
        categories_data = []
        
        category_stats = db.query(
            models.Document.category,
            func.count(models.Document.id).label('count'),
            func.avg(models.Document.confidence).label('avg_confidence')
        ).filter(
            models.Document.category.isnot(None),
            models.Document.user_id == current_user.id
        ).group_by(models.Document.category).all()
        
        for category, count, avg_conf in category_stats:
            percentage = (count / total_classified) * 100
            
            categories_data.append({
                "category": category,
                "count": count,
                "percentage": round(percentage, 2),
                "avg_confidence": round(avg_conf or 0.0, 4)
            })
        
        # Trier par nombre de documents
        categories_data.sort(key=lambda x: x['count'], reverse=True)
        
        return {
            "total_classified": total_classified,
            "categories": categories_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul des statistiques par catégorie: {str(e)}"
        )

@router.get("/stats/timeline")
async def get_timeline_stats(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Retourne l'évolution des documents dans le temps
    
    Args:
        days: Nombre de jours à analyser
        db: Session de base de données
        current_user: Utilisateur connecté
        
    Returns:
        Timeline des documents créés
    """
    try:
        start_date = datetime.now() - timedelta(days=days)
        
        # Documents par jour
        daily_counts = db.query(
            func.date(models.Document.created_at).label('date'),
            func.count(models.Document.id).label('count')
        ).filter(
            models.Document.created_at >= start_date,
            models.Document.user_id == current_user.id
        ).group_by(func.date(models.Document.created_at)).all()
        
        timeline_data = [
            {
                "date": str(date),
                "count": count
            }
            for date, count in daily_counts
        ]
        
        timeline_data.sort(key=lambda x: x['date'])
        
        return {
            "period_days": days,
            "timeline": timeline_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul de la timeline: {str(e)}"
        )

@router.get("/export/csv")
async def export_to_csv(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Exporte tous les documents au format CSV
    
    Args:
        db: Session de base de données
        current_user: Utilisateur connecté
        
    Returns:
        Fichier CSV téléchargeable
    """
    try:
        # Récupérer tous les documents avec leurs métadonnées
        documents = db.query(models.Document).filter(
            models.Document.user_id == current_user.id
        ).all()
        
        if not documents:
            raise HTTPException(status_code=404, detail="Aucun document à exporter")
        
        # Préparer les données pour le DataFrame
        data = []
        for doc in documents:
            metadata = doc.doc_metadata[0] if doc.doc_metadata else None
            
            data.append({
                "ID": doc.id,
                "Nom du fichier": doc.filename,
                "Type": doc.file_type,
                "Catégorie": doc.category or "Non classé",
                "Confiance": doc.confidence or 0.0,
                "Nombre de mots": metadata.word_count if metadata else 0,
                "Langue": metadata.language if metadata else "N/A",
                "Largeur image": metadata.image_width if metadata else 0,
                "Hauteur image": metadata.image_height if metadata else 0,
                "Taille (Ko)": metadata.image_size_kb if metadata else 0,
                "Date de création": doc.created_at.strftime("%Y-%m-%d %H:%M:%S") if doc.created_at else ""
            })
        
        # Créer le DataFrame
        df = pd.DataFrame(data)
        
        # Convertir en CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')  # utf-8-sig pour Excel
        csv_buffer.seek(0)
        
        # Créer la réponse avec le fichier CSV
        return StreamingResponse(
            iter([csv_buffer.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=documents_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'export CSV: {str(e)}"
        )

@router.get("/export/json")
async def export_to_json(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Exporte tous les documents au format JSON
    
    Args:
        db: Session de base de données
        current_user: Utilisateur connecté
        
    Returns:
        Fichier JSON téléchargeable
    """
    try:
        documents = db.query(models.Document).filter(
            models.Document.user_id == current_user.id
        ).all()
        
        if not documents:
            raise HTTPException(status_code=404, detail="Aucun document à exporter")
        
        # Convertir en format JSON
        export_data = []
        for doc in documents:
            metadata = doc.doc_metadata[0] if doc.doc_metadata else None
            
            export_data.append({
                "id": doc.id,
                "filename": doc.filename,
                "file_type": doc.file_type,
                "category": doc.category,
                "confidence": doc.confidence,
                "extracted_text": doc.extracted_text,
                "metadata": {
                    "word_count": metadata.word_count if metadata else None,
                    "language": metadata.language if metadata else None,
                    "image_width": metadata.image_width if metadata else None,
                    "image_height": metadata.image_height if metadata else None,
                    "image_size_kb": metadata.image_size_kb if metadata else None
                } if metadata else None,
                "created_at": doc.created_at.isoformat() if doc.created_at else None
            })
        
        return {
            "total": len(export_data),
            "export_date": datetime.now().isoformat(),
            "documents": export_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'export JSON: {str(e)}"
        )
