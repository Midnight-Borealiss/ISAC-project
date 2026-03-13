import streamlit as st
from db_connector import db_connector 
from agent import ISACAgent

st.set_page_config(page_title="ISAC - MVP", layout="wide", page_icon="🏥")

# Instanciation optimisée de l'agent
@st.cache_resource
def get_isac_agent():
    return ISACAgent()

isac_agent = get_isac_agent()

st.title("🏥 Bienvenue sur ISAC")

if not db_connector.client:
    st.sidebar.error("❌ Base de données déconnectée")
    st.stop()

# --- INITIALISATION SESSION ---
if "logged_in" not in st.session_state:
    st.session_state.update({"logged_in": False, "name": None, "user_profile": "PATIENT"})

# --- LOGIQUE DE NAVIGATION ---
if not st.session_state.logged_in:
    if st.button("Connexion Test"):
        st.session_state.update({"logged_in": True, "name": "Utilisateur"})
        st.rerun()
else:
    # Appel de tes vues ici...
    st.write(f"Bonjour {st.session_state.name}")