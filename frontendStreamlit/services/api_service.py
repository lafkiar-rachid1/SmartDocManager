"""
Service API pour communiquer avec le backend
"""
import requests
from typing import Dict, List, Optional
from services.auth_service import AuthService

API_URL = "http://localhost:8000"

class APIService:
    """Service pour toutes les requêtes API"""
    
    @staticmethod
    def upload_document(file, filename: str) -> Dict:
        """Upload un document"""
        try:
            # Détecter le type MIME basé sur l'extension
            content_type = 'application/octet-stream'
            filename_lower = filename.lower()
            if filename_lower.endswith('.pdf'):
                content_type = 'application/pdf'
            elif filename_lower.endswith(('.jpg', '.jpeg')):
                content_type = 'image/jpeg'
            elif filename_lower.endswith('.png'):
                content_type = 'image/png'
            
            files = {'file': (filename, file, content_type)}
            response = requests.post(
                f"{API_URL}/api/upload",
                files=files,
                headers=AuthService.get_headers()
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.json().get("detail", "Erreur d'upload")}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def analyze_guest_document(file, filename: str) -> Dict:
        """Analyse un document sans authentification (mode visiteur)"""
        try:
            # Détecter le type MIME basé sur l'extension
            content_type = 'application/octet-stream'
            filename_lower = filename.lower()
            if filename_lower.endswith('.pdf'):
                content_type = 'application/pdf'
            elif filename_lower.endswith(('.jpg', '.jpeg')):
                content_type = 'image/jpeg'
            elif filename_lower.endswith('.png'):
                content_type = 'image/png'
            
            files = {'file': (filename, file, content_type)}
            response = requests.post(
                f"{API_URL}/api/analyze-guest",
                files=files
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.json().get("detail", "Erreur d'analyse")}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_documents() -> Dict:
        """Récupérer tous les documents de l'utilisateur"""
        try:
            response = requests.get(
                f"{API_URL}/api/documents",
                headers=AuthService.get_headers()
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Erreur de récupération"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete_document(document_id: int) -> Dict:
        """Supprimer un document"""
        try:
            response = requests.delete(
                f"{API_URL}/api/documents/{document_id}",
                headers=AuthService.get_headers()
            )
            
            if response.status_code == 200:
                return {"success": True}
            else:
                return {"success": False, "error": "Erreur de suppression"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def perform_ocr(document_id: int) -> Dict:
        """Effectuer l'OCR sur un document"""
        try:
            response = requests.post(
                f"{API_URL}/api/ocr",
                json={"document_id": document_id},
                headers=AuthService.get_headers()
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.json().get("detail", "Erreur OCR")}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def classify_document(document_id: int) -> Dict:
        """Classifier un document"""
        try:
            response = requests.post(
                f"{API_URL}/api/classify",
                json={"document_id": document_id},
                headers=AuthService.get_headers()
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.json().get("detail", "Erreur classification")}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_statistics() -> Dict:
        """Récupérer les statistiques"""
        try:
            response = requests.get(
                f"{API_URL}/api/stats",
                headers=AuthService.get_headers()
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Erreur de récupération"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_category_statistics() -> Dict:
        """Récupérer les statistiques par catégorie"""
        try:
            response = requests.get(
                f"{API_URL}/api/stats/categories",
                headers=AuthService.get_headers()
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Erreur de récupération"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_document_image(document_id: int):
        """Récupérer l'image d'un document"""
        try:
            response = requests.get(
                f"{API_URL}/api/documents/{document_id}/image",
                headers=AuthService.get_headers()
            )
            
            if response.status_code == 200:
                return response.content
            else:
                return None
        except Exception as e:
            return None
