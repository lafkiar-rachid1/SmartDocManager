"""
Service de traitement d'images avec OpenCV
Améliore la qualité des images avant l'OCR
"""

import cv2
import numpy as np
from PIL import Image
import io

class ImageProcessor:
    """
    Classe pour le prétraitement des images avant OCR
    Améliore la qualité et augmente la précision de l'extraction de texte
    """
    
    @staticmethod
    def preprocess_image(image_path: str) -> np.ndarray:
        """
        Prétraite une image pour améliorer l'OCR
        
        Étapes:
        1. Conversion en niveaux de gris
        2. Réduction du bruit
        3. Binarisation (noir et blanc)
        4. Amélioration de la netteté
        
        Args:
            image_path: Chemin vers l'image à traiter
            
        Returns:
            Image numpy array prétraitée
        """
        # Lire l'image
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Impossible de lire l'image: {image_path}")
        
        # Conversion en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Réduction du bruit avec un filtre gaussien
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Binarisation adaptative (seuillage)
        # Meilleur que le seuillage simple pour les images avec éclairage variable
        binary = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        
        # Amélioration de la netteté
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        sharpened = cv2.filter2D(binary, -1, kernel)
        
        return sharpened
    
    @staticmethod
    def detect_orientation(image_path: str) -> float:
        """
        Détecte l'orientation d'une image (rotation)
        Utile pour corriger les documents scannés de travers
        
        Args:
            image_path: Chemin vers l'image
            
        Returns:
            Angle de rotation en degrés
        """
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Détection des contours
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Détection de lignes avec la transformée de Hough
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        
        if lines is not None:
            # Calculer l'angle moyen des lignes
            angles = []
            for rho, theta in lines[:, 0]:
                angle = np.degrees(theta) - 90
                angles.append(angle)
            
            return np.median(angles)
        
        return 0.0
    
    @staticmethod
    def rotate_image(image_path: str, angle: float) -> np.ndarray:
        """
        Effectue une rotation de l'image
        
        Args:
            image_path: Chemin vers l'image
            angle: Angle de rotation en degrés
            
        Returns:
            Image tournée
        """
        img = cv2.imread(image_path)
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        
        # Matrice de rotation
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), 
                                flags=cv2.INTER_CUBIC,
                                borderMode=cv2.BORDER_REPLICATE)
        
        return rotated
    
    @staticmethod
    def resize_image(image_path: str, max_width: int = 2000) -> np.ndarray:
        """
        Redimensionne l'image si elle est trop grande
        Améliore les performances sans perte significative de qualité
        
        Args:
            image_path: Chemin vers l'image
            max_width: Largeur maximale en pixels
            
        Returns:
            Image redimensionnée
        """
        img = cv2.imread(image_path)
        height, width = img.shape[:2]
        
        if width > max_width:
            ratio = max_width / width
            new_width = max_width
            new_height = int(height * ratio)
            resized = cv2.resize(img, (new_width, new_height), 
                               interpolation=cv2.INTER_AREA)
            return resized
        
        return img
    
    @staticmethod
    def get_image_info(image_path: str) -> dict:
        """
        Extrait les informations d'une image
        
        Args:
            image_path: Chemin vers l'image
            
        Returns:
            Dictionnaire avec les métadonnées de l'image
        """
        img = cv2.imread(image_path)
        
        if img is None:
            return {}
        
        height, width = img.shape[:2]
        
        # Taille du fichier en Ko
        import os
        file_size_kb = os.path.getsize(image_path) / 1024
        
        return {
            "width": width,
            "height": height,
            "size_kb": round(file_size_kb, 2),
            "channels": img.shape[2] if len(img.shape) == 3 else 1
        }
