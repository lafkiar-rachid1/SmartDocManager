"""
Page de connexion - Login
"""
import streamlit as st
from services.auth_service import AuthService

st.set_page_config(
    page_title="Connexion - SmartDocManager",
    page_icon="🔐",
    layout="centered"
)

# CSS personnalisé
# CSS personnalisé - Mode Sombre
st.markdown("""
<style>
    /* Fond sombre global */
    .stApp {
        background-color: #0F172A !important;
    }
    
    .login-container {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 3rem;
        border-radius: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        max-width: 500px;
        margin: 2rem auto;
        border: 1px solid #475569;
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-header h1 {
        color: #F8FAFC !important;
    }
    .login-header p {
        color: #94A3B8 !important;
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
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
        background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
    }
    
    /* Inputs */
    .stTextInput label {
        color: #E2E8F0 !important;
    }
    .stTextInput input {
        background-color: #0F172A !important;
        color: #E2E8F0 !important;
        border-color: #475569 !important;
    }
    .stTextInput input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 1px #8B5CF6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Vérifier si déjà connecté
if AuthService.is_authenticated():
    st.switch_page("pages/2_Upload.py")

# Header
st.markdown("""
<div class="login-header">
    <h1>🔐 Connexion</h1>
    <p style="color: #6b7280;">Connectez-vous pour accéder à votre espace</p>
</div>
""", unsafe_allow_html=True)

# Formulaire de connexion
with st.form("login_form"):
    username = st.text_input("👤 Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
    password = st.text_input("🔒 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
    
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Se connecter", use_container_width=True, type="primary")
    with col2:
        if st.form_submit_button("Retour", use_container_width=True):
            st.switch_page("Accueil.py")
    
    if submit:
        if not username or not password:
            st.error("⚠️ Veuillez remplir tous les champs")
        else:
            with st.spinner("🔄 Connexion en cours..."):
                result = AuthService.login(username, password)
                
                if result["success"]:
                    st.success("✅ Connexion réussie ! Redirection...")
                    st.balloons()
                    st.switch_page("pages/2_Upload.py")
                else:
                    st.error(f"❌ {result['error']}")

st.markdown("<br>", unsafe_allow_html=True)

# Lien vers l'inscription
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: #6b7280;">
        <p>Vous n'avez pas de compte ?</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("✨ Créer un compte", use_container_width=True):
        st.switch_page("pages/1_Register.py")
