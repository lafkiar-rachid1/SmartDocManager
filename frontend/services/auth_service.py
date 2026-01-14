"""
Service d'authentification pour gérer les tokens JWT et l'état utilisateur
"""
import streamlit as st
import requests
import json
from typing import Optional, Dict

API_URL = "http://localhost:8000"

class AuthService:
    """Service pour gérer l'authentification des utilisateurs"""
    
    @staticmethod
    def login(username: str, password: str) -> Dict:
        """Connexion utilisateur"""
        try:
            response = requests.post(
                f"{API_URL}/api/auth/login",
                data={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                # Sauvegarder dans session_state
                st.session_state.token = data["access_token"]
                st.session_state.user = data["user"]
                st.session_state.is_authenticated = True
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": response.json().get("detail", "Erreur de connexion")}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def register(username: str, email: str, password: str) -> Dict:
        """Inscription utilisateur"""
        try:
            response = requests.post(
                f"{API_URL}/api/auth/register",
                json={"username": username, "email": email, "password": password}
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.json().get("detail", "Erreur d'inscription")}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def logout():
        """Déconnexion utilisateur"""
        # Nettoyer session_state
        if 'token' in st.session_state:
            del st.session_state.token
        if 'user' in st.session_state:
            del st.session_state.user
        if 'is_authenticated' in st.session_state:
            del st.session_state.is_authenticated
        st.rerun()
    
    @staticmethod
    def is_authenticated() -> bool:
        """Vérifier si l'utilisateur est authentifié"""
        return st.session_state.get('is_authenticated', False)
    
    @staticmethod
    def get_token() -> Optional[str]:
        """Récupérer le token JWT"""
        return st.session_state.get('token', None)
    
    @staticmethod
    def get_user() -> Optional[Dict]:
        """Récupérer les informations utilisateur"""
        return st.session_state.get('user', None)
    
    @staticmethod
    def get_headers() -> Dict:
        """Récupérer les headers avec le token d'authentification"""
        token = AuthService.get_token()
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}
