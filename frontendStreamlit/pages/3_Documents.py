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

# CSS personnalisé
st.markdown("""
<style>
    /* Style général */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    
    /* Cartes de documents */
    .doc-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: all 0.3s;
    }
    
    .doc-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    
    /* Filtres */
    .filter-section {
        background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.6) 100%);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 1.5rem;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Badges */
    .category-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .confidence-high {
        color: #10b981;
        background: rgba(16, 185, 129, 0.1);
    }
    
    .confidence-medium {
        color: #f59e0b;
        background: rgba(245, 158, 11, 0.1);
    }
    
    .confidence-low {
        color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }
    
    /* Modal */
    .modal-header {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem 1rem 0 0;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(79, 70, 229, 0.2);
        margin-bottom: 0.75rem;
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

# En-tête avec design amélioré
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1 style='font-size: 4rem; font-weight: 900; background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
        📁 Mes Documents
    </h1>
</div>
""", unsafe_allow_html=True)

filtered_docs = filter_documents()

# Stats et bouton d'actualisation
col_stat, col_btn = st.columns([4, 1])
with col_stat:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #60a5fa 0%, #6366f1 100%); padding: 1rem 2rem; border-radius: 1rem; color: white; text-align: center;'>
        <h2 style='margin: 0; font-size: 2rem; font-weight: 800;'>{len(filtered_docs)}</h2>
        <p style='margin: 0; font-size: 1.1rem; opacity: 0.9;'>Document(s) trouvé(s)</p>
    </div>
    """, unsafe_allow_html=True)
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Actualiser", use_container_width=True, type="primary"):
        load_documents()
        st.rerun()

# Section des filtres avec design amélioré
st.markdown("""
<div style='margin: 2rem 0;'>
    <h2 style='font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;'>
        🔍 Filtres de Recherche
    </h2>
</div>
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
                        # Carte de document avec design amélioré
                        # Icône selon le type
                        icon = "📄"
                        icon_color = "#3b82f6"
                        if doc.get('file_type') == 'PDF':
                            icon = "📕"
                            icon_color = "#ef4444"
                        elif doc.get('file_type') == 'IMAGE':
                            icon = "🖼️"
                            icon_color = "#10b981"
                        
                        # Nom du fichier tronqué
                        filename = doc.get('filename', 'Sans nom')
                        display_name = filename[:30] + '...' if len(filename) > 30 else filename
                        
                        # Badge de confiance avec couleur
                        confidence = (doc.get('confidence') or 0) * 100
                        if confidence >= 80:
                            conf_color = "#10b981"
                            conf_bg = "rgba(16, 185, 129, 0.1)"
                        elif confidence >= 60:
                            conf_color = "#f59e0b"
                            conf_bg = "rgba(245, 158, 11, 0.1)"
                        else:
                            conf_color = "#ef4444"
                            conf_bg = "rgba(239, 68, 68, 0.1)"
                        
                        st.markdown(f"""
                        <div class='doc-card'>
                            <div style='text-align: center; margin-bottom: 1rem;'>
                                <div style='font-size: 3.5rem; margin-bottom: 0.5rem;'>{icon}</div>
                                <h3 style='margin: 0; font-size: 1.1rem; font-weight: 700; color: #1f2937;'>{display_name}</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Catégorie
                        if doc.get('category'):
                            st.markdown(f"""
                            <div style='text-align: center; margin: 1rem 0;'>
                                <span style='background: linear-gradient(135deg, #60a5fa 0%, #6366f1 100%); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 700; font-size: 0.9rem;'>
                                    📁 {doc['category']}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Confiance
                        if doc.get('confidence') is not None:
                            st.markdown(f"""
                            <div style='text-align: center; margin: 1rem 0;'>
                                <span style='background: {conf_bg}; color: {conf_color}; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 700; font-size: 0.9rem;'>
                                    ⭐ {confidence:.1f}%
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Boutons d'action
                        col_btn1, col_btn2 = st.columns(2, gap="small")
                        with col_btn1:
                            if st.button("👁️ Voir", key=f"view_{doc['id']}", use_container_width=True, type="primary"):
                                st.session_state.selected_document = doc
                                st.rerun()
                        with col_btn2:
                            if st.button("🗑️", key=f"delete_{doc['id']}", use_container_width=True):
                                if st.session_state.get(f'confirm_delete_{doc["id"]}'):
                                    delete_document(doc['id'])
                                else:
                                    st.session_state[f'confirm_delete_{doc["id"]}'] = True
                                    st.rerun()
                        
                        # Confirmation de suppression
                        if st.session_state.get(f'confirm_delete_{doc["id"]}'):
                            st.warning("⚠️ Confirmer ?")
                            col_conf1, col_conf2 = st.columns(2)
                            with col_conf1:
                                if st.button("✅", key=f"yes_{doc['id']}", use_container_width=True):
                                    delete_document(doc['id'])
                            with col_conf2:
                                if st.button("❌", key=f"no_{doc['id']}", use_container_width=True):
                                    del st.session_state[f'confirm_delete_{doc["id"]}']
                                    st.rerun()
                        
                        st.markdown('</div>', unsafe_allow_html=True)

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
        
        # Informations principales
        st.markdown("### 📋 Informations")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='info-box'>
                <p style='color: #4F46E5; font-weight: bold; margin-bottom: 0.5rem;'>📎 Nom du fichier</p>
                <p style='font-weight: bold; font-size: 1.1rem; margin: 0;'>{doc.get('filename', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='info-box'>
                <p style='color: #4F46E5; font-weight: bold; margin-bottom: 0.5rem;'>📂 Type de fichier</p>
                <p style='font-weight: bold; font-size: 1.1rem; margin: 0;'>{doc.get('file_type', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if doc.get('category'):
            col3, col4 = st.columns(2)
            with col3:
                st.markdown(f"""
                <div class='info-box'>
                    <p style='color: #10b981; font-weight: bold; margin-bottom: 0.5rem;'>📁 Catégorie</p>
                    <p style='font-weight: bold; font-size: 1.1rem; margin: 0;'>{doc['category']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                confidence_value = (doc.get('confidence') or 0) * 100
                confidence_color = "#10b981" if confidence_value >= 80 else "#f59e0b" if confidence_value >= 60 else "#ef4444"
                st.markdown(f"""
                <div class='info-box'>
                    <p style='color: {confidence_color}; font-weight: bold; margin-bottom: 0.5rem;'>⭐ Confiance</p>
                    <p style='font-weight: bold; font-size: 1.1rem; margin: 0; color: {confidence_color};'>{confidence_value:.1f}%</p>
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
            with st.expander("👁️ Voir le texte complet", expanded=False):
                st.text_area(
                    "Texte",
                    value=doc['extracted_text'],
                    height=300,
                    label_visibility="collapsed"
                )
        
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
