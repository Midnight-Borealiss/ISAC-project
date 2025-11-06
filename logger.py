# logger.py (VERSION FINALE ET SÉCURISÉE)

from datetime import datetime
import streamlit as st
from pyairtable import Table
import pytz

# --- INITIALISATION GLOBALE ET DÉFENSSIVE ---
# Ces variables DOIVENT être définies, même à None, pour éviter l'erreur NameError.
AIRTABLE_LOGS_TABLE = None
AIRTABLE_NEW_QUESTIONS_TABLE = None
IS_AIRTABLE_READY = False

# --- CONFIGURATION AIRTABLE (Chargement sécurisé et mis en cache) ---

@st.cache_resource
def get_airtable_table(table_name):
    """Charge un objet Table Airtable en toute sécurité et le met en cache."""
    try:
        api_key = st.secrets["airtable"]["API_KEY"]
        base_id = st.secrets["airtable"]["BASE_ID"]
        
        # Vérification simple de l'existence des clés
        if not api_key or not base_id or not table_name:
            print(f"Airtable: Clés ou nom de table '{table_name}' manquants dans les secrets.")
            return None

        # Tente de créer l'objet Table (là où l'erreur d'API peut se produire)
        table = Table(api_key, base_id, table_name)
        print(f"Airtable: Table '{table_name}' chargée avec succès.")
        return table

    except Exception as e:
        # Si le chargement des secrets échoue ou l'initialisation de Table plante
        print(f"================================================================")
        print(f"!!! ÉCHEC CRITIQUE DE LA CONFIGURATION AIRTABLE !!!")
        print(f"Table: {table_name}")
        print(f"Erreur: {e}") 
        print(f"Vérifiez l'API_KEY et BASE_ID dans secrets.toml.")
        print(f"================================================================")
        return None

# --- Récupération des objets Table ---
try:
    # On utilise le try/except ici pour intercepter les erreurs de "KeyError" si le bloc [airtable] manque
    LOGS_TABLE_NAME = st.secrets["airtable"]["TABLE_LOGS"] 
    NEW_QUESTIONS_TABLE_NAME = st.secrets["airtable"]["TABLE_NEW_QUESTIONS"]
except KeyError:
    LOGS_TABLE_NAME = None
    NEW_QUESTIONS_TABLE_NAME = None

# Les objets Table sont récupérés ici, et grâce à l'initialisation au début, 
# même si cette partie plante, les variables existent (elles seront None).
AIRTABLE_LOGS_TABLE = get_airtable_table(LOGS_TABLE_NAME)
AIRTABLE_NEW_QUESTIONS_TABLE = get_airtable_table(NEW_QUESTIONS_TABLE_NAME)

# L'indicateur de préparation est maintenant basé sur la réussite du chargement
IS_AIRTABLE_READY = AIRTABLE_LOGS_TABLE is not None and AIRTABLE_NEW_QUESTIONS_TABLE is not None



# --- FONCTIONS DE JOURNALISATION ---

def log_to_airtable(table_obj, fields):
    """Fonction générique pour enregistrer une ligne dans une table Airtable."""
    if not IS_AIRTABLE_READY:
        print("Airtable non prêt. Log ignoré.")
        return

    if table_obj is None:
        print(f"Airtable: L'objet Table cible est None pour les données: {fields}. Log ignoré.")
        return

    try:
        # Enregistrement des données
        table_obj.create(fields)

    except Exception as e:
        # Affiche l'erreur complète de l'API Airtable dans les logs Streamlit
        print(f"================================================================")
        print(f"!!! ERREUR D'ÉCRITURE AIRTABLE !!!")
        print(f"Table: {getattr(table_obj, '_table_name', 'INCONNU')}")
        print(f"Détails de l'erreur Airtable: {e}") 
        print(f"Vérifiez les noms de colonnes et les types de champs Airtable.")
        print(f"Données envoyées: {fields}")
        print(f"================================================================")

# Crée un horodatage avec le fuseau horaire (UTC ou autre)
current_time = datetime.now(pytz.utc).isoformat()
# OU si vous voulez l'heure de Dakar (plus sûr avec l'API)
# current_time = datetime.now(pytz.timezone('Africa/Dakar')).isoformat()

def log_connection_event(event_type: str, username: str, name: str, profile: str):
    """Enregistre un événement de connexion ou de déconnexion dans la table 'Logs'."""
    fields = {
        "Timestamp": datetime.now(pytz.utc).isoformat(),
        "Type": event_type, 
        "Email": username,
        "Nom": name,
        "Profile": profile
    }
    log_to_airtable(AIRTABLE_LOGS_TABLE, fields)


def log_interaction(user_question: str, bot_response: str, is_handled: bool, profile: str = "GUEST", username: str = "unknown"):
    """Enregistre une interaction (question/réponse) dans la table 'Logs'."""
    fields = {
        "Timestamp": datetime.now(pytz.utc).isoformat(),
        "Type": "INTERACTION",
        "Email": username,
        "Profile": profile,
        "Question": user_question,
        "Réponse": bot_response,
        "Géré": is_handled 
    }
    log_to_airtable(AIRTABLE_LOGS_TABLE, fields)


def log_unhandled_question(user_question: str, profile: str, username: str):
    """Enregistre les questions sans réponse trouvée dans la table 'New_Questions'."""
    fields = {
        "Date": current_time, 
        "Question": user_question,
        "Email": username,
        "Profile": profile,
        "Statut": "À Traiter" 
    }
    log_to_airtable(AIRTABLE_NEW_QUESTIONS_TABLE, fields)