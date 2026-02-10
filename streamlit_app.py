import streamlit as st
from db_connector import mongo_db
from agent import ismaila_agent

# On importe les vues depuis le nouveau dossier modules
from modules.contribution.view import render_contribution
from modules.admin.admin_view import render_admin

# --- CONFIGURATION ---
USER_PROFILES_RULES = {
    "ADMINISTRATION": ["mina@gmail.com", "ismaila.admin@uam.sn"],
    "ÉTUDIANT": ["@edu.uam.sn", "@uam.sn"]
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
    clean_email = email.strip().lower()
    for profile, keywords in USER_PROFILES_RULES.items():
        for kw in keywords:
            if kw.lower() in clean_email:
                return profile
    return DEFAULT_PROFILE

# --- VUES ---

def render_login_page():
    st.title("🎓 Bienvenue sur l'assistant intelligent du Groupe ISM.")
    st.markdown("Veuillez saisir votre nom et votre email pour démarrer la conversation.👤")
    with st.form("login_form"):
        user_name = st.text_input("Prénom ou Pseudonyme")
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
                # Log de connexion dans MongoDB
                mongo_db.log_event("LOGIN", user_email, user_name, f"Profil: {user_profile}")
                st.rerun()
            else:
                st.error("Veuillez remplir tous les champs.")

def render_chatbot_page():
    # 1. Sidebar
    st.sidebar.title("🛠️ Menu")
    st.sidebar.info(f"Connecté en tant que :\n**{st.session_state.name}**\n({st.session_state.user_profile})")
    
    # 2. Logique de Navigation (Fusion)
    menu_options = ["💬 Chatbot", "🌍 Contribution"]
    if st.session_state.user_profile == "ADMINISTRATION":
        menu_options.append("🛡️ Dashboard Admin")
    
    mode = st.sidebar.radio("Navigation", menu_options)

    if st.sidebar.button('Déconnexion 🚪'):
        logout()
    
    # --- ROUTAGE DES PAGES ---
    
    if mode == "Dashboard Admin":
        render_admin_page() # Appelle le fichier app/views/admin_view.py
        
    elif mode == "🌍 Contribution":
        render_contribution_page() # Appelle le fichier app/views/contribution_view.py
        
    else:
        # INTERFACE CHATBOT CLASSIQUE
        st.title("💬 Votre Assistant ISMaiLa à votre service")
        st.markdown("Bienvenue sur l'assistant intelligent du Groupe ISM.")

        if len(st.session_state.messages) == 0:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Salut {st.session_state.name} ! Comment puis-je vous aider ?"
            })

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if prompt := st.chat_input("Posez votre question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            
            # Réponse de l'agent
            response, _ = ismaila_agent.get_response(prompt, st.session_state.user_profile, st.session_state.username)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"): st.write(response)

# --- LANCEMENT ---
if not st.session_state.logged_in:
    render_login_page()
else:
    render_chatbot_page()