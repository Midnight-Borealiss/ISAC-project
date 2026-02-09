import streamlit as st
from agent import ismaila_agent
from logger import db_logger
from admin_dashboard import render_admin_dashboard

# --- CONFIGURATION DES PROFILS ---
USER_PROFILES_RULES = {
    "ADMINISTRATION": ["votre.email@admin", "votre.email@gmail.com", "minawade005gmail.com"],
    "ÉTUDIANT": ["votre.email@edu", "etudiant@ism.sn"]
}
DEFAULT_PROFILE = "ÉTUDIANT"

st.set_page_config(page_title="ISMaiLa - Assistant Virtuel", layout="wide")

# --- GESTION DE LA SESSION ---
if "logged_in" not in st.session_state:
    st.session_state.update({
        "logged_in": False,
        "username": None,
        "name": None,
        "messages": [],
        "user_profile": DEFAULT_PROFILE
    })

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def get_user_profile(email):
    email = email.lower()
    for profile, keywords in USER_PROFILES_RULES.items():
        if any(kw in email for kw in keywords):
            return profile
    return DEFAULT_PROFILE

# --- VUES ---

def render_login_page():
    st.title("🎓 Bienvenue sur l'assistant intelligent du Groupe ISM.")
    st.markdown("Veuillez saisir votre nom et votre email pour démarrer la conversation.👤")
    with st.form("login_form"):
        user_name = st.text_input("Prénom & Nom")
        user_email = st.text_input("Email Institutionnel")
        submit = st.form_submit_button("Se connecter")
        
        if submit:
            if user_email and user_name:
                user_profile = get_user_profile(user_email)
                st.session_state.update({
                    "logged_in": True,
                    "username": user_email,
                    "name": user_name,
                    "user_profile": user_profile
                })
                # Log de connexion
                db_logger.log_connection_event("LOGIN", user_email, user_name, user_profile)
                st.rerun()
            else:
                st.error("Veuillez remplir tous les champs.")

def render_chatbot_page():
    # 1. Sidebar
    st.sidebar.title("🛠️ Menu")
    st.sidebar.info(f"Connecté en tant que :\n**{st.session_state.name}**\n({st.session_state.user_profile})")
    
    if st.session_state.user_profile == "ADMINISTRATION":
        mode = st.sidebar.radio("Navigation", ["Chatbot", "Dashboard Admin"])
        if mode == "Dashboard Admin":
            render_admin_dashboard()
            return

    if st.sidebar.button('Déconnexion 🚪'):
        logout()
    
    # 2. Interface Chat
    st.title("💬 Votre Assistant ISMaiLa à votre service")
    st.markdown("Bienvenue sur l'assistant intelligent du Groupe ISM.")

    # --- LA CORRECTION EST ICI ---
    # On ajoute le message d'accueil UNIQUEMENT si la liste est vide
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"Salut {st.session_state.name} ! Comment puis-je vous aider ?"
        })
    # -----------------------------

    # Affichage de l'historique
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Zone de saisie
    if prompt := st.chat_input("Posez votre question à ISMaiLa..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("ISMAILA analyse votre demande..."):
            response, _ = ismaila_agent.get_response(
                prompt, 
                st.session_state.user_profile,
                st.session_state.username
            )
            
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- LOGIQUE PRINCIPALE ---
if not st.session_state.logged_in:
    render_login_page()
else:
    render_chatbot_page()