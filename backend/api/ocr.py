"""
Route API pour l'extraction OCR
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from services.ocr_service import OCRService
from services.image_processing import ImageProcessor
from auth_utils import get_current_active_user
import os
import tempfile

router = APIRouter()
ocr_service = OCRService()
image_processor = ImageProcessor()

@router.post("/ocr", response_model=schemas.OCRResponse)
async def perform_ocr(
    request: schemas.OCRRequest,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Effectue l'OCR sur un document téléversé
    
    Args:
        request: Requête contenant l'ID du document
        db: Session de base de données
        
    Returns:
        Texte extrait et métadonnées
    """
    # Récupérer le document
    document = db.query(models.Document).filter(
        models.Document.id == request.document_id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    
    if not os.path.exists(document.filepath):
        raise HTTPException(status_code=404, detail="Fichier physique non trouvé")
    
    try:
        extracted_text = ""
        metadata_dict = {}
        
        # Traiter selon le type de fichier
        if document.file_type == "PDF":
            # Extraire le texte du PDF
            extracted_text, metadata_dict = ocr_service.extract_text_from_pdf(
                document.filepath
            )
        else:
            # Prétraiter l'image avec OpenCV
            try:
                preprocessed_image = image_processor.preprocess_image(document.filepath)
                
                # Sauvegarder l'image prétraitée temporairement
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                    temp_path = temp_file.name
                    import cv2
                    cv2.imwrite(temp_path, preprocessed_image)
                
                # Extraire le texte de l'image prétraitée
                extracted_text, metadata_dict = ocr_service.extract_text_from_image(
                    temp_path
                )
                
                # Nettoyer le fichier temporaire
                os.unlink(temp_path)
                
            except Exception as e:
                # Si le prétraitement échoue, utiliser l'image originale
                print(f"Prétraitement échoué, utilisation de l'image originale: {e}")
                extracted_text, metadata_dict = ocr_service.extract_text_from_image(
                    document.filepath
                )
        
        # Mettre à jour le document avec le texte extrait
        document.extracted_text = extracted_text
        
        # Obtenir les informations de l'image
        image_info = image_processor.get_image_info(document.filepath)
        
        # Créer ou mettre à jour les métadonnées
        existing_metadata = db.query(models.DocumentMetadata).filter(
            models.DocumentMetadata.document_id == document.id
        ).first()
        
        if existing_metadata:
            # Mettre à jour
            existing_metadata.word_count = metadata_dict.get("word_count")
            existing_metadata.char_count = metadata_dict.get("char_count")
            existing_metadata.line_count = metadata_dict.get("line_count")
            existing_metadata.language = metadata_dict.get("language")
            existing_metadata.image_width = image_info.get("width")
            existing_metadata.image_height = image_info.get("height")
            existing_metadata.image_size_kb = image_info.get("size_kb")
        else:
            # Créer nouvelle métadonnée
            db_metadata = models.DocumentMetadata(
                document_id=document.id,
                word_count=metadata_dict.get("word_count"),
                char_count=metadata_dict.get("char_count"),
                line_count=metadata_dict.get("line_count"),
                language=metadata_dict.get("language"),
                image_width=image_info.get("width"),
                image_height=image_info.get("height"),
                image_size_kb=image_info.get("size_kb")
            )
            db.add(db_metadata)
        
        db.commit()
        
        return schemas.OCRResponse(
            document_id=document.id,
            extracted_text=extracted_text,
            word_count=metadata_dict.get("word_count", 0),
            language=metadata_dict.get("language", "fra"),
            processing_time=metadata_dict.get("processing_time", 0.0)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'extraction OCR: {str(e)}"
        )

@router.get("/ocr/languages")
async def get_supported_languages():
    """
    Retourne la liste des langues supportées par Tesseract
    
    Returns:
        Liste des codes de langues
    """
    try:
        languages = ocr_service.get_supported_languages()
        return {
            "languages": languages,
            "default": ocr_service.default_language
        }
    except Exception as e:
        return {
            "languages": ["fra", "eng"],
            "default": "fra",
            "error": str(e)
        }
