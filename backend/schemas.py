"""
Schémas Pydantic pour la validation des données
Utilisés pour valider les entrées/sorties de l'API REST
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# ========== Schémas pour les documents ==========

class DocumentBase(BaseModel):
    """Schéma de base pour un document"""
    filename: str
    file_type: Optional[str] = None

class DocumentCreate(DocumentBase):
    """Schéma pour la création d'un document"""
    filepath: str
    extracted_text: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None

class DocumentMetadataBase(BaseModel):
    """Schéma de base pour les métadonnées"""
    word_count: Optional[int] = None
    char_count: Optional[int] = None
    line_count: Optional[int] = None
    language: Optional[str] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    image_size_kb: Optional[float] = None

class DocumentMetadataResponse(DocumentMetadataBase):
    """Schéma de réponse pour les métadonnées"""
    id: int
    document_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentResponse(DocumentBase):
    """Schéma de réponse complet pour un document"""
    id: int
    filepath: str
    extracted_text: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    doc_metadata: List[DocumentMetadataResponse] = []
    
    class Config:
        from_attributes = True

# ========== Schémas pour l'upload ==========

class UploadResponse(BaseModel):
    """Réponse après upload d'un fichier"""
    message: str
    document_id: int
    filename: str
    filepath: str

# ========== Schémas pour l'OCR ==========

class OCRRequest(BaseModel):
    """Requête pour effectuer l'OCR sur un document"""
    document_id: int

class OCRResponse(BaseModel):
    """Réponse de l'OCR"""
    document_id: int
    extracted_text: str
    word_count: int
    language: str
    processing_time: float  # Temps en secondes

# ========== Schémas pour la classification ==========

class ClassifyRequest(BaseModel):
    """Requête pour classifier un document"""
    document_id: int

class ClassifyResponse(BaseModel):
    """Réponse de la classification"""
    document_id: int
    category: str
    confidence: float
    all_predictions: dict  # Toutes les catégories avec leurs scores

# ========== Schémas pour les statistiques ==========

class StatsResponse(BaseModel):
    """Statistiques globales du système"""
    total_documents: int
    documents_by_category: dict
    average_confidence: float
    total_words_extracted: int
    documents_by_type: dict
    recent_documents: int  # Documents des 7 derniers jours

class CategoryStats(BaseModel):
    """Statistiques par catégorie"""
    category: str
    count: int
    percentage: float
    avg_confidence: float
