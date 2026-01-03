"""
Page d'upload de documents - Upload
Permet de téléverser des documents avec OCR et classification automatique
"""
import streamlit as st
from services.auth_service import AuthService
from services.api_service import APIService
import time

st.set_page_config(
    page_title="Upload - SmartDocManager",
    page_icon="📤",
    layout="wide"
)

# Vérifier l'authentification
if not AuthService.is_authenticated():
    st.error("🔒 Vous devez être connecté pour accéder à cette page")
    if st.button("Se connecter"):
        st.switch_page("pages/0_Login.py")
    st.stop()

# CSS personnalisé
# CSS personnalisé - Mode Sombre
st.markdown("""
<style>
    /* Fond sombre global */
    .stApp {
        background-color: #0F172A !important;
    }
    
    .upload-container {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border: 2px solid #475569;
    }
    .step-container {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
    }
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        background: #1E293B;
        color: #94A3B8;
        margin: 0 0.5rem;
        border: 1px solid #475569;
    }
    .step.active {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        transform: scale(1.05);
        border: none;
        box-shadow: 0 10px 20px rgba(139, 92, 246, 0.3);
    }
    .step.completed {
        background: #059669;
        color: white;
        border: none;
    }
    .result-card {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4);
    }
    /* Textes */
    h1, h2, h3 {
        color: #F8FAFC !important;
    }
    p, li {
        color: #CBD5E1 !important;
    }
    .stMarkdown p {
        color: #E2E8F0 !important;
    }
    .stCaption {
        color: #94A3B8 !important;
    }
    
    /* Boutons */
    .stButton>button {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header avec info utilisateur
user = AuthService.get_user()
col1, col2 = st.columns([4, 1])
with col1:
    st.title("📤 Upload de Documents")
with col2:
    if st.button("🚪 Déconnexion"):
        AuthService.logout()

st.markdown(f"👤 Connecté en tant que: **{user['username']}**")
st.markdown("---")

# Initialiser session_state
if 'upload_result' not in st.session_state:
    st.session_state.upload_result = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Étapes du processus
steps = [
    {"id": 1, "name": "Upload", "icon": "📤", "desc": "Téléversement du fichier"},
    {"id": 2, "name": "OCR", "icon": "👁️", "desc": "Extraction du texte"},
    {"id": 3, "name": "Classification", "icon": "🤖", "desc": "Classification IA"},
    {"id": 4, "name": "Terminé", "icon": "✅", "desc": "Traitement terminé"}
]

# Afficher les étapes
if st.session_state.upload_result is not None:
    cols = st.columns(4)
    for idx, step in enumerate(steps):
        with cols[idx]:
            if idx < st.session_state.current_step:
                st.markdown(f"""
                <div class="step completed">
                    <div style="font-size: 2rem;">{step['icon']}</div>
                    <div style="font-weight: bold;">{step['name']}</div>
                    <div style="font-size: 0.8rem;">{step['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
            elif idx == st.session_state.current_step:
                st.markdown(f"""
                <div class="step active">
                    <div style="font-size: 2rem;">{step['icon']}</div>
                    <div style="font-weight: bold;">{step['name']}</div>
                    <div style="font-size: 0.8rem;">{step['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="step">
                    <div style="font-size: 2rem;">{step['icon']}</div>
                    <div style="font-weight: bold;">{step['name']}</div>
                    <div style="font-size: 0.8rem;">{step['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

# Zone d'upload
if st.session_state.upload_result is None:
    st.markdown("### 📁 Sélectionnez un document à analyser")
    
    uploaded_file = st.file_uploader(
        "Glissez-déposez votre document ici ou cliquez pour parcourir",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="Formats acceptés: PDF, JPG, PNG • Taille max: 10 MB"
    )
    
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.success(f"📄 Fichier sélectionné: **{uploaded_file.name}**")
            st.caption(f"Taille: {uploaded_file.size / 1024 / 1024:.2f} MB")
            
            if st.button("🚀 Lancer l'analyse", use_container_width=True, type="primary"):
                # Simuler les étapes
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Étape 1: Upload
                st.session_state.current_step = 0
                status_text.text("📤 Téléversement du fichier...")
                progress_bar.progress(25)
                time.sleep(0.5)
                
                # Étape 2: OCR
                st.session_state.current_step = 1
                status_text.text("👁️ Extraction du texte...")
                progress_bar.progress(50)
                time.sleep(0.5)
                
                # Lire le contenu du fichier
                file_content = uploaded_file.getvalue()
                
                # Appeler l'API d'upload
                upload_result = APIService.upload_document(file_content, uploaded_file.name)
                
                if not upload_result["success"]:
                    st.error(f"❌ {upload_result['error']}")
                    progress_bar.empty()
                    status_text.empty()
                else:
                    document_id = upload_result["data"]["document_id"]
                    
                    # Étape 2: OCR
                    st.session_state.current_step = 1
                    status_text.text("👁️ Extraction du texte...")
                    progress_bar.progress(50)
                    time.sleep(0.5)
                    
                    ocr_result = APIService.perform_ocr(document_id)
                    
                    if not ocr_result["success"]:
                        st.error(f"❌ {ocr_result['error']}")
                        progress_bar.empty()
                        status_text.empty()
                    else:
                        # Étape 3: Classification
                        st.session_state.current_step = 2
                        status_text.text("🤖 Classification IA...")
                        progress_bar.progress(75)
                        time.sleep(0.5)
                        
                        classify_result = APIService.classify_document(document_id)
                        
                        if not classify_result["success"]:
                            st.error(f"❌ {classify_result['error']}")
                            progress_bar.empty()
                            status_text.empty()
                        else:
                            # Combiner les résultats
                            combined_result = {
                                "document_id": document_id,
                                "filename": upload_result["data"]["filename"],
                                "file_type": upload_result["data"].get("file_type", "N/A"),
                                "extracted_text": ocr_result["data"].get("extracted_text", ""),
                                "word_count": ocr_result["data"].get("word_count", 0),
                                "language": ocr_result["data"].get("language", "N/A"),
                                "category": classify_result["data"].get("category", "N/A"),
                                "confidence": classify_result["data"].get("confidence", 0) * 100,  # Convertir en pourcentage
                                "id": document_id
                            }
                            
                            # Étape 4: Terminé
                            st.session_state.current_step = 3
                            status_text.text("✅ Traitement terminé !")
                            progress_bar.progress(100)
                            time.sleep(0.5)
                            
                            st.session_state.upload_result = combined_result
                            st.rerun()

else:
    # Afficher les résultats
    result = st.session_state.upload_result
    
    st.balloons()
    st.success("✅ Document traité avec succès !")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="result-card">
            <h3>📋 Catégorie détectée</h3>
            <h1 style="font-size: 2.5rem; margin: 1rem 0;">{result.get('category', 'N/A')}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # L'API retourne déjà la confiance en pourcentage (0-100)
        confidence = result.get('confidence', 0)
        st.markdown("### 📊 Niveau de confiance")
        st.progress(confidence / 100)
        st.markdown(f"<h2 style='text-align: center; color: #667eea;'>{confidence:.1f}%</h2>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Informations supplémentaires
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📝 Mots extraits", result.get('word_count', 0))
    
    with col2:
        st.metric("📄 Type de fichier", result.get('file_type', 'N/A'))
    
    with col3:
        st.metric("📁 ID Document", result.get('id', 'N/A'))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Aperçu du texte extrait
    if result.get('extracted_text'):
        with st.expander("📝 Aperçu du texte extrait", expanded=False):
            st.text_area(
                "Texte",
                value=result['extracted_text'][:500] + "..." if len(result['extracted_text']) > 500 else result['extracted_text'],
                height=200,
                disabled=True
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Boutons d'action
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📁 Voir mes documents", use_container_width=True):
            st.switch_page("pages/3_Documents.py")
    
    with col2:
        if st.button("📊 Voir les statistiques", use_container_width=True):
            st.switch_page("pages/4_Dashboard.py")
    
    with col3:
        if st.button("🔄 Analyser un autre document", use_container_width=True, type="primary"):
            st.session_state.upload_result = None
            st.session_state.current_step = 0
            st.rerun()
