import streamlit as st
import os
import sys

# --- CONFIGURATION ISAC ---
ADMIN_EMAILS = ["minawade005@gmail.com"] # Tes emails médecins/admin

st.set_page_config(page_title="ISAC - Assistant Médical", layout="wide", page_icon="🏥")

# --- INITIALISATION SESSION ---
if "logged_in" not in st.session_state:
    st.session_state.update({"logged_in": False, "username": None, "user_profile": None, "messages": []})

def render_sidebar_health_profile():
    """Formulaire de constantes dans la barre latérale"""
    st.sidebar.header("📋 Mon Profil Santé")
    age = st.sidebar.number_input("Âge", min_value=0, max_value=120, value=25)
    poids = st.sidebar.number_input("Poids (kg)", min_value=0, max_value=250, value=70)
    temp = st.sidebar.slider("Température (°C)", 35.0, 42.0, 37.0, 0.1)
    
    # On stocke ces données pour que l'agent.py y ait accès
    st.session_state["health_metrics"] = {
        "age": age,
        "poids": poids,
        "temperature": temp
    }
    
    if temp >= 38.5:
        st.sidebar.warning("⚠️ Fièvre détectée")

# --- LOGIQUE DE NAVIGATION ---
if st.session_state.logged_in:
    render_sidebar_health_profile()
    
    st.sidebar.title(f"Bonjour, {st.session_state.name}")
    opts = ["💬 Ma Consultation", "📅 Prévention & Rappels", "📖 Guide Santé"]
    if st.session_state.user_profile == "ADMINISTRATION":
        opts.append("🛡️ Espace Praticien")
    
    mode = st.sidebar.radio("Navigation", opts)
    
    # --- LES IMPORTS CORRIGÉS ICI ---
    if mode == "💬 Ma Consultation":
        from chat_view import render_chat  # Vérifie que le fichier s'appelle bien chat_view.py
        render_chat()
    elif mode == "📅 Prévention & Rappels":
        from view import render_health_page # Vérifie que la fonction s'appelle render_health_page
        render_health_page()
    elif mode == "📖 Guide Santé":
        from help_view import render_help_page
        render_help_page()
    elif mode == "🛡️ Espace Praticien":
        from admin_view import render_admin_page
        render_admin_page()