"""
Page d'inscription - Register
"""
import streamlit as st
from services.auth_service import AuthService

st.set_page_config(
    page_title="Inscription - SmartDocManager",
    page_icon="✨",
    layout="centered"
)

# CSS personnalisé
st.markdown("""
<style>
    .register-header {
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
<div class="register-header">
    <h1>✨ Inscription</h1>
    <p style="color: #6b7280;">Créez votre compte gratuitement</p>
</div>
""", unsafe_allow_html=True)

# Formulaire d'inscription
with st.form("register_form"):
    username = st.text_input("👤 Nom d'utilisateur", placeholder="Choisissez un nom d'utilisateur")
    email = st.text_input("📧 Email", placeholder="votre.email@example.com")
    password = st.text_input("🔒 Mot de passe", type="password", placeholder="Choisissez un mot de passe sécurisé")
    password_confirm = st.text_input("🔒 Confirmer le mot de passe", type="password", placeholder="Confirmez votre mot de passe")
    
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Créer mon compte", use_container_width=True, type="primary")
    with col2:
        if st.form_submit_button("Retour", use_container_width=True):
            st.switch_page("Accueil.py")
    
    if submit:
        # Validation des champs
        if not username or not email or not password or not password_confirm:
            st.error("⚠️ Veuillez remplir tous les champs")
        elif password != password_confirm:
            st.error("❌ Les mots de passe ne correspondent pas")
        elif len(password) < 6:
            st.error("❌ Le mot de passe doit contenir au moins 6 caractères")
        elif "@" not in email or "." not in email:
            st.error("❌ Veuillez entrer une adresse email valide")
        else:
            with st.spinner("🔄 Création du compte..."):
                result = AuthService.register(username, email, password)
                
                if result["success"]:
                    st.success("✅ Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                    st.balloons()
                    if st.button("Se connecter maintenant", use_container_width=True):
                        st.switch_page("pages/0_Login.py")
                else:
                    st.error(f"❌ {result['error']}")

st.markdown("<br>", unsafe_allow_html=True)

# Lien vers la connexion
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: #6b7280;">
        <p>Vous avez déjà un compte ?</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔐 Se connecter", use_container_width=True):
        st.switch_page("pages/0_Login.py")
