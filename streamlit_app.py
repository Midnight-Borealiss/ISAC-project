import streamlit as st
import os
import sys
import pandas as pd

# --- FIX DES CHEMINS ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_connector import mongo_db
# À insérer juste après l'import de mongo_db
try:
    # On teste si on peut compter les documents
    count = mongo_db.contributions.count_documents({})
    st.sidebar.success(f"📡 MongoDB Connecté ({count} contribs)")
except Exception as e:
    st.sidebar.error(f"📡 Erreur MongoDB : {e}")
from agent import ismaila_agent
from modules.contribution.view import render_contribution_page
from modules.admin.admin_view import render_admin_page

# --- CONFIGURATION ---
USER_PROFILES_RULES = {
    "ADMINISTRATION": ["mina@gmail.com", "ismaila.admin@uam.sn"],
    "ÉTUDIANT": ["@edu.uam.sn", "@uam.sn"]
}
DEFAULT_PROFILE = "ÉTUDIANT"

st.set_page_config(page_title="ISMaiLa - Assistant Virtuel", layout="wide", page_icon="🎓")

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
                # Log de connexion
                mongo_db.logs.insert_one({
                    "event": "LOGIN", 
                    "user": user_email, 
                    "timestamp": pd.Timestamp.now()
                })
                st.rerun()
            else:
                st.error("Veuillez remplir tous les champs.")

def render_chatbot_page():
    st.sidebar.title("🛠️ Menu")
    st.sidebar.info(f"Connecté : **{st.session_state.name}**\n({st.session_state.user_profile})")
    
    menu_options = ["💬 Chatbot", "🌍 Contribution"]
    if st.session_state.user_profile == "ADMINISTRATION":
        menu_options.append("🛡️ Dashboard Admin")
    
    mode = st.sidebar.radio("Navigation", menu_options)

    if st.sidebar.button('Déconnexion 🚪'):
        logout()
    
    if mode == "🛡️ Dashboard Admin":
        render_admin_page()
    elif mode == "🌍 Contribution":
        render_contribution_page()
    else:
        st.title("💬 Assistant ISMaiLa")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.write(msg["content"])

        if prompt := st.chat_input("Posez votre question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            
            response, _ = ismaila_agent.get_response(prompt, st.session_state.user_profile, st.session_state.username)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"): st.write(response)

# --- LANCEMENT ---
if not st.session_state.logged_in:
    render_login_page()
else:
    render_chatbot_page()