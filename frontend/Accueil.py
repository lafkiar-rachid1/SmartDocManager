"""
Page d'accueil publique - SmartDocManager avec Streamlit
Permet l'analyse de documents sans authentification ni stockage
"""
import streamlit as st
from services.api_service import APIService
from services.auth_service import AuthService
import time

# Configuration de la page
st.set_page_config(
    page_title="SmartDocManager - Accueil",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé - Mode Sombre
st.markdown("""
<style>
    /* Fond sombre global */
    .stApp {
        background-color: #0F172A !important;
    }
    
    .main {
        background-color: #0F172A !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
    }
    .warning-banner {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        color: white;
        margin-bottom: 2rem;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .feature-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
        border: 2px solid #475569;
        transition: all 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(139, 92, 246, 0.4);
        border-color: #8B5CF6;
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
    }
    .feature-card h3 {
        color: #E2E8F0 !important;
    }
    .feature-card p {
        color: #94A3B8 !important;
    }
    .result-card {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(139, 92, 246, 0.5);
        background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
    }
    
    /* Inputs et autres éléments */
    .stTextInput input {
        background-color: #1E293B !important;
        color: #E2E8F0 !important;
        border-color: #475569 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #8B5CF6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialiser session_state pour la page d'accueil
if 'guest_result' not in st.session_state:
    st.session_state.guest_result = None

# Vérifier si l'utilisateur est déjà authentifié
if AuthService.is_authenticated():
    st.switch_page("pages/2_Upload.py")

# Header principal
st.markdown("""
<div class="main-header">
    <h1>📄 SmartDocManager</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">Analysez vos documents intelligemment avec l'IA</p>
</div>
""", unsafe_allow_html=True)

# Bannière d'avertissement
st.markdown("""
<div class="warning-banner">
    <h3>⚠️ Mode Visiteur - Aucune Sauvegarde</h3>
    <p>Vos documents ne sont pas sauvegardés. Dès que vous quittez cette page, tout est effacé.</p>
    <p><strong>Créez un compte gratuitement pour bénéficier du stockage permanent de vos documents !</strong></p>
</div>
""", unsafe_allow_html=True)

# Boutons de connexion/inscription
col1, col2, col3 = st.columns([3, 1, 1])
with col2:
    if st.button("🔐 Connexion", use_container_width=True):
        st.switch_page("pages/0_Login.py")
with col3:
    if st.button("✨ Créer un compte", use_container_width=True):
        st.switch_page("pages/1_Register.py")

st.markdown("<br>", unsafe_allow_html=True)

# Section principale
st.markdown("### 🎯 Essayez notre analyseur de documents gratuitement")
st.markdown("Téléchargez un document et découvrez sa catégorie automatiquement grâce à l'intelligence artificielle")

st.markdown("<br>", unsafe_allow_html=True)

# Zone d'upload
if st.session_state.guest_result is None:
    uploaded_file = st.file_uploader(
        "📤 Glissez-déposez votre document ici ou cliquez pour parcourir",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="Formats acceptés: PDF, JPG, PNG • Taille max: 10 MB"
    )
    
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.info(f"📄 Fichier sélectionné: **{uploaded_file.name}**")
            st.caption(f"Taille: {uploaded_file.size / 1024 / 1024:.2f} MB")
            
            if st.button("🔍 Analyser le document", use_container_width=True, type="primary"):
                with st.spinner("🤖 Analyse en cours..."):
                    # Lire le contenu du fichier
                    file_content = uploaded_file.getvalue()
                    result = APIService.analyze_guest_document(file_content, uploaded_file.name)
                    
                    if result["success"]:
                        st.session_state.guest_result = result["data"]
                        # Normaliser les données pour l'affichage
                        if "confidence" in st.session_state.guest_result:
                            # L'API retourne la confiance en pourcentage (0-100)
                            # On la garde telle quelle pour l'affichage
                            pass
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ {result['error']}")
else:
    # Afficher les résultats
    result = st.session_state.guest_result
    
    st.success("✅ Analyse terminée !")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Catégorie détectée
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        category = result.get('category', 'N/A')
        st.markdown(f"""
        <div class="result-card">
            <h2 style="margin: 0;">📋 Catégorie détectée</h2>
            <h1 style="margin: 1rem 0; font-size: 3rem;">{category}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Niveau de confiance
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📊 Niveau de confiance")
        # L'API retourne déjà en pourcentage (0-100), donc on divise par 100 pour la progress bar
        confidence_value = result.get('confidence', 0)
        st.progress(confidence_value / 100)
        st.markdown(f"<h2 style='text-align: center; color: #667eea;'>{confidence_value:.1f}%</h2>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Avertissement
    st.warning("""
    ⚠️ **Résultat temporaire**
    
    Ce document n'a pas été sauvegardé. Pour conserver vos analyses et accéder à l'historique complet, 
    créez un compte gratuit.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bouton pour analyser un autre document
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Analyser un autre document", use_container_width=True, type="primary"):
            st.session_state.guest_result = None
            st.rerun()

# Section avantages
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### ✨ Pourquoi choisir SmartDocManager ?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
        <h3>Analyse rapide</h3>
        <p style="color: #6b7280;">Classification automatique en quelques secondes grâce à notre moteur d'IA optimisé</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
        <h3>Intelligence artificielle</h3>
        <p style="color: #6b7280;">Modèle de Machine Learning entraîné sur des milliers de documents professionnels</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">💾</div>
        <h3>Stockage sécurisé</h3>
        <p style="color: #6b7280;">Créez un compte pour sauvegarder vos documents et accéder à l'historique complet</p>
    </div>
    """, unsafe_allow_html=True)
