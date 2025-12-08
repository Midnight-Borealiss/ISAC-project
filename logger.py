# logger.py

from datetime import datetime
import streamlit as st
from pyairtable import Table
import pytz 

# --- CONFIGURATION ---
# Initialisation à None pour être sûr que l'état est connu
AIRTABLE_LOGS_STAGING = None 
AIRTABLE_NEW_QUESTIONS = None
IS_READY = False

try:
    # Récupération des secrets
    API_KEY = st.secrets["airtable"]["API_KEY"]
    BASE_ID = st.secrets["airtable"]["BASE_ID"]
    TABLE_STAGING = "LOGS_STAGING" # Vérifiez l'orthographe exacte dans Airtable !
    TABLE_NEW = st.secrets["airtable"]["TABLE_NEW_QUESTIONS"]
    
    # Tentative d'initialisation des tables
    AIRTABLE_LOGS_STAGING = Table(API_KEY, BASE_ID, TABLE_STAGING)
    AIRTABLE_NEW_QUESTIONS = Table(API_KEY, BASE_ID, TABLE_NEW)
    
    # Si nous arrivons ici, la configuration a réussi
    IS_READY = True 

except Exception as e:
    # Affiche l'erreur si les clés ou les tables sont mal configurées
    # Cette erreur est la cause de l'échec d'initialisation.
    print(f"LOGGER CONFIGURATION FAILED: {e}")
    IS_READY = False

def safe_log(table, fields):
    """Fonction d'écriture générique sécurisée vers Airtable."""
    
    # 1. Vérifie si l'initialisation a réussi ET si l'objet table est bien un objet
    if not IS_READY or table is None:
        print("LOGGER ERROR: Skipped logging because Airtable connection failed during startup.")
        return
        
    try:
        # Tente d'envoyer l'enregistrement
        table.create(fields)
    except Exception as e:
        # MODIFICATION : Nous imprimons ici le VRAI message d'erreur Airtable (e)
        # SANS CRASHER sur table.table_name, car nous savons que l'objet table existe
        # (sinon le premier if l'aurait attrapé)
        print(f"LOGGER ERROR: Écriture vers {table.table_name} échouée. Message Airtable: {e}")


# --- Le reste des fonctions de log (inchangé) ---

def log_connection_event(event_type: str, username: str, name: str, profile: str):
    fields = {
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
    fields = {
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
    fields = {
        "Date": datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S'),
        "Question": str(user_question),
        "Email": str(username),
        "Profile": str(profile),
        "Statut": "À Traiter"
    }
    safe_log(AIRTABLE_NEW_QUESTIONS, fields)