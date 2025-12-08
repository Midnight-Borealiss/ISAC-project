# streamlit_app.py
import streamlit as st
import time 
from agent import get_agent_response
from logger import log_connection_event 
from admin_dashboard import render_admin_dashboard

USER_PROFILES_RULES = {
    "ADMINISTRATION": ["admin@ism.edu", "votre.email@admin"],
    "ÉTUDIANT": ["etudiant@ism.edu"]
}
DEFAULT_PROFILE = "GUEST"

st.set_page_config(page_title="Assistant ISMaiLa", layout="wide")

# Session Init
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_profile" not in st.session_state: st.session_state.user_profile = DEFAULT_PROFILE
if "messages" not in st.session_state: st.session_state.messages = []
if "view" not in st.session_state: st.session_state.view = 'chatbot'

def login(email, name):
    profile = DEFAULT_PROFILE
    for p, emails in USER_PROFILES_RULES.items():
        if email.lower() in emails: profile = p
            
    st.session_state.logged_in = True
    st.session_state.username = email
    st.session_state.name = name
    st.session_state.user_profile = profile
    
    log_connection_event("LOGIN", email, name, profile)
    st.rerun()

def logout():
    log_connection_event("LOGOUT", st.session_state.username, st.session_state.name, st.session_state.user_profile)
    st.session_state.clear()
    st.rerun()

# --- UI ---
if not st.session_state.logged_in:
    st.title("Connexion ISMaiLa")
    with st.form("login"):
        name = st.text_input("Nom")
        email = st.text_input("Email")
        if st.form_submit_button("Entrer") and name and email:
            login(email, email) # Username = Email pour simplifier
else:
    # Sidebar
    st.sidebar.write(f"**{st.session_state.name}** ({st.session_state.user_profile})")
    
    if st.session_state.user_profile == "ADMINISTRATION":
        if st.sidebar.button("Dashboard 📊"): st.session_state.view = 'dashboard'
        if st.sidebar.button("Chatbot 💬"): st.session_state.view = 'chatbot'
        
    st.sidebar.button("Déconnexion", on_click=logout)

    # Main Content
    if st.session_state.view == 'dashboard' and st.session_state.user_profile == "ADMINISTRATION":
        render_admin_dashboard()
    else:
        st.title("Chatbot ISMaiLa")
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
            
        if prompt := st.chat_input("Question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            with st.spinner("..."):
                resp, _ = get_agent_response(prompt, st.session_state.user_profile, st.session_state.username)
                st.session_state.messages.append({"role": "assistant", "content": resp})
                st.chat_message("assistant").write(resp)