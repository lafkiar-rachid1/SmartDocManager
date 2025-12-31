"""
Schémas Pydantic pour l'authentification
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schéma pour la création d'un nouvel utilisateur"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """Schéma pour la connexion d'un utilisateur"""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schéma pour la réponse contenant les infos utilisateur"""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schéma pour le token JWT"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Données contenues dans le token"""
    username: Optional[str] = None
