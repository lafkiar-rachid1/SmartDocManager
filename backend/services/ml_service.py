"""
Service de Machine Learning pour la classification de documents
Utilise TF-IDF + Naive Bayes pour classifier les documents
"""

import joblib
import os
from typing import Tuple, Dict
import numpy as np

class MLService:
    """
    Service de classification automatique de documents
    Charge un modèle pré-entraîné et prédit la catégorie des documents
    """
    
    def __init__(self):
        """
        Initialise le service ML
        Charge le modèle et le vectorizer depuis les fichiers .pkl
        """
        self.model_path = os.path.join("ml", "model.pkl")
        self.vectorizer_path = os.path.join("ml", "vectorizer.pkl")
        
        self.model = None
        self.vectorizer = None
        self.categories = None  # Sera défini après chargement du modèle
        
        # Charger le modèle s'il existe
        self.load_model()
    
    def load_model(self):
        """
        Charge le modèle et le vectorizer depuis les fichiers
        """
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                # Récupérer les catégories directement du modèle (ordre correct)
                self.categories = self.model.classes_.tolist()
                print(f"✅ Modèle ML chargé avec succès")
                print(f"📊 Catégories (ordre du modèle): {self.categories}")
            else:
                print("⚠️ Modèle ML non trouvé. Veuillez exécuter train_model.py")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
    
    def predict(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Prédit la catégorie d'un document à partir de son texte
        
        Args:
            text: Texte du document à classifier
            
        Returns:
            Tuple (catégorie prédite, score de confiance, tous les scores)
        """
        if self.model is None or self.vectorizer is None or self.categories is None:
            raise Exception("Modèle ML non chargé. Veuillez entraîner le modèle d'abord.")
        
        if not text or len(text.strip()) == 0:
            return "Autre", 0.0, {}
        
        try:
            # Vectoriser le texte avec TF-IDF
            text_vectorized = self.vectorizer.transform([text])
            
            # Prédire la catégorie
            prediction = self.model.predict(text_vectorized)[0]
            
            # Obtenir les probabilités pour toutes les catégories
            probabilities = self.model.predict_proba(text_vectorized)[0]
            
            # Créer un dictionnaire avec toutes les prédictions
            # IMPORTANT: utiliser model.classes_ pour garantir le bon ordre
            all_predictions = {}
            for category, prob in zip(self.model.classes_, probabilities):
                all_predictions[category] = round(float(prob), 4)
            
            # Trouver la catégorie avec la plus haute probabilité
            max_prob_index = np.argmax(probabilities)
            predicted_category = self.model.classes_[max_prob_index]
            confidence = float(probabilities[max_prob_index])
            
            print(f"🔍 Prédiction: {predicted_category} (confiance: {confidence:.2%})")
            print(f"📊 Tous les scores: {all_predictions}")
            
            return predicted_category, round(confidence, 4), all_predictions
            
        except Exception as e:
            raise Exception(f"Erreur lors de la prédiction: {str(e)}")
    
    def predict_batch(self, texts: list) -> list:
        """
        Prédit les catégories de plusieurs documents
        
        Args:
            texts: Liste de textes à classifier
            
        Returns:
            Liste de tuples (catégorie, confiance, tous_scores)
        """
        results = []
        for text in texts:
            result = self.predict(text)
            results.append(result)
        return results
    
    def get_feature_importance(self, category: str, top_n: int = 10) -> Dict[str, float]:
        """
        Retourne les mots les plus importants pour une catégorie
        Utile pour comprendre la décision du modèle
        
        Args:
            category: Nom de la catégorie
            top_n: Nombre de mots à retourner
            
        Returns:
            Dictionnaire {mot: importance}
        """
        if self.model is None or self.vectorizer is None:
            return {}
        
        try:
            # Trouver l'index de la catégorie
            category_idx = self.categories.index(category)
            
            # Obtenir les coefficients du modèle pour cette catégorie
            coefficients = self.model.coef_[category_idx]
            
            # Obtenir les noms des features (mots)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Trier par importance
            top_indices = np.argsort(coefficients)[-top_n:][::-1]
            
            importance_dict = {}
            for idx in top_indices:
                importance_dict[feature_names[idx]] = round(float(coefficients[idx]), 4)
            
            return importance_dict
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des features: {e}")
            return {}
    
    def get_model_info(self) -> Dict:
        """
        Retourne des informations sur le modèle chargé
        
        Returns:
            Dictionnaire avec les informations du modèle
        """
        if self.model is None:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_type": type(self.model).__name__,
            "categories": self.categories,
            "n_features": len(self.vectorizer.get_feature_names_out()),
            "model_path": self.model_path
        }
