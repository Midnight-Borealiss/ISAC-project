# logger.py

from datetime import datetime
import streamlit as st
from pyairtable import Table
import pytz 

# --- CONFIGURATION (Non modifiée) ---
AIRTABLE_LOGS_STAGING = None
AIRTABLE_NEW_QUESTIONS = None
IS_READY = False
# ... (Configuration Airtable/Secrets non modifiée)

try:
    API_KEY = st.secrets["airtable"]["API_KEY"]
    BASE_ID = st.secrets["airtable"]["BASE_ID"]
    TABLE_STAGING = "Logs_Staging"
    TABLE_NEW = st.secrets["airtable"]["TABLE_NEW_QUESTIONS"]
    
    AIRTABLE_LOGS_STAGING = Table(API_KEY, BASE_ID, TABLE_STAGING)
    AIRTABLE_NEW_QUESTIONS = Table(API_KEY, BASE_ID, TABLE_NEW)
    IS_READY = True
except Exception as e:
    print(f"LOGGER ERROR: Configuration échouée: {e}")
    IS_READY = False

def safe_log(table, fields):
    if not IS_READY or not table:
        return
    try:
        table.create(fields)
    except Exception as e:
        print(f"LOGGER ERROR: Écriture échouée dans {table.table_name}: {e}")

# --- FONCTIONS PUBLIQUES ---

def log_connection_event(event_type: str, username: str, name: str, profile: str):
    """Log connexion/déconnexion vers Logs_Staging."""
    fields = {
        # MODIFICATION ICI : Utilisation de strftime pour un format lisible
        "Timestamp": datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S'), 
        "Type": str(event_type),
        "Email": str(username),
        "Nom": str(name),
        "Profile": str(profile),
        "Question": "",
        "Réponse": "",
        "Géré": "False"
    }
    safe_log(AIRTABLE_LOGS_STAGING, fields)

def log_interaction(user_question: str, bot_response: str, is_handled: bool, profile: str, username: str):
    """Log interaction vers Logs_Staging."""
    fields = {
        # MODIFICATION ICI : Utilisation de strftime pour un format lisible
        "Timestamp": datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S'), 
        "Type": "INTERACTION",
        "Email": str(username),
        "Nom": st.session_state.get("name", ""),
        "Profile": str(profile),
        "Question": str(user_question),
        "Réponse": str(bot_response),
        "Géré": str(is_handled) 
    }
    safe_log(AIRTABLE_LOGS_STAGING, fields)

def log_unhandled_question(user_question: str, profile: str, username: str):
    """Log question non traitée vers New_Questions."""
    fields = {
        # MODIFICATION ICI : Utilisation de strftime pour un format lisible
        "Date": datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S'),
        "Question": str(user_question),
        "Email": str(username),
        "Profile": str(profile),
        "Statut": "À Traiter"
    }
    safe_log(AIRTABLE_NEW_QUESTIONS, fields)
