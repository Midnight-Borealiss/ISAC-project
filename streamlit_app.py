import streamlit as st
import os
import sys
import pandas as pd
from modules.help.help_view import render_help_page

# --- FIX DES CHEMINS ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_connector import mongo_db
from agent import ismaila_agent
from logger import db_logger
from modules.contribution.view import render_contribution_page
from modules.admin.admin_view import render_admin_page
from modules.help.help_view import render_help_page

# --- CONFIGURATION ---
USER_PROFILES_RULES = {
    "ADMINISTRATION": ["minawade005@gmail.com", "ismaila.admin@uam.sn"],
    "ÉTUDIANT": ["@edu.uam.sn", "@uam.sn"]
}
DEFAULT_PROFILE = "ÉTUDIANT"

st.set_page_config(page_title="ISMaiLa - Assistant Virtuel", layout="wide", page_icon="🎓")

# --- INITIALISATION SESSION ---
if "logged_in" not in st.session_state:
    st.session_state.update({
        "logged_in": False, "username": None, "name": None, "messages": [], "user_profile": "ÉTUDIANT"
    })

def logout():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

# --- INTERFACE CHATBOT ---
def render_chat_interface():
    st.title("💬 Assistant ISMaiLa")
    if not st.session_state.messages:
        st.session_state.messages.append({"role": "assistant", "content": f"Bonjour {st.session_state.name} ! Comment puis-je vous aider ?"})

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if p := st.chat_input("Posez votre question..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        res, src = ismaila_agent.get_response(p, st.session_state.user_profile, st.session_state.username)
        st.session_state.messages.append({"role": "assistant", "content": res})
        with st.chat_message("assistant"): 
            st.write(res)
            st.caption(f"Source: {src}")

# --- PAGE PRINCIPALE APRÈS LOGIN ---
def render_chatbot_page():
    # Barre latérale UNIQUE
    st.sidebar.title("🛠️ Menu ISMaiLa")
    
    opts = ["💬 Chatbot", "🌍 Contribution", "❓ Aide"]
    if st.session_state.user_profile == "ADMINISTRATION":
        opts.append("🛡️ Dashboard Admin")
    
    mode = st.sidebar.radio("Navigation", opts, key="navigation_radio")
    
    if st.sidebar.button('Déconnexion 🚪'): logout()
    
    # Affichage du contenu
    if mode == "🛡️ Dashboard Admin":
        render_admin_page()
    elif mode == "🌍 Contribution":
        render_contribution_page()
    elif mode == "❓ Aide":
        render_help_page()
    else:
        render_chat_interface()

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.logged_in:
    st.title("🎓 Assistant Intelligent ISM")
    with st.form("login"):
        u_name = st.text_input("Prénom")
        u_email = st.text_input("Email Institutionnel")
        if st.form_submit_button("Se connecter"):
            if u_email and u_name:
                prof = "ADMINISTRATION" if u_email in ["minawade005@gmail.com", "ismaila.admin@uam.sn"] else "ÉTUDIANT"
                st.session_state.update({"logged_in": True, "username": u_email, "name": u_name, "user_profile": prof})
                st.rerun()
else:
    render_chatbot_page()