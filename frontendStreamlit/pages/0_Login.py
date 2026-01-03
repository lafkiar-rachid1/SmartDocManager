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
st.markdown("""
<style>
    .login-container {
        background: white;
        padding: 3rem;
        border-radius: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        max-width: 500px;
        margin: 2rem auto;
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
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
