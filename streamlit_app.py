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
        "logged_in": False,
        "username": None,
        "name": None,
        "messages": [],
        "user_profile": DEFAULT_PROFILE
    })

def logout():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

def get_user_profile(email):
    clean_email = email.strip().lower()
    for profile, keywords in USER_PROFILES_RULES.items():
        if any(kw.lower() in clean_email for kw in keywords): return profile
    return DEFAULT_PROFILE

# --- RENDER PAGES ---
def render_login_page():
    st.title("🎓 Bienvenue sur ISMaiLa")
    with st.form("login_form"):
        u_name = st.text_input("Prénom")
        u_email = st.text_input("Email Institutionnel")
        if st.form_submit_button("Se connecter"):
            if u_email and u_name:
                u_prof = get_user_profile(u_email)
                st.session_state.update({"logged_in": True, "username": u_email, "name": u_name, "user_profile": u_prof})
                db_logger.log_connection_event("LOGIN", u_email, u_name, u_prof)
                st.rerun()
            else: st.error("Champs requis.")

def render_chatbot_page():
    # Sidebar avec Statistiques
    st.sidebar.title("🛠️ Menu")
    try:
        n_val = mongo_db.contributions.count_documents({"status": "valide"})
        n_pend = mongo_db.contributions.count_documents({"status": "en_attente"})
        st.sidebar.success(f"📡 DB Connectée")
        st.sidebar.write(f"✅ {n_val} réponses")
        if n_pend > 0: st.sidebar.warning(f"⏳ {n_pend} à valider")
    except: st.sidebar.error("Erreur DB")

    st.sidebar.info(f"👤 {st.session_state.name}\n({st.session_state.user_profile})")
    # Ajoute "❓ Aide" aux options du menu
    menu_options = ["💬 Chatbot", "🌍 Contribution", "❓ Aide"]
    if st.session_state.user_profile == "ADMINISTRATION":
        menu_options.append("🛡️ Dashboard Admin")
    
    mode = st.sidebar.radio("Navigation", menu_options)
    opts = ["❓ Aide", "💬 Chatbot", "🌍 Contribution"]

    if st.session_state.user_profile == "ADMINISTRATION": opts.append("🛡️ Dashboard Admin")
    mode = st.sidebar.radio("Navigation", opts, key="main_navigation_menu")
    
    if st.sidebar.button('Déconnexion 🚪'): logout()

    if mode == "🛡️ Dashboard Admin": render_admin_page()
    elif mode == "🌍 Contribution": render_contribution_page()
    elif mode == "❓ Aide":
        render_help_page()
    else:
        st.title("💬 Votre Assistant ISMaiLa à votre service")
       # st.markdown("Bienvenue sur l'assistant intelligent du Groupe ISM.")

        if len(st.session_state.messages) == 0:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Salut {st.session_state.name} ! Comment puis-je vous aider ?"
            })

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if p := st.chat_input("Posez votre question..."):
            st.session_state.messages.append({"role": "user", "content": p})
            with st.chat_message("user"): st.write(p)
            
            res, src = ismaila_agent.get_response(p, st.session_state.user_profile, st.session_state.username)
            st.session_state.messages.append({"role": "assistant", "content": res})
            with st.chat_message("assistant"): 
                st.write(res)
                st.caption(f"Source: {src}")

# --- MAIN ---
if not st.session_state.logged_in: 
    render_login_page()
else: render_chatbot_page()