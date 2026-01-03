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

# CSS personnalisé - Design moderne sur fond blanc
st.markdown("""
<style>
    /* Fond principal BLANC */
    .stApp {
        background-color: #f8fafc !important;
    }
    
    .main {
        background-color: #f8fafc !important;
    }
    
    /* Cartes de documents */
    .doc-card {
        background-color: #ffffff;
        padding: 0;
        border-radius: 1rem;
        border: 2px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        overflow: hidden;
    }
    
    .doc-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    /* En-tête de carte */
    .card-header {
        height: 200px;
        background: #667eea;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 3px solid #5a67d8;
    }
    
    .card-header.pdf {
        background: #f43f5e;
        border-bottom-color: #e11d48;
    }
    
    .card-header.image {
        background: #10b981;
        border-bottom-color: #059669;
    }
    
    .card-body {
        padding: 1.5rem;
        background-color: #ffffff;
    }
    
    /* Filtres */
    .filter-section {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 1rem;
        border: 2px solid #e2e8f0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
    }
    
    /* Badges */
    .badge-container {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 1.5rem;
        font-weight: 700;
        font-size: 0.85rem;
        transition: all 0.3s;
    }
    
    .badge:hover {
        transform: translateY(-2px);
    }
    
    .badge-category {
        background-color: #667eea;
        color: white;
    }
    
    .badge-type {
        background-color: #f43f5e;
        color: white;
    }
    
    .badge-confidence-high {
        background-color: #10b981;
        color: white;
    }
    
    .badge-confidence-medium {
        background-color: #f59e0b;
        color: white;
    }
    
    .badge-confidence-low {
        background-color: #ef4444;
        color: white;
    }
    
    /* Aperçu du texte */
    .text-preview {
        background-color: #f1f5f9;
        padding: 1rem;
        border-radius: 0.75rem;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #334155;
        font-size: 0.9rem;
        font-style: italic;
        line-height: 1.6;
    }
    
    .text-preview-title {
        color: #667eea;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Titre de document */
    .doc-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #1e293b;
        margin: 1rem 0;
        text-align: center;
        line-height: 1.4;
    }
    
    .doc-date {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    
    /* Stats card */
    .stats-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 2px solid #667eea;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
    }
    
    .stats-number {
        font-size: 3rem;
        font-weight: 900;
        color: #667eea;
    }
    
    .stats-label {
        font-size: 1.1rem;
        color: #1e293b;
        font-weight: 700;
    }
    
    /* Titres */
    .page-title {
        font-size: 4rem;
        font-weight: 900;
        color: #667eea;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(102, 126, 234, 0.2);
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        color: #475569;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Info box dans modal */
    .info-box {
        background-color: #f8fafc;
        padding: 1.25rem;
        border-radius: 0.75rem;
        border: 2px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .info-box-label {
        color: #667eea;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .info-box-value {
        color: #1e293b;
        font-weight: 700;
        font-size: 1.1rem;
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
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
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

# Fonction pour charger les documents
def load_documents():
    """Charger les documents depuis l'API"""
    with st.spinner("🔄 Chargement des documents..."):
        result = APIService.get_documents()
        if result["success"]:
            st.session_state.documents = result["data"]
            return True
        else:
            st.error(f"❌ {result['error']}")
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
        load_documents()
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
    <div class='stats-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; padding: 2rem;'>
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
        load_documents()
        st.rerun()

# Section des filtres
st.markdown("""
<h2 class='section-title'>🔍 Filtres de Recherche</h2>
""", unsafe_allow_html=True)

st.markdown('<div class="filter-section">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("**🔎 Rechercher**")
    search = st.text_input(
        "Rechercher",
        value=st.session_state.search_term,
        placeholder="Nom du fichier...",
        label_visibility="collapsed"
    )
    if search != st.session_state.search_term:
        st.session_state.search_term = search
        st.rerun()

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
        label_visibility="collapsed"
    )
    if category != st.session_state.filter_category:
        st.session_state.filter_category = category
        st.rerun()

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
        label_visibility="collapsed"
    )
    if file_type != st.session_state.filter_type:
        st.session_state.filter_type = file_type
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

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
            for j in range(cols_per_row):
                if i + j < len(filtered_docs):
                    doc = filtered_docs[i + j]
                    with cols[j]:
                        # Carte de document avec design WOW
                        st.markdown('<div class="doc-card">', unsafe_allow_html=True)
                        
                        # En-tête avec aperçu image ou icône
                        file_type = doc.get('file_type', 'UNKNOWN')
                        if file_type == 'IMAGE':
                            # Essayer d'afficher l'image
                            try:
                                import requests
                                from PIL import Image
                                from io import BytesIO
                                import base64
                                
                                headers = AuthService.get_headers()
                                response = requests.get(
                                    f"http://localhost:8000/api/documents/{doc['id']}/image",
                                    headers=headers
                                )
                                
                                if response.status_code == 200:
                                    image = Image.open(BytesIO(response.content))
                                    # Redimensionner pour l'aperçu
                                    image.thumbnail((400, 200))
                                    buffered = BytesIO()
                                    image.save(buffered, format="PNG")
                                    img_str = base64.b64encode(buffered.getvalue()).decode()
                                    
                                    st.markdown(f"""
                                    <div class='card-header image' style='padding: 0;'>
                                        <img src='data:image/png;base64,{img_str}' style='width: 100%; height: 100%; object-fit: cover;'>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown("""
                                    <div class='card-header image'>
                                        <div style='font-size: 5rem;'>🖼️</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            except:
                                st.markdown("""
                                <div class='card-header image'>
                                    <div style='font-size: 5rem;'>🖼️</div>
                                </div>
                                """, unsafe_allow_html=True)
                        elif file_type == 'PDF':
                            st.markdown("""
                            <div class='card-header pdf'>
                                <div style='font-size: 5rem;'>📕</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class='card-header'>
                                <div style='font-size: 5rem;'>📄</div>
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
                            type_icon = "📕" if file_type == "PDF" else "🖼️" if file_type == "IMAGE" else "📄"
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
        
        badge_html = f"""
        <div style='display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap;'>
        """
        
        # Badge type de fichier
        if file_type == 'PDF':
            badge_html += f"""
            <div style='background-color: #ef4444; color: white; padding: 0.75rem 1.5rem; border-radius: 2rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3);'>
                <span style='font-size: 1.5rem;'>📕</span>
                <span>PDF</span>
            </div>
            """
        elif file_type == 'IMAGE':
            badge_html += f"""
            <div style='background-color: #10b981; color: white; padding: 0.75rem 1.5rem; border-radius: 2rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);'>
                <span style='font-size: 1.5rem;'>🖼️</span>
                <span>IMAGE</span>
            </div>
            """
        else:
            badge_html += f"""
            <div style='background-color: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 2rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);'>
                <span style='font-size: 1.5rem;'>📄</span>
                <span>{file_type}</span>
            </div>
            """
        
        # Badge catégorie
        if category:
            badge_html += f"""
            <div style='background-color: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 2rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);'>
                <span style='font-size: 1.5rem;'>📁</span>
                <span>{category}</span>
            </div>
            """
        
        # Badge confiance
        if doc.get('confidence') is not None:
            confidence_value = doc.get('confidence') * 100
            if confidence_value >= 80:
                conf_bg = "#10b981"
            elif confidence_value >= 60:
                conf_bg = "#f59e0b"
            else:
                conf_bg = "#ef4444"
            
            badge_html += f"""
            <div style='background-color: {conf_bg}; color: white; padding: 0.75rem 1.5rem; border-radius: 2rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);'>
                <span style='font-size: 1.5rem;'>⭐</span>
                <span>Confiance: {confidence_value:.1f}%</span>
            </div>
            """
        
        # Badge date
        if doc.get('created_at'):
            from datetime import datetime
            try:
                date_obj = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
                date_str = date_obj.strftime('%d/%m/%Y %H:%M')
                badge_html += f"""
                <div style='background-color: #64748b; color: white; padding: 0.75rem 1.5rem; border-radius: 2rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 10px rgba(100, 116, 139, 0.3);'>
                    <span style='font-size: 1.5rem;'>📅</span>
                    <span>{date_str}</span>
                </div>
                """
            except:
                pass
        
        badge_html += "</div>"
        st.markdown(badge_html, unsafe_allow_html=True)
        
        # Informations détaillées
        st.markdown("### 📋 Informations")
        
        st.markdown(f"""
        <div style='background-color: #f8fafc; padding: 1.5rem; border-radius: 1rem; border: 2px solid #e2e8f0; margin-bottom: 1rem;'>
            <div style='margin-bottom: 1rem;'>
                <span style='color: #64748b; font-weight: 600; font-size: 0.9rem;'>📎 NOM DU FICHIER</span>
                <p style='color: #1e293b; font-weight: 700; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>{doc.get('filename', 'N/A')}</p>
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
                <div style='background-color: #667eea; color: white; padding: 1rem 1.5rem; border-radius: 0.75rem; flex: 1; text-align: center; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.2);'>
                    <div style='font-size: 2rem; font-weight: 900;'>{word_count}</div>
                    <div style='font-size: 0.9rem; opacity: 0.95;'>📝 Mots</div>
                </div>
                <div style='background-color: #10b981; color: white; padding: 1rem 1.5rem; border-radius: 0.75rem; flex: 1; text-align: center; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2);'>
                    <div style='font-size: 2rem; font-weight: 900;'>{char_count}</div>
                    <div style='font-size: 0.9rem; opacity: 0.95;'>🔤 Caractères</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Affichage du texte avec formatage amélioré
            st.markdown(f"""
            <div style='background-color: #f8fafc; padding: 1.5rem; border-radius: 1rem; border: 2px solid #e2e8f0; margin-bottom: 1.5rem;'>
                <div style='color: #667eea; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;'>
                    <span style='font-size: 1.2rem;'>📝</span>
                    <span>Aperçu:</span>
                </div>
                <div style='color: #334155; line-height: 1.8; font-size: 0.95rem;'>
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
