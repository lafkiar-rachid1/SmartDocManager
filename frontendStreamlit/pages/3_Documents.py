"""
Page Documents - Liste et gestion des documents
Affiche tous les documents avec filtres et possibilité de suppression
"""

import streamlit as st
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.auth_service import AuthService
from services.api_service import APIService

# Configuration de la page
st.set_page_config(
    page_title="Documents - SmartDocManager",
    page_icon="📁",
    layout="wide"
)

# CSS personnalisé - Mode Sombre
st.markdown("""
<style>
    /* Fond principal SOMBRE */
    .stApp {
        background-color: #0F172A !important;
    }
    
    .main {
        background-color: #0F172A !important;
    }
    
    /* Cartes de documents - Redesign */
    .doc-card {
        background: linear-gradient(160deg, #2D3748 0%, #1E293B 100%);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
        margin: 0; /* Let streamlit grid handle gap */
        height: 100%;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        position: relative;
    }
    
    .doc-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: radial-gradient(circle at top right, rgba(139, 92, 246, 0.1), transparent 50%);
        pointer-events: none;
    }
    
    .doc-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
        border-color: rgba(139, 92, 246, 0.6);
        background: linear-gradient(160deg, #334155 0%, #243045 100%);
        z-index: 10;
    }
    
    /* En-tête plus subtil */
    .card-header {
        height: 120px;
        background: rgba(15, 23, 42, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        position: relative;
        backdrop-filter: blur(5px);
    }
    
    /* Indicateur de couleur en haut selon le type */
    .card-header::after {
        content: '';
        position: absolute;
        bottom: 0px;
        left: 20%;
        right: 20%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.8), transparent);
        box-shadow: 0 -2px 10px rgba(139, 92, 246, 0.5);
        top: auto;
    }
    
    .card-header.pdf::after { background: linear-gradient(90deg, #EF4444, #F87171); }
    .card-header.image::after { background: linear-gradient(90deg, #3B82F6, #60A5FA); }
    
    .card-body {
        padding: 1.5rem;
        background-color: transparent;
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    /* Titre structuré */
    .doc-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F1F5F9; /* Slate 100 */
        text-align: center;
        line-height: 1.4;
        margin: 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Badges unifiés */
    .badge-container {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.75rem;
        background-color: #334155; /* Fond neutre sombre */
        color: #E2E8F0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .badge-category { background-color: rgba(139, 92, 246, 0.2); color: #A78BFA; border-color: rgba(139, 92, 246, 0.3); }
    .badge-type { background-color: rgba(59, 130, 246, 0.2); color: #60A5FA; border-color: rgba(59, 130, 246, 0.3); }
    
    /* Confiance */
    .confidence-pill {
        background-color: rgba(15, 23, 42, 0.5);
        border-radius: 0.5rem;
        padding: 0.5rem;
        text-align: center;
        margin-top: auto; /* Pousser vers le bas */
    }
    
    /* Aperçu du texte encadré */
    .text-preview {
        background-color: rgba(15, 23, 42, 0.5);
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin: 0;
        color: #94A3B8;
        font-size: 0.85rem;
        font-style: italic;
        line-height: 1.6;
    }
    
    .text-preview-title {
        color: #8B5CF6;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Date discrète */
    .doc-date {
        text-align: center;
        color: #64748b;
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }
    
    /* Boutons */
    .stButton button {
        border-radius: 1rem !important;
        font-weight: 700 !important;
        transition: all 0.3s !important;
        border: none !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Vérifier l'authentification
if not AuthService.is_authenticated():
    st.warning("⚠️ Vous devez être connecté pour accéder à cette page")
    st.info("👉 Veuillez vous connecter pour voir vos documents")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔐 Se connecter", use_container_width=True, type="primary"):
            st.switch_page("pages/0_Login.py")
    st.stop()

# Initialiser session state
if 'documents' not in st.session_state:
    st.session_state.documents = None
if 'selected_document' not in st.session_state:
    st.session_state.selected_document = None
if 'filter_category' not in st.session_state:
    st.session_state.filter_category = 'all'
if 'filter_type' not in st.session_state:
    st.session_state.filter_type = 'all'
if 'search_term' not in st.session_state:
    st.session_state.search_term = ''
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = 0
if 'current_page' not in st.session_state:
    st.session_state.current_page = None

# Nettoyer le selected_document quand on arrive sur la page depuis une autre page
if st.session_state.current_page != '3_Documents':
    st.session_state.selected_document = None
    st.session_state.current_page = '3_Documents'

# Fonction pour charger les documents avec cache
@st.cache_data(ttl=60, show_spinner=False)  # Cache de 60 secondes
def fetch_documents_cached(_auth_headers):
    """Charger les documents depuis l'API avec cache"""
    result = APIService.get_documents()
    if result["success"]:
        return result["data"]
    return None

# Fonction pour charger les documents
def load_documents(force_refresh=False):
    """Charger les documents depuis l'API"""
    with st.spinner("🔄 Chargement des documents..."):
        if force_refresh:
            # Forcer le rafraîchissement en changeant le timestamp
            st.session_state.last_refresh = st.session_state.last_refresh + 1
            st.cache_data.clear()
        
        headers = AuthService.get_headers()
        # Utiliser le cache avec un timestamp pour forcer le refresh si besoin
        docs = fetch_documents_cached(str(headers) + str(st.session_state.last_refresh))
        
        if docs is not None:
            st.session_state.documents = docs
            return True
        else:
            st.error("❌ Erreur lors du chargement des documents")
            return False

# Fonction pour filtrer les documents
def filter_documents():
    """Appliquer les filtres aux documents"""
    if not st.session_state.documents:
        return []
    
    filtered = st.session_state.documents.copy()
    
    # Filtrer par catégorie
    if st.session_state.filter_category != 'all':
        filtered = [doc for doc in filtered if doc.get('category') == st.session_state.filter_category]
    
    # Filtrer par type
    if st.session_state.filter_type != 'all':
        filtered = [doc for doc in filtered if doc.get('file_type') == st.session_state.filter_type]
    
    # Recherche par nom de fichier
    if st.session_state.search_term:
        search_lower = st.session_state.search_term.lower()
        filtered = [doc for doc in filtered if search_lower in doc.get('filename', '').lower()]
    
    return filtered

# Fonction pour supprimer un document
def delete_document(document_id):
    """Supprimer un document"""
    result = APIService.delete_document(document_id)
    if result["success"]:
        st.success("✅ Document supprimé avec succès!")
        st.session_state.selected_document = None
        # Forcer le refresh du cache
        load_documents(force_refresh=True)
        st.rerun()
    else:
        st.error(f"❌ {result['error']}")

# Charger les documents au premier chargement
if st.session_state.documents is None:
    load_documents()

# En-tête moderne et simple
st.markdown("""
<div style='text-align: center; margin-bottom: 3rem; padding: 2rem 0;'>
    <h1 class='page-title'>
        📁 Mes Documents
    </h1>
    <p class='page-subtitle'>
        Gérez vos documents avec style ✨
    </p>
</div>
""", unsafe_allow_html=True)

filtered_docs = filter_documents()

# Stats et bouton d'actualisation
col_stat, col_btn = st.columns([4, 1])
with col_stat:
    st.markdown(f"""
    <div class='stats-card' style='background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%); border: none; padding: 2rem;'>
        <div style='display: flex; align-items: center; justify-content: space-between;'>
            <div style='display: flex; align-items: center; gap: 2rem;'>
                <div style='font-size: 5rem; filter: drop-shadow(0 5px 10px rgba(0,0,0,0.2));'>📊</div>
                <div style='text-align: left;'>
                    <div style='font-size: 3.5rem; font-weight: 900; color: white; line-height: 1; margin-bottom: 0.5rem;'>{len(filtered_docs)}</div>
                    <div style='font-size: 1.3rem; color: rgba(255,255,255,0.95); font-weight: 700;'>Document(s) trouvé(s)</div>
                </div>
            </div>
            <div style='font-size: 6rem; opacity: 0.1; color: white;'>📁</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Actualiser", use_container_width=True, type="primary"):
        load_documents(force_refresh=True)
        st.rerun()

# Section des filtres
st.markdown("""
<h2 class='section-title'>🔍 Filtres de Recherche</h2>
""", unsafe_allow_html=True)



col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("**🔎 Rechercher**")
    search = st.text_input(
        "Rechercher",
        value=st.session_state.search_term,
        placeholder="Nom du fichier...",
        label_visibility="collapsed",
        key="search_input"
    )
    if search != st.session_state.search_term:
        st.session_state.search_term = search

with col2:
    st.markdown("**📂 Catégorie**")
    # Obtenir les catégories uniques
    categories = ['all']
    if st.session_state.documents:
        categories.extend(sorted(set(doc.get('category', '') for doc in st.session_state.documents if doc.get('category'))))
    
    category = st.selectbox(
        "Catégorie",
        options=categories,
        format_func=lambda x: 'Toutes' if x == 'all' else x,
        index=categories.index(st.session_state.filter_category) if st.session_state.filter_category in categories else 0,
        label_visibility="collapsed",
        key="category_select"
    )
    if category != st.session_state.filter_category:
        st.session_state.filter_category = category

with col3:
    st.markdown("**📄 Type de fichier**")
    # Obtenir les types uniques
    file_types = ['all']
    if st.session_state.documents:
        file_types.extend(sorted(set(doc.get('file_type', '') for doc in st.session_state.documents if doc.get('file_type'))))
    
    file_type = st.selectbox(
        "Type",
        options=file_types,
        format_func=lambda x: 'Tous' if x == 'all' else x,
        index=file_types.index(st.session_state.filter_type) if st.session_state.filter_type in file_types else 0,
        label_visibility="collapsed",
        key="type_select"
    )
    if file_type != st.session_state.filter_type:
        st.session_state.filter_type = file_type



# Liste des documents
if not st.session_state.documents:
    st.info("📭 Aucun document trouvé. Uploadez votre premier document!")
    if st.button("📤 Aller à l'upload", type="primary"):
        st.switch_page("pages/2_Upload.py")
else:
    filtered_docs = filter_documents()
    
    if len(filtered_docs) == 0:
        st.warning("🔍 Aucun document ne correspond aux critères de recherche")
        st.info("💡 Essayez de modifier vos filtres")
    else:
        # Afficher les documents en grille (3 colonnes)
        cols_per_row = 3
        for i in range(0, len(filtered_docs), cols_per_row):
            cols = st.columns(cols_per_row, gap="large")
            # Ajouter un espacement vertical entre les rangées
            if i > 0:
                st.markdown("<div style='margin: 4rem 0;'></div>", unsafe_allow_html=True)
            for j in range(cols_per_row):
                if i + j < len(filtered_docs):
                    doc = filtered_docs[i + j]
                    with cols[j]:
                        # Carte de document avec design WOW
                        st.markdown('<div class="doc-card">', unsafe_allow_html=True)
                        
                        # En-tête avec icône (pas de chargement d'image pour la performance)
                        file_type = doc.get('file_type', 'UNKNOWN')
                        if file_type == 'IMAGE':
                            # Afficher uniquement l'icône pour la performance
                            # L'image complète sera chargée dans les détails
                            st.markdown("""
                            <div class='card-header image'>
                                <div style='font-size: 3.5rem;'>🖼️</div>
                            </div>
                            """, unsafe_allow_html=True)
                        elif file_type == 'PDF':
                            st.markdown("""
                            <div class='card-header pdf'>
                                <div style='font-size: 3.5rem;'>📕</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class='card-header'>
                                <div style='font-size: 3.5rem;'>📄</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Corps de la carte
                        st.markdown('<div class="card-body">', unsafe_allow_html=True)
                        
                        # Titre du document
                        filename = doc.get('filename', 'Sans nom')
                        display_name = filename[:35] + '...' if len(filename) > 35 else filename
                        st.markdown(f"""
                        <div class='doc-title'>{display_name}</div>
                        """, unsafe_allow_html=True)
                        
                        # Badges
                        st.markdown('<div class="badge-container">', unsafe_allow_html=True)
                        
                        # Badge catégorie
                        if doc.get('category'):
                            st.markdown(f"""
                            <span class='badge badge-category'>
                                <span>📁</span>
                                <span>{doc['category']}</span>
                            </span>
                            """, unsafe_allow_html=True)
                        
                        # Badge type
                        if file_type:
                            type_icon = "�" if file_type == "PDF" else "🖼️" if file_type == "IMAGE" else "📄"
                            st.markdown(f"""
                            <span class='badge badge-type'>
                                <span>{type_icon}</span>
                                <span>{file_type}</span>
                            </span>
                            """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Badge confiance
                        if doc.get('confidence') is not None:
                            confidence = doc['confidence'] * 100
                            if confidence >= 80:
                                badge_class = "badge-confidence-high"
                            elif confidence >= 60:
                                badge_class = "badge-confidence-medium"
                            else:
                                badge_class = "badge-confidence-low"
                            
                            st.markdown(f"""
                            <div style='text-align: center; margin: 1rem 0;'>
                                <span class='badge {badge_class}'>
                                    <span>⭐</span>
                                    <span>Confiance: {confidence:.1f}%</span>
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Date
                        if doc.get('created_at'):
                            from datetime import datetime
                            try:
                                date_obj = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
                                date_str = date_obj.strftime('%d/%m/%Y %H:%M')
                                st.markdown(f"""
                                <div class='doc-date'>
                                    📅 {date_str}
                                </div>
                                """, unsafe_allow_html=True)
                            except:
                                pass
                        
                        # Aperçu du texte
                        if doc.get('extracted_text'):
                            preview = doc['extracted_text'][:120].strip()
                            if len(doc['extracted_text']) > 120:
                                preview += "..."
                            st.markdown(f"""
                            <div class='text-preview'>
                                <div class='text-preview-title'>
                                    <span>📝</span>
                                    <span>Aperçu:</span>
                                </div>
                                <div>"{preview}"</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)  # Fin card-body
                        
                        # Boutons d'action avec design moderne
                        st.markdown("<div style='padding: 0 1rem 1rem 1rem;'>", unsafe_allow_html=True)
                        col_btn1, col_btn2 = st.columns(2, gap="small")
                        with col_btn1:
                            if st.button("👁️ Détails", key=f"view_{doc['id']}", use_container_width=True, type="primary"):
                                st.session_state.selected_document = doc
                                st.rerun()
                        with col_btn2:
                            if st.button("🗑️ Supprimer", key=f"delete_{doc['id']}", use_container_width=True):
                                if st.session_state.get(f'confirm_delete_{doc["id"]}'):
                                    delete_document(doc['id'])
                                else:
                                    st.session_state[f'confirm_delete_{doc["id"]}'] = True
                                    st.rerun()
                        
                        # Confirmation de suppression
                        if st.session_state.get(f'confirm_delete_{doc["id"]}'):
                            st.warning("⚠️ Êtes-vous sûr ?")
                            col_conf1, col_conf2 = st.columns(2)
                            with col_conf1:
                                if st.button("✅ Oui", key=f"yes_{doc['id']}", use_container_width=True):
                                    delete_document(doc['id'])
                            with col_conf2:
                                if st.button("❌ Non", key=f"no_{doc['id']}", use_container_width=True):
                                    del st.session_state[f'confirm_delete_{doc["id"]}']
                                    st.rerun()
                        
                        st.markdown('</div></div>', unsafe_allow_html=True)  # Fin padding + doc-card

# Modal de détails du document
if st.session_state.selected_document:
    doc = st.session_state.selected_document
    
    @st.dialog("📄 Détails du Document", width="large")
    def show_document_details():
        # Afficher l'image si c'est un fichier IMAGE
        if doc.get('file_type') == 'IMAGE':
            st.markdown("### 🖼️ Aperçu de l'image")
            try:
                import requests
                from PIL import Image
                from io import BytesIO
                
                headers = AuthService.get_headers()
                response = requests.get(
                    f"http://localhost:8000/api/documents/{doc['id']}/image",
                    headers=headers
                )
                
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    st.image(image, use_container_width=True)
                else:
                    st.warning("⚠️ Impossible de charger l'image")
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Badges en haut
        file_type = doc.get('file_type', 'N/A')
        category = doc.get('category', '')
        
        # Utiliser st.columns pour les badges au lieu de HTML pour éviter les problèmes d'affichage
        st.markdown("---")
        
        cols_badges = st.columns([1, 1, 1, 1])
        
        # Badge type de fichier
        with cols_badges[0]:
            if file_type == 'PDF':
                st.markdown("""
                <div style='background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: white; padding: 0.75rem 1rem; border-radius: 1.5rem; font-weight: 700; text-align: center; box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);'>
                    <div style='font-size: 1.8rem;'>📄</div>
                    <div style='font-size: 0.85rem; margin-top: 0.25rem;'>PDF</div>
                </div>
                """, unsafe_allow_html=True)
            elif file_type == 'IMAGE':
                st.markdown("""
                <div style='background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: white; padding: 0.75rem 1rem; border-radius: 1.5rem; font-weight: 700; text-align: center; box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);'>
                    <div style='font-size: 1.8rem;'>🖼️</div>
                    <div style='font-size: 0.85rem; margin-top: 0.25rem;'>IMAGE</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: white; padding: 0.75rem 1rem; border-radius: 1.5rem; font-weight: 700; text-align: center; box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);'>
                    <div style='font-size: 1.8rem;'>📄</div>
                    <div style='font-size: 0.85rem; margin-top: 0.25rem;'>{file_type}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Badge catégorie
        with cols_badges[1]:
            if category:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.75rem 1rem; border-radius: 1.5rem; font-weight: 700; text-align: center; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);'>
                    <div style='font-size: 1.8rem;'>📁</div>
                    <div style='font-size: 0.85rem; margin-top: 0.25rem;'>{category}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Badge confiance
        with cols_badges[2]:
            if doc.get('confidence') is not None:
                confidence_value = doc.get('confidence') * 100
                if confidence_value >= 80:
                    conf_bg = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
                elif confidence_value >= 60:
                    conf_bg = "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"
                else:
                    conf_bg = "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
                
                st.markdown(f"""
                <div style='background: {conf_bg}; color: white; padding: 0.75rem 1rem; border-radius: 1.5rem; font-weight: 700; text-align: center; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);'>
                    <div style='font-size: 1.8rem;'>⭐</div>
                    <div style='font-size: 0.85rem; margin-top: 0.25rem;'>{confidence_value:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Badge date
        with cols_badges[3]:
            if doc.get('created_at'):
                from datetime import datetime
                try:
                    date_obj = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
                    date_str = date_obj.strftime('%d/%m/%Y')
                    time_str = date_obj.strftime('%H:%M')
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #64748b 0%, #475569 100%); color: white; padding: 0.75rem 1rem; border-radius: 1.5rem; font-weight: 700; text-align: center; box-shadow: 0 4px 10px rgba(100, 116, 139, 0.3);'>
                        <div style='font-size: 1.8rem;'>📅</div>
                        <div style='font-size: 0.7rem; margin-top: 0.25rem;'>{date_str}<br>{time_str}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    pass
        
        st.markdown("---")
        
        # Informations détaillées
        st.markdown("### 📋 Informations")
        
        st.markdown(f"""
        <div style='background-color: #1E293B; padding: 1.5rem; border-radius: 1rem; border: 2px solid #334155; margin-bottom: 1rem;'>
            <div style='margin-bottom: 1rem;'>
                <span style='color: #94A3B8; font-weight: 600; font-size: 0.9rem;'>📎 NOM DU FICHIER</span>
                <p style='color: #F1F5F9; font-weight: 700; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>{doc.get('filename', 'N/A')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métadonnées
        if doc.get('metadata') and len(doc['metadata']) > 0:
            st.markdown("### 📊 Métadonnées")
            col5, col6 = st.columns(2)
            
            metadata = doc['metadata'][0]
            with col5:
                st.metric("📝 Nombre de mots", metadata.get('word_count', 0))
            with col6:
                st.metric("🌐 Langue", metadata.get('language', 'N/A'))
        
        # Texte extrait
        if doc.get('extracted_text'):
            st.markdown("### 📄 Texte extrait")
            
            text = doc['extracted_text']
            word_count = len(text.split())
            char_count = len(text)
            
            # Stats du texte
            st.markdown(f"""
            <div style='display: flex; gap: 1rem; margin-bottom: 1rem;'>
                <div style='background-color: #8B5CF6; color: white; padding: 1rem 1.5rem; border-radius: 0.75rem; flex: 1; text-align: center; box-shadow: 0 4px 10px rgba(139, 92, 246, 0.2);'>
                    <div style='font-size: 2rem; font-weight: 900;'>{word_count}</div>
                    <div style='font-size: 0.9rem; opacity: 0.95;'>📝 Mots</div>
                </div>
                <div style='background-color: #10B981; color: white; padding: 1rem 1.5rem; border-radius: 0.75rem; flex: 1; text-align: center; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2);'>
                    <div style='font-size: 2rem; font-weight: 900;'>{char_count}</div>
                    <div style='font-size: 0.9rem; opacity: 0.95;'>🔤 Caractères</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Affichage du texte avec formatage amélioré
            st.markdown(f"""
            <div style='background-color: #1E293B; padding: 1.5rem; border-radius: 1rem; border: 2px solid #334155; margin-bottom: 1.5rem;'>
                <div style='color: #8B5CF6; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;'>
                    <span style='font-size: 1.2rem;'>📝</span>
                    <span>Aperçu:</span>
                </div>
                <div style='color: #CBD5E1; line-height: 1.8; font-size: 0.95rem;'>
                    {text[:500]}{'...' if len(text) > 500 else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("👁️ Voir le texte complet", expanded=False):
                st.markdown(f"""
                <div style='background: #ffffff; padding: 1.5rem; border-radius: 0.75rem; border: 2px solid #e2e8f0;'>
                    <pre style='white-space: pre-wrap; word-wrap: break-word; font-family: "Segoe UI", sans-serif; margin: 0; color: #1e293b; line-height: 1.8;'>{text}</pre>
                </div>
                """, unsafe_allow_html=True)
        
        # Boutons d'action
        st.markdown("<br>", unsafe_allow_html=True)
        col_action1, col_action2 = st.columns(2)
        
        with col_action1:
            if st.button("❌ Fermer", use_container_width=True):
                st.session_state.selected_document = None
                st.rerun()
        
        with col_action2:
            if st.button("🗑️ Supprimer ce document", use_container_width=True, type="primary"):
                delete_document(doc['id'])
    
    show_document_details()
