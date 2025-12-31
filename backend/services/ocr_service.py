"""
Service OCR (Optical Character Recognition)
Utilise Tesseract pour extraire le texte des images et PDF
"""

import pytesseract
from PIL import Image
import os
from pdf2image import convert_from_path
import tempfile
from typing import Tuple, Dict
import time
from dotenv import load_dotenv

load_dotenv()

class OCRService:
    """
    Service d'extraction de texte à partir d'images et de PDF
    Utilise Tesseract OCR avec support multilingue
    """
    
    def __init__(self):
        """
        Initialise le service OCR
        Configure le chemin vers Tesseract si nécessaire (Windows)
        """
        # Configuration Tesseract pour Windows
        tesseract_cmd = os.getenv("TESSERACT_CMD")
        if tesseract_cmd and os.path.exists(tesseract_cmd):
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        # Configuration du dossier tessdata
        tessdata_prefix = os.getenv("TESSDATA_PREFIX")
        if tessdata_prefix:
            os.environ["TESSDATA_PREFIX"] = tessdata_prefix
        
        # Langue par défaut
        self.default_language = os.getenv("OCR_LANGUAGE", "fra")
    
    def extract_text_from_image(self, image_path: str, lang: str = None) -> Tuple[str, Dict]:
        """
        Extrait le texte d'une image
        
        Args:
            image_path: Chemin vers l'image
            lang: Code langue (fra, eng, ara, etc.)
            
        Returns:
            Tuple (texte extrait, métadonnées)
        """
        start_time = time.time()
        
        if lang is None:
            lang = self.default_language
        
        try:
            # Ouvrir l'image
            img = Image.open(image_path)
            
            # Extraction du texte avec Tesseract
            # config='--psm 3' : Automatic page segmentation (mode par défaut)
            text = pytesseract.image_to_string(
                img,
                lang=lang,
                config='--psm 3'
            )
            
            # Nettoyer le texte
            text = text.strip()
            
            # Extraire les métadonnées
            processing_time = time.time() - start_time
            word_count = len(text.split())
            char_count = len(text)
            line_count = len(text.split('\n'))
            
            metadata = {
                "word_count": word_count,
                "char_count": char_count,
                "line_count": line_count,
                "language": lang,
                "processing_time": round(processing_time, 2)
            }
            
            return text, metadata
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction OCR: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path: str, lang: str = None) -> Tuple[str, Dict]:
        """
        Extrait le texte d'un fichier PDF
        Convertit d'abord le PDF en images, puis applique l'OCR
        
        Args:
            pdf_path: Chemin vers le PDF
            lang: Code langue
            
        Returns:
            Tuple (texte extrait, métadonnées)
        """
        start_time = time.time()
        
        if lang is None:
            lang = self.default_language
        
        try:
            # Convertir le PDF en images (une image par page)
            # Peut nécessiter l'installation de poppler sur Windows
            images = convert_from_path(pdf_path, dpi=300)
            
            all_text = []
            total_words = 0
            total_chars = 0
            total_lines = 0
            
            # Extraire le texte de chaque page
            for i, image in enumerate(images):
                # Sauvegarder temporairement l'image
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                    temp_path = temp_file.name
                    image.save(temp_path, 'PNG')
                
                # Extraire le texte de cette page
                page_text = pytesseract.image_to_string(
                    Image.open(temp_path),
                    lang=lang,
                    config='--psm 3'
                )
                
                all_text.append(f"--- Page {i+1} ---\n{page_text}")
                
                # Nettoyer le fichier temporaire
                os.unlink(temp_path)
                
                # Compter les mots/chars/lignes
                total_words += len(page_text.split())
                total_chars += len(page_text)
                total_lines += len(page_text.split('\n'))
            
            # Combiner tout le texte
            full_text = "\n\n".join(all_text).strip()
            
            processing_time = time.time() - start_time
            
            metadata = {
                "word_count": total_words,
                "char_count": total_chars,
                "line_count": total_lines,
                "language": lang,
                "page_count": len(images),
                "processing_time": round(processing_time, 2)
            }
            
            return full_text, metadata
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction OCR du PDF: {str(e)}")
    
    def detect_language(self, image_path: str) -> str:
        """
        Détecte automatiquement la langue d'une image
        
        Args:
            image_path: Chemin vers l'image
            
        Returns:
            Code de langue détecté
        """
        try:
            img = Image.open(image_path)
            
            # Obtenir les informations OSD (Orientation and Script Detection)
            osd = pytesseract.image_to_osd(img)
            
            # Parser les résultats
            for line in osd.split('\n'):
                if 'Script:' in line:
                    script = line.split(':')[1].strip()
                    # Mapper le script vers un code langue
                    if 'Latin' in script:
                        return 'fra'  # ou 'eng'
                    elif 'Arabic' in script:
                        return 'ara'
            
            return self.default_language
            
        except:
            return self.default_language
    
    def get_supported_languages(self) -> list:
        """
        Retourne la liste des langues supportées par Tesseract
        
        Returns:
            Liste des codes de langues
        """
        try:
            langs = pytesseract.get_languages()
            return langs
        except:
            return ['fra', 'eng']
