import os
import sys
import streamlit as st

# --- CORRECTIF DE CHEMIN (PATH FIX) ---
# Indispensable pour que Python trouve le dossier 'modules'
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# --- IMPORTS DES SERVICES ET AGENTS ---
from db_connector import mongo_db
from agent import ismaila_agent

# --- IMPORTS MODULAIRES (VUES) ---
# On utilise les noms de fonctions définis dans nos nouveaux fichiers
try:
    from modules.chatbot.chat_view import render_chat
    from modules.contribution.view import render_contribution
    from modules.admin.admin_view import render_admin
except ImportError as e:
    st.error(f"Erreur de chargement des modules : {e}")
    st.stop()

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="ISMaiLa", page_icon="🎓", layout="wide")

# (Ici, place ton code de gestion de session / Login habituel)
# Imaginons que ton utilisateur est déjà connecté pour la logique ci-dessous :

def render_main_interface():
    """Gère la navigation entre les différents modules"""
    
    st.sidebar.title("📌 Navigation")
    
    # Définition des modes selon le profil
    modes = ["💬 Chatbot"]
    if st.session_state.get('user_profile') == "ADMINISTRATION":
        modes.append("🛡️ Administration")
    modes.append("🌍 Contribution")
    
    mode = st.sidebar.radio("Aller vers :", modes)

    # --- ROUTAGE DES VUES ---
    if mode == "🛡️ Administration":
        # On appelle 'render_admin' (et non render_admin_page)
        render_admin() 
        
    elif mode == "🌍 Contribution":
        # On appelle 'render_contribution' (et non render_contribution_page)
        render_contribution() 
        
    else:
        # On appelle 'render_chat'
        render_chat()

# Lancement de l'app
if __name__ == "__main__":
    # simulation simplifiée de la session pour l'exemple
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    render_main_interface()