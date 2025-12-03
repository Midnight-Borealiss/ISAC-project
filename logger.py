# logger.py (VERSION FINALE SÉCURISÉE AIRTABLE + STAGING)

from datetime import datetime
import streamlit as st
from pyairtable import Table
import pytz # Nécessaire pour l'horodatage UTC sécurisé

# --- INITIALISATION GLOBALE ET DÉFENSSIVE ---
# Ces variables seront remplies par get_airtable_table()
AIRTABLE_LOGS_TABLE = None
AIRTABLE_NEW_QUESTIONS_TABLE = None
IS_AIRTABLE_READY = False

# --- CONFIGURATION AIRTABLE (Chargement sécurisé et mis en cache) ---

@st.cache_resource
def get_airtable_table(table_name):
    """Charge un objet Table Airtable en toute sécurité et le met en cache."""
    global AIRTABLE_LOGS_TABLE, AIRTABLE_NEW_QUESTIONS_TABLE, IS_AIRTABLE_READY
    try:
        api_key = st.secrets["airtable"]["API_KEY"]
        base_id = st.secrets["airtable"]["BASE_ID"]
        
        # Vérification simple de l'existence des clés
        if not api_key or not base_id or not table_name:
            print(f"Airtable: Clés ou nom de table '{table_name}' manquants dans les secrets.")
            return None

        # Tente de créer l'objet Table
        table = Table(api_key, base_id, table_name)
        
        # Mettre à jour l'état de préparation des variables globales
        try:
            # Note: Si vous utilisez TABLE_LOGS_STAGING comme clé dans secrets.toml, utilisez-la ici
            if table_name == st.secrets["airtable"].get("TABLE_LOGS_STAGING", "Logs_Staging"):
                AIRTABLE_LOGS_TABLE = table
            
            if table_name == st.secrets["airtable"]["TABLE_NEW_QUESTIONS"]:
                AIRTABLE_NEW_QUESTIONS_TABLE = table
        except:
            # Protection contre les clés manquantes dans secrets
            pass
            
        IS_AIRTABLE_READY = True
        return table

    except Exception as e:
        print(f"================================================================")
        print(f"!!! ÉCHEC CRITIQUE DE LA CONFIGURATION AIRTABLE !!!")
        print(f"Erreur lors du chargement de la table '{table_name}': {e}")
        print(f"================================================================")
        IS_AIRTABLE_READY = False
        return None

# Initialisation des tables au démarrage de l'application
# Remplacez "Logs_Staging" par le nom exact de votre nouvelle table tampon
get_airtable_table("Logs_Staging") 
get_airtable_table(st.secrets["airtable"].get("TABLE_NEW_QUESTIONS", "New_Questions"))


# --- NOUVELLE FONCTION D'ÉCRITURE SÉCURISÉE ---

def log_to_airtable(table: Table, fields: dict):
    """Tente d'écrire dans la table Airtable spécifiée et gère l'échec."""
    if table is None:
        print("LOGS: Échec d'écriture. La table Airtable n'a pas pu être chargée.")
        return

    try:
        # Tente la création de l'enregistrement
        table.create(fields)
        print(f"LOGS: Écriture réussie dans la table tampon '{table.table_name}'.")
        
    except Exception as e:
        # Ce bloc empêche le plantage de l'application en cas d'erreur 403,
        # de champ manquant, ou de format incorrect.
        print(f"================================================================")
        print(f"!!! ÉCHEC D'ÉCRITURE AIRTABLE NON CRITIQUE !!!")
        print(f"Le bot continue, mais l'enregistrement de log a échoué.")
        print(f"Table: {table.table_name}")
        print(f"Erreur: {e}")
        print(f"Données envoyées (vérifiez les noms de colonnes et l'automation): {fields}")
        print(f"================================================================")


# --- FONCTIONS DE LOG APPLICATIVES (Utilisent log_to_airtable) ---
# NOTE : Ces champs doivent correspondre aux noms de colonnes de votre table STAGING.

def log_connection_event(event_type: str, username: str, name: str, profile: str):
    """Enregistre un événement de connexion/déconnexion dans la table 'Logs_Staging'."""
    fields = {
        # Envoie l'horodatage au format ISO, l'automation fera la conversion en Date/Heure
        "Timestamp": datetime.now(pytz.utc).isoformat(), 
        "Type": event_type, 
        "Email": username,
        "Nom": name,
        "Profile": profile
    }
    log_to_airtable(AIRTABLE_LOGS_TABLE, fields)


def log_interaction(user_question: str, bot_response: str, is_handled: bool, profile: str = "GUEST", username: str = "unknown"):
    """Enregistre une interaction (question/réponse) dans la table 'Logs_Staging'."""
    fields = {
        "Timestamp": datetime.now(pytz.utc).isoformat(),
        "Type": "INTERACTION",
        "Email": username,
        "Profile": profile,
        "Question": user_question,
        "Réponse": bot_response,
        # Envoie le booléen comme une chaîne (l'automation le convertira en Checkbox)
        "Géré": str(is_handled) 
    }
    log_to_airtable(AIRTABLE_LOGS_TABLE, fields)


def log_unhandled_question(user_question: str, profile: str, username: str):
    """Enregistre les questions sans réponse trouvée dans la table 'New_Questions'."""
    # Cette table n'a pas besoin de staging si elle est simple
    fields = {
        "Date": datetime.now(pytz.utc).isoformat(), 
        "Question": user_question,
        "Email": username,
        "Profile": profile,
        "Statut": "À traiter"
    }
    log_to_airtable(AIRTABLE_NEW_QUESTIONS_TABLE, fields)
