"""
Modèles SQLAlchemy pour la base de données PostgreSQL
Définit la structure des tables et les relations entre elles
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """
    Table des utilisateurs pour l'authentification
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relation avec les documents
    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"


class Document(Base):
    """
    Table principale stockant les documents téléversés et analysés
    """
    __tablename__ = "documents"
    
    # Clé primaire auto-incrémentée
    id = Column(Integer, primary_key=True, index=True)
    
    # Clé étrangère vers l'utilisateur
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Informations sur le fichier
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    file_type = Column(String(50))  # PDF, PNG, JPG
    
    # Résultats de l'analyse OCR
    extracted_text = Column(Text)  # Texte extrait par OCR
    
    # Résultats de la classification ML
    category = Column(String(100))  # Facture, CV, Contrat, Lettre, Autre
    confidence = Column(Float)  # Score de confiance (0-1)
    
    # Métadonnées temporelles
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    owner = relationship("User", back_populates="documents")
    doc_metadata = relationship("DocumentMetadata", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, category={self.category})>"


class DocumentMetadata(Base):
    """
    Table des métadonnées extraites des documents
    Contient des informations analytiques supplémentaires
    """
    __tablename__ = "document_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Statistiques du texte
    word_count = Column(Integer)  # Nombre de mots
    char_count = Column(Integer)  # Nombre de caractères
    line_count = Column(Integer)  # Nombre de lignes
    
    # Informations linguistiques
    language = Column(String(10))  # Code langue (fra, eng, etc.)
    
    # Informations sur l'image
    image_width = Column(Integer)
    image_height = Column(Integer)
    image_size_kb = Column(Float)  # Taille en Ko
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relation inverse vers Document
    document = relationship("Document", back_populates="doc_metadata")
    
    def __repr__(self):
        return f"<DocumentMetadata(id={self.id}, document_id={self.document_id}, words={self.word_count})>"
