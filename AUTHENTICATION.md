# 🔐 Système d'Authentification - Smart Document Manager

## 📋 Vue d'ensemble

Le système d'authentification a été ajouté pour sécuriser l'application. Chaque utilisateur doit maintenant se connecter pour accéder à la plateforme, et chaque document est associé à l'utilisateur qui l'a téléversé.

## 🏗️ Architecture

### Backend (FastAPI + JWT)

#### Modèles de base de données
- **Table `users`** : Stocke les informations des utilisateurs
  - `id` : Identifiant unique
  - `email` : Email (unique)
  - `username` : Nom d'utilisateur (unique)
  - `hashed_password` : Mot de passe hashé avec bcrypt
  - `full_name` : Nom complet (optionnel)
  - `is_active` : Statut du compte
  - `created_at` : Date de création

- **Table `documents`** : Modifiée pour inclure `user_id`
  - Chaque document est maintenant lié à un utilisateur via `user_id`
  - Relation : `User` 1→N `Document`

#### Technologies utilisées
- **passlib[bcrypt]** : Hashage sécurisé des mots de passe
- **python-jose[cryptography]** : Génération et validation des tokens JWT
- **FastAPI OAuth2PasswordBearer** : Schéma d'authentification standard

#### Routes d'authentification (`/api/auth`)
- `POST /auth/register` : Inscription d'un nouvel utilisateur
- `POST /auth/login` : Connexion (retourne un token JWT)
- `GET /auth/me` : Récupère les infos de l'utilisateur connecté
- `GET /auth/check` : Vérifie si le token est valide

#### Protection des routes
Toutes les routes de l'API nécessitent maintenant un token JWT valide :
- `/api/upload` : Upload de documents
- `/api/documents` : Liste des documents (filtrée par utilisateur)
- `/api/ocr` : Extraction OCR
- `/api/classify` : Classification ML
- `/api/stats` : Statistiques (uniquement pour les docs de l'utilisateur)

### Frontend (React)

#### Composants créés
- **Login.jsx** : Page de connexion
- **Register.jsx** : Page d'inscription
- **PrivateRoute.jsx** : Composant pour protéger les routes
- **authService.js** : Service de gestion de l'authentification

#### Fonctionnalités
- **Persistance** : Token stocké dans `localStorage`
- **Intercepteurs Axios** : Ajout automatique du token à chaque requête
- **Redirection automatique** : Si le token expire ou est invalide → redirection vers `/login`
- **Protection des routes** : Routes `/`, `/documents`, `/dashboard` nécessitent une connexion

## 🚀 Utilisation

### 1. Inscription d'un nouvel utilisateur
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "motdepasse123",
  "full_name": "John Doe"
}
```

**Réponse** :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2024-12-26T10:00:00Z"
  }
}
```

### 2. Connexion
```bash
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=motdepasse123
```

**Réponse** : Même format que l'inscription

### 3. Utilisation du token
Toutes les requêtes vers l'API doivent inclure le header :
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4. Frontend - Flux utilisateur
1. Première visite → Redirection vers `/login`
2. L'utilisateur peut choisir **Se connecter** ou **S'inscrire**
3. Après authentification → Token stocké → Redirection vers `/`
4. Navigation libre dans l'application
5. Déconnexion → Suppression du token → Redirection vers `/login`

## 🔒 Sécurité

### Mots de passe
- **Hashage** : bcrypt avec salt automatique
- **Validation** : Minimum 6 caractères (configurable)
- **Stockage** : Uniquement le hash, jamais en clair

### Tokens JWT
- **Algorithme** : HS256
- **Durée de vie** : 7 jours (configurable dans `auth_utils.py`)
- **Clé secrète** : Stockée dans `.env` (à changer en production)

### Protection
- **Routes backend** : Middleware `get_current_active_user` sur toutes les routes sensibles
- **Routes frontend** : Composant `PrivateRoute` pour protéger les pages
- **Isolation des données** : Chaque utilisateur ne voit que ses propres documents

## ⚙️ Configuration

### Variables d'environnement (`.env`)
```env
SECRET_KEY=smartdocmanager_super_secret_key_2024_change_in_production
```

**⚠️ Important** : Changez cette clé en production avec une valeur aléatoire et sécurisée.

### Génération d'une clé sécurisée
```python
import secrets
print(secrets.token_urlsafe(32))
```

## 📊 Base de données

### Migration
Lorsque vous redémarrez le backend, les tables `users` seront automatiquement créées grâce à SQLAlchemy.

### Utilisateur existant
Si vous aviez déjà des documents dans la base :
1. Créez un compte utilisateur
2. Les anciens documents sans `user_id` devront être réassignés manuellement ou supprimés

## 🧪 Tests

### Test d'inscription
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"testuser","password":"test123"}'
```

### Test de connexion
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=test123"
```

### Test d'upload avec token
```bash
TOKEN="votre_token_jwt_ici"
curl -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@document.pdf"
```

## 📝 Notes de développement

### Personnalisation
- **Durée du token** : Modifiez `ACCESS_TOKEN_EXPIRE_MINUTES` dans `auth_utils.py`
- **Validation du mot de passe** : Ajoutez des règles dans `auth.py` (longueur, complexité, etc.)
- **Champs utilisateur** : Ajoutez des colonnes dans le modèle `User` (rôle, avatar, etc.)

### Extensions possibles
- ✅ Système de rôles (admin, user)
- ✅ Réinitialisation de mot de passe par email
- ✅ OAuth2 (Google, GitHub)
- ✅ 2FA (Two-Factor Authentication)
- ✅ Logs d'activité utilisateur
- ✅ Limitation de taux (rate limiting)

## 🐛 Dépannage

### "Token expiré"
→ Reconnectez-vous pour obtenir un nouveau token

### "401 Unauthorized"
→ Vérifiez que le token est bien envoyé dans le header `Authorization`

### "Email/Username déjà utilisé"
→ Choisissez un autre email ou username

### Documents ne s'affichent pas
→ Vérifiez que l'utilisateur est bien connecté et que `user_id` est correct dans la base

## 🎓 Pour la présentation académique

Points à mettre en avant :
- ✅ **Sécurité** : Hashage bcrypt + JWT
- ✅ **Isolation des données** : Chaque utilisateur ne voit que ses documents
- ✅ **Architecture moderne** : OAuth2 + Bearer Token
- ✅ **Expérience utilisateur** : Login/Register fluide, redirection automatique
- ✅ **Production-ready** : Gestion des erreurs, validation des inputs
