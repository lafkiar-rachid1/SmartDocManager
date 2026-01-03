# SmartDocManager - Frontend Streamlit

Frontend développé avec Streamlit (bibliothèque Python) reproduisant toutes les fonctionnalités du frontend React.

## 📋 Fonctionnalités

✅ **Page d'accueil publique** - Analyse de documents sans inscription (mode visiteur)
✅ **Authentification** - Login/Register avec JWT
✅ **Upload de documents** - Avec progression visuelle et classification IA
✅ **Liste des documents** - Filtres et suppression
✅ **Dashboard** - Statistiques et graphiques avec Plotly
✅ **Design moderne** - Interface professionnelle avec CSS personnalisé

## 🚀 Installation

1. **Créer un environnement virtuel Python**
```bash
cd frontendStreamlit
python -m venv venv
```

2. **Activer l'environnement virtuel**
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## ▶️ Lancement

**Assurez-vous que le backend FastAPI est démarré** sur http://localhost:8000

Puis lancez Streamlit:
```bash
streamlit run Accueil.py
```

L'application sera accessible sur: **http://localhost:8501**

## 📁 Structure

```
frontendStreamlit/
├── Accueil.py              # Page d'accueil publique (point d'entrée)
├── requirements.txt         # Dépendances Python
├── .streamlit/
│   └── config.toml         # Configuration Streamlit
├── services/
│   ├── auth_service.py     # Service d'authentification JWT
│   └── api_service.py      # Service API pour backend
└── pages/
    ├── 0_🔐_Login.py       # Page de connexion
    ├── 1_✨_Register.py    # Page d'inscription
    ├── 2_📤_Upload.py      # Page d'upload (protégée)
    ├── 3_📁_Documents.py   # Liste des documents (protégée)
    └── 4_📊_Dashboard.py   # Statistiques (protégée)
```

## 🎨 Pages disponibles

### Pages publiques
- **Accueil** (`/`) - Analyse sans inscription
- **Login** - Connexion
- **Register** - Inscription

### Pages protégées (nécessitent connexion)
- **Upload** - Téléverser et analyser des documents
- **Documents** - Gérer vos documents
- **Dashboard** - Voir les statistiques

## ⚙️ Configuration

Le fichier `.streamlit/config.toml` configure:
- Thème (couleurs, fonts)
- Port du serveur (8501)
- Taille max d'upload (10 MB)

## 🔗 API Backend

Toutes les requêtes sont envoyées vers: `http://localhost:8000/api/`

Endpoints utilisés:
- `/login` - Authentification
- `/register` - Inscription
- `/upload` - Upload document (authentifié)
- `/analyze-guest` - Analyse sans auth
- `/documents` - Liste documents
- `/statistics` - Statistiques
- `/category-stats` - Stats par catégorie

## 📝 Notes

- Les sessions utilisateur sont gérées via `st.session_state`
- Les tokens JWT sont stockés dans la session
- Le mode visiteur ne sauvegarde pas les documents
- Design responsive avec CSS personnalisé
- Icônes emojis pour simplicité

## 🐛 Dépannage

**Erreur de connexion au backend:**
- Vérifiez que le backend est démarré sur http://localhost:8000
- Vérifiez les paramètres CORS dans le backend

**Erreur d'import:**
- Assurez-vous que toutes les dépendances sont installées: `pip install -r requirements.txt`

**Port déjà utilisé:**
- Modifiez le port dans `.streamlit/config.toml`
- Ou lancez avec: `streamlit run Accueil.py --server.port 8502`
