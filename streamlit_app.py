import streamlit as st
import os
import sys

# 1. CETTE COMMANDE DOIT ÊTRE LA TOUTE PREMIÈRE (ET UNIQUE)
st.set_page_config(page_title="ISAC - Interface de Soin Avant Consultation", layout="wide", page_icon="🏥")

# 2. IMPORTS (Après la config de page)
try:
    from db_connector import db_connector 
except Exception as e:
    st.error(f"Erreur d'import du connecteur : {e}")

# 3. TITRE ET ÉTAT DE CONNEXION
st.title("🏥 Bienvenue sur ISAC")

# Vérification silencieuse de la connexion
if db_connector and db_connector.client:
    st.sidebar.success("✅ Base de données connectée")
else:
    st.sidebar.error("❌ Base de données déconnectée")
    st.stop() # Arrête l'exécution ici si la DB est cruciale

# --- INITIALISATION SESSION ---
if "logged_in" not in st.session_state:
    st.session_state.update({
        "logged_in": False, 
        "name": None, 
        "user_profile": "PATIENT", 
        "messages": []
    })

# --- FONCTION PROFIL SANTÉ ---
def render_sidebar_health_profile():
    st.sidebar.header("📋 Mon Profil Santé")
    age = st.sidebar.number_input("Âge", min_value=0, max_value=120, value=25)
    poids = st.sidebar.number_input("Poids (kg)", min_value=0, max_value=250, value=70)
    temp = st.sidebar.slider("Température (°C)", 35.0, 42.0, 37.0, 0.1)
    
    st.session_state["health_metrics"] = {
        "age": age,
        "poids": poids,
        "temperature": temp
    }
    
    if temp >= 38.5:
        st.sidebar.warning("⚠️ Fièvre détectée")

# --- LOGIQUE DE NAVIGATION / AUTH ---
# (Note: Ajoute ici ton formulaire de login si logged_in est False)
if not st.session_state.logged_in:
    st.info("Veuillez vous connecter pour accéder à ISAC.")
    # Exemple rapide de bouton pour tester
    if st.button("Connexion Test"):
        st.session_state.logged_in = True
        st.session_state.name = "Utilisateur"
        st.rerun()

else:
    render_sidebar_health_profile()
    
    st.sidebar.title(f"Bonjour, {st.session_state.name}")
    opts = ["💬 Ma Consultation", "📅 Prévention & Rappels", "📖 Guide Santé"]
    
    if st.session_state.user_profile == "ADMINISTRATION":
        opts.append("🛡️ Espace Praticien")
    
    mode = st.sidebar.radio("Navigation", opts)
    
    # --- NAVIGATION ---
    if mode == "💬 Ma Consultation":
        from chat_view import render_chat
        render_chat()
    elif mode == "📅 Prévention & Rappels":
        from view import render_health_page
        render_health_page()
    elif mode == "📖 Guide Santé":
        from help_view import render_help_page
        render_help_page()
    elif mode == "🛡️ Espace Praticien":
        from admin_view import render_admin_page
        render_admin_page()