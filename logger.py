# logger.py (VERSION GOOGLE SHEETS)

from datetime import datetime
import streamlit as st
import pytz # À garder pour l'horodatage UTC
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# --- CONFIGURATION (Réutilisation de la fonction de db_connector) ---
# NOTE: Dans un vrai projet, ces fonctions de secrets seraient dans un fichier 'config' partagé.

@st.cache_resource
def get_service_account_credentials():
    """Charge les credentials du compte de service GSheets."""
    try:
        # 1. Copie du dictionnaire secrets (Solution à la TypeError)
        gsheet_secrets = dict(st.secrets["gsheets"]) # <-- CRÉATION D'UNE COPIE MODIFIABLE
        
        # 2. Correction de la clé privée (maintenant autorisé sur la COPIE)
        # La valeur de 'private_key' est une chaîne, et doit être modifiée.
        gsheet_secrets["private_key"] = gsheet_secrets["private_key"].replace('\\n', '\n')
        
        return gsheet_secrets
    except KeyError as e:
        print(f"DEBUG: La section 'gsheets' ou une clé manque dans secrets.toml: {e}")
        return None


# --- ACCÈS AUX DONNÉES EN ÉCRITURE (Logs) ---

def log_to_gsheets(sheet_name: str, data: list):
    """Écrit une ligne de données dans l'onglet spécifié."""
    
    credentials = get_service_account_credentials()
    if not credentials:
        print(f"LOGS: Échec d'écriture dans GSheets. Credentials manquants.")
        return

    try:
        # 1. Authentification
        gc = gspread.service_account_from_dict(credentials)
        
        # 2. Ouverture du document et de l'onglet
        sh = gc.open_by_url(st.secrets["gsheets"]["sheet_url"])
        worksheet = sh.worksheet(sheet_name) # Nom de l'onglet

        # 3. Écriture (append_row est la plus simple)
        worksheet.append_row(data)
        
    except Exception as e:
        # Capture l'échec d'écriture (ex: noms de colonnes/permissions de partage)
        print(f"==================================================================")
        print(f"!!! ÉCHEC D'ÉCRITURE dans l'onglet '{sheet_name}' !!!")
        print(f"CAUSE PROBABLE: Feuille non partagée avec le Compte de Service ou nom de colonnes/onglet erroné.")
        print(f"ERREUR DÉTAILLÉE : {e}")
        print(f"==================================================================")


# --- FONCTIONS DE LOG APPLICATIVES ---

def log_connection_event(event_type: str, username: str, name: str, profile: str):
    """Enregistre un événement de connexion ou de déconnexion dans la table 'Logs'."""
    # Les données sont envoyées sous forme de liste, dans l'ordre EXACT des colonnes de l'onglet 'Logs'.
    # ORDRE DES COLONNES DANS VOTRE SHEET 'Logs' : Timestamp, Type, Email, Nom, Profile, Question, Réponse, Géré
    
    current_time_utc = datetime.now(pytz.utc).isoformat()
    
    # Remplir les colonnes Question/Réponse/Géré avec des valeurs vides pour un log de connexion
    data = [
        current_time_utc,
        event_type, 
        username,
        name,
        profile,
        "",  # Question
        "",  # Réponse
        ""   # Géré
    ]
    log_to_gsheets("Logs", data)


def log_interaction(user_question: str, bot_response: str, is_handled: bool, profile: str = "GUEST", username: str = "unknown"):
    """Enregistre une interaction (question/réponse) dans la table 'Logs'."""
    # ORDRE DES COLONNES DANS VOTRE SHEET 'Logs' : Timestamp, Type, Email, Nom, Profile, Question, Réponse, Géré
    
    current_time_utc = datetime.now(pytz.utc).isoformat()
    
    data = [
        current_time_utc,
        "INTERACTION",
        username,
        "", # Nom (non utilisé dans log_interaction)
        profile,
        user_question,
        bot_response,
        str(is_handled) # Le booléen doit être converti en texte
    ]
    log_to_gsheets("Logs", data)


def log_unhandled_question(user_question: str, profile: str, username: str):
    """Enregistre les questions sans réponse trouvée dans la table 'New_Questions'."""
    # ORDRE DES COLONNES DANS VOTRE SHEET 'New_Questions' : Date, Question, Email, Profile, Statut
    
    current_time_utc = datetime.now(pytz.utc).isoformat()
    
    data = [
        current_time_utc,
        user_question, 
        username,
        profile,
        "À traiter"
    ]
    log_to_gsheets("New_Questions", data)