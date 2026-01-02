"""
Routes API pour les visiteurs (analyse sans authentification)
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from services.ml_service import MLService
from services.ocr_service import OCRService

router = APIRouter()

# Initialiser les services
ml_service = MLService()
ocr_service = OCRService()


@router.post("/analyze-guest")
async def analyze_guest_document(file: UploadFile = File(...)):
    """
    Analyse un document pour un visiteur sans l'enregistrer dans la base de données
    
    - Extrait le texte du document (OCR si image, texte si PDF)
    - Classifie le document avec le modèle ML
    - Retourne la catégorie et le niveau de confiance
    - Ne sauvegarde RIEN dans la base de données
    """
    # Vérifier le type de fichier
    allowed_types = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Type de fichier non supporté. Formats acceptés: PDF, JPG, PNG"
        )
    
    # Vérifier la taille du fichier (max 10 MB)
    file_size = 0
    temp_file_path = None
    
    try:
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            
            # Lire et écrire le fichier par chunks
            while chunk := await file.read(1024 * 1024):  # 1 MB chunks
                file_size += len(chunk)
                
                if file_size > 10 * 1024 * 1024:  # 10 MB max
                    raise HTTPException(
                        status_code=400,
                        detail="Le fichier est trop volumineux. Taille maximale: 10 MB"
                    )
                
                temp_file.write(chunk)
        
        # Extraire le texte selon le type de fichier
        if file.content_type == 'application/pdf':
            extracted_text, metadata = ocr_service.extract_text_from_pdf(temp_file_path)
        else:
            extracted_text, metadata = ocr_service.extract_text_from_image(temp_file_path)
        
        # Vérifier qu'on a extrait du texte
        if not extracted_text or len(extracted_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Impossible d'extraire du texte du document. Assurez-vous que le document contient du texte lisible."
            )
        
        # Classifier le document
        category, confidence, all_predictions = ml_service.predict(extracted_text)
        
        # Retourner les résultats (sans sauvegarder)
        return JSONResponse(content={
            "category": category,
            "confidence": float(confidence * 100),  # Convertir en pourcentage
            "text_length": len(extracted_text),
            "word_count": metadata.get("word_count", 0),
            "message": "Analyse terminée. Ce document n'a pas été sauvegardé."
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse du document: {str(e)}"
        )
    
    finally:
        # Nettoyer le fichier temporaire
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass
