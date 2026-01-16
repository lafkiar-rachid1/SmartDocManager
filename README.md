# 📄 Smart Document Manager

**Système de Gestion Intelligente des Documents avec OCR et IA**

Un projet académique full-stack complet permettant de téléverser des documents, d'extraire automatiquement le texte via OCR, et de les classifier automatiquement à l'aide de l'intelligence artificielle.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)

## 🎯 Objectifs du Projet

- Téléverser des documents scannés (PDF, images)
- Extraire automatiquement le texte via OCR (Tesseract)
- Extraire et stocker des métadonnées
- Classifier automatiquement les documents avec l'IA
- Visualiser des statistiques dans un tableau de bord
- Exporter les données en CSV/JSON

## 🛠️ Technologies Utilisées

### Backend
- **Python 3.9+**
- **FastAPI** - Framework web moderne
- **PostgreSQL** - Base de données relationnelle
- **SQLAlchemy** - ORM Python
- **Tesseract OCR** - Extraction de texte
- **OpenCV** - Traitement d'images
- **scikit-learn** - Machine Learning (TF-IDF +( Naive Bayes, Logistic Regression, SVM, Random Forest))

### Frontend
- **Streamlit 1.31** - Framework web Python pour data apps
- **Plotly Express** - Graphiques interactifs
- **Pandas** - Manipulation de données
- **Pillow** - Traitement d'images
- **Requests** - Client HTTP

## 📁 Structure du Projet

```
SmartDocManager/
├── backend/
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── database.py            # Configuration PostgreSQL
│   ├── models.py              # Modèles SQLAlchemy
│   ├── schemas.py             # Schémas Pydantic
│   ├── requirements.txt       # Dépendances Python
│   ├── .env.example          # Configuration exemple
│   │
│   ├── api/                   # Routes API REST
│   │   ├── upload.py         # Upload de documents
│   │   ├── ocr.py            # Extraction OCR
│   │   ├── classify.py       # Classification IA
│   │   └── stats.py          # Statistiques et export
│   │
│   ├── services/              # Logique métier
│   │   ├── image_processing.py   # Traitement OpenCV
│   │   ├── ocr_service.py        # Service OCR
│   │   └── ml_service.py         # Service ML
│   │
│   ├── ml/                    # Machine Learning
│   │   ├── train_model.py    # Script d'entraînement
│   │   ├── model.pkl         # Modèle entraîné
│   │   └── vectorizer.pkl    # Vectorizer TF-IDF
│   │
│   └── storage/documents/     # Fichiers uploadés
│
└── frontend/
    ├── Accueil.py            # Page d'accueil (analyse visiteur)
    ├── pages/                # Pages de l'application
    │   ├── 0_Login.py       # Page de connexion
    │   ├── 1_Register.py    # Page d'inscription
    │   ├── 2_Upload.py      # Page d'upload authentifié
    │   ├── 3_Documents.py   # Liste et gestion des documents
    │   └── 4_Dashboard.py   # Statistiques et visualisations
    │
    ├── services/             # Services backend
    │   ├── auth_service.py  # Service d'authentification
    │   └── api_service.py   # Service API REST
    │
    ├── .streamlit/
    │   └── config.toml      # Configuration Streamlit
    │
    ├── requirements.txt     # Dépendances Python
    └── README.md
```

## 🚀 Installation et Configuration

### Prérequis

1. **Python 3.9+**
2. **PostgreSQL 12+**
3. **Tesseract OCR**
   - Windows: Télécharger depuis [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-fra`
   - macOS: `brew install tesseract tesseract-lang`

### Configuration de la Base de Données

1. Créer une base de données PostgreSQL:

```sql
CREATE DATABASE smartdoc_db;
CREATE USER smartdoc_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE smartdoc_db TO smartdoc_user;
```

### Installation Backend

1. Naviguer vers le dossier backend:

```bash
cd backend
```

2. Créer un environnement virtuel:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Installer les dépendances:

```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement:

```bash
# Copier le fichier exemple
copy .env.example .env  # Windows
cp .env.example .env    # Linux/macOS

# Éditer .env avec vos configurations
```

Exemple de configuration `.env`:

```env
DATABASE_URL=postgresql://smartdoc_user:votre_mot_de_passe@localhost:5432/smartdoc_db
HOST=0.0.0.0
PORT=8000
STORAGE_PATH=./storage/documents
TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe
OCR_LANGUAGE=fra
```

5. Entraîner le modèle de Machine Learning:

```bash
python ml/train_model.py
```

Cette commande va:
- Créer les fichiers `model.pkl` et `vectorizer.pkl`
- Afficher les métriques de performance
- Tester quelques prédictions

6. Lancer le serveur backend:

```bash
python main.py
```

Le serveur démarre sur `http://localhost:8000`

Documentation API disponible sur:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Installation Frontend Streamlit

1. Naviguer vers le dossier frontend:

```bash
cd frontend
```

2. Installer les dépendances:

```bash
pip install -r requirements.txt
```

3. Lancer l'application Streamlit:

```bash
streamlit run Accueil.py
```

L'application démarre sur `http://localhost:8501`

## 📖 Utilisation

### 1. Mode Visiteur (Page d'Accueil)

1. Ouvrir l'application sur `http://localhost:8501`
2. Téléverser un document (analyse sans sauvegarde)
3. Voir la catégorie détectée et le niveau de confiance
4. **Note**: Les documents ne sont pas sauvegardés en mode visiteur

### 2. Connexion / Inscription

1. Cliquer sur "🔐 Connexion" ou "✨ Créer un compte"
2. Créer un compte avec username, email et mot de passe
3. Se connecter pour accéder aux fonctionnalités complètes

### 3. Upload de Documents (Authentifié)

1. Accéder à la page Upload (📤)
2. Glisser-déposer un fichier ou cliquer pour sélectionner
3. Cliquer sur "🚀 Lancer l'analyse"
4. Le système effectue automatiquement:
   - Upload du fichier
   - Extraction OCR du texte
   - Classification par IA
5. Voir les résultats détaillés (catégorie, confiance, texte extrait)

### 4. Gestion des Documents

1. Accéder à la page Documents (📁)
2. Visualiser tous vos documents sauvegardés
3. Utiliser les filtres:
   - Recherche par nom de fichier
   - Filtrer par catégorie
   - Filtrer par type de fichier
4. Cliquer sur "👁️ Voir" pour les détails complets
5. Supprimer des documents avec confirmation

### 5. Tableau de Bord

1. Accéder au Dashboard (📊)
2. Visualiser les statistiques globales:
   - Nombre total de documents
   - Documents des 7 derniers jours
   - Confiance moyenne de classification
   - Nombre de catégories uniques
3. Voir les graphiques interactifs (Plotly):
   - Distribution par catégorie (Camembert)
   - Documents par catégorie (Barres)
   - Tableau récapitulatif des catégories

## 🤖 Classification IA

Le système utilise un modèle de Machine Learning pour classifier automatiquement les documents en 5 catégories:

1. **Facture** - Factures, devis, bons de commande
2. **CV** - Curriculum Vitae, profils professionnels
3. **Contrat** - Contrats de travail, conventions, accords
4. **Lettre** - Lettres de motivation, correspondance
5. **Autre** - Documents non classifiés

### Algorithme

Le système effectue une **comparaison automatique de plusieurs algorithmes** et sélectionne le meilleur :

**Vectorisation :**
- **TF-IDF** (Term Frequency-Inverse Document Frequency)
  - N-grams : 1-3 (unigrammes, bigrammes, trigrammes)
  - Max features : 5000
  - Échelle logarithmique sublinear_tf

**Algorithmes de Classification Testés :**
1. **Naive Bayes Multinomial** - Rapide, performant pour le texte
2. **Logistic Regression** - Robuste, bonne généralisation
3. **Support Vector Machine (Linear)** - Excellent pour les espaces de haute dimension
4. **Random Forest** - Ensemble learning, résiste bien à l'overfitting

**Métriques d'Évaluation :**
- Précision Train et Test
- Cross-validation 5-fold
- Détection automatique d'overfitting
- Courbes ROC et AUC
- Rapport de classification complet

Le meilleur modèle est automatiquement sélectionné et sauvegardé.

### Performance

Le modèle est entraîné sur des exemples en français avec validation rigoureuse :
- **Précision globale** : ~85-95%
- **Cross-validation** : ±2-5% de stabilité
- **Détection d'overfitting** : Surveillance de l'écart Train-Test
- **Graphiques ROC** : Génération automatique pour analyse visuelle
- Les catégories avec vocabulaire distinctif ont une meilleure performance

## 📊 API REST

### Endpoints Principaux

#### Upload
- `POST /api/upload` - Téléverser un document
- `GET /api/documents` - Liste des documents
- `GET /api/documents/{id}` - Détails d'un document
- `DELETE /api/documents/{id}` - Supprimer un document

#### OCR
- `POST /api/ocr` - Effectuer l'OCR
- `GET /api/ocr/languages` - Langues supportées

#### Classification
- `POST /api/classify` - Classifier un document
- `POST /api/classify/batch` - Classifier plusieurs documents
- `GET /api/classify/categories` - Liste des catégories

#### Statistiques
- `GET /api/stats` - Statistiques globales
- `GET /api/stats/categories` - Stats par catégorie
- `GET /api/stats/timeline` - Évolution temporelle
- `GET /api/export/csv` - Export CSV
- `GET /api/export/json` - Export JSON

## 🔧 Configuration Avancée

### Améliorer l'OCR

Pour de meilleurs résultats OCR:

1. Installer des packs de langues supplémentaires:
```bash
# Windows: Télécharger depuis GitHub Tesseract
# Linux
sudo apt-get install tesseract-ocr-eng tesseract-ocr-ara
```

2. Modifier `OCR_LANGUAGE` dans `.env`:
```env
OCR_LANGUAGE=fra+eng  # Français + Anglais
```

### Entraîner un Meilleur Modèle

1. Ajouter plus d'exemples dans `backend/ml/train_model.py`
2. Modifier les paramètres du modèle
3. Réentraîner: `python ml/train_model.py`

### Ajuster le Traitement d'Images

Modifier les paramètres dans `backend/services/image_processing.py`:
- Taille de blur
- Seuils de binarisation
- Résolution maximale

## 🐛 Dépannage

### Erreurs Communes

**1. Tesseract non trouvé**
```
Error: Tesseract not found
```
Solution: Installer Tesseract et configurer `TESSERACT_CMD` dans `.env`

**2. Connexion PostgreSQL échouée**
```
Error: Connection refused
```
Solution: Vérifier que PostgreSQL est démarré et que `DATABASE_URL` est correct

**3. Module non trouvé**
```
ModuleNotFoundError: No module named 'X'
```
Solution: Réinstaller les dépendances `pip install -r requirements.txt`

**4. Erreur de connexion API**
```
Error: Connection refused to http://localhost:8000
```
Solution: Vérifier que le backend FastAPI est démarré sur le port 8000

**5. Streamlit ne démarre pas**
```
Streamlit command not found
```
Solution: Installer Streamlit `pip install streamlit` et vérifier que l'environnement virtuel est activé

🚀 **Bon développement !**
