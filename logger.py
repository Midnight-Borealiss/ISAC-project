# logger.py

from datetime import datetime
import logging
import json
import os
import time
import traceback
import streamlit as st
from pyairtable import Table
import pytz
from typing import Optional

# --- CONFIGURATION ---
AIRTABLE_LOGS_STAGING: Optional[Table] = None
AIRTABLE_NEW_QUESTIONS: Optional[Table] = None
IS_READY = False

# Logger standardisé pour la traçabilité localement et dans stdout
logger = logging.getLogger("chatbot_logger")
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(ch)
logger.setLevel(logging.INFO)


def _write_local_fallback(fields: dict, error: Optional[BaseException] = None) -> None:
    """Écrit un fallback log local (JSON) quand Airtable n'est pas disponible."""
    try:
        os.makedirs("logs", exist_ok=True)
        record = {
            "timestamp": datetime.now(pytz.utc).isoformat(),
            "fields": fields,
            "error": repr(error) if error else None,
            "traceback": traceback.format_exc() if error else None
        }
        path = os.path.join("logs", "airtable_fallback.log")
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        logger.warning("Wrote fallback log to %s", path)
    except Exception:
        # Ne pas monter d'exception ici : on est déjà en situation d'erreur
        logger.exception("Failed to write local fallback log.")


try:
    # Récupération des secrets
    API_KEY = st.secrets["airtable"]["API_KEY"]
    BASE_ID = st.secrets["airtable"]["BASE_ID"]
    TABLE_STAGING = "LOGS_STAGING"
    TABLE_NEW = st.secrets["airtable"]["TABLE_NEW_QUESTIONS"]

    # Tentative d'initialisation des tables
    AIRTABLE_LOGS_STAGING = Table(API_KEY, BASE_ID, TABLE_STAGING)
    AIRTABLE_NEW_QUESTIONS = Table(API_KEY, BASE_ID, TABLE_NEW)

    IS_READY = True
    logger.info("Airtable tables initialized successfully.")
except Exception as e:
    logger.exception("LOGGER CONFIGURATION FAILED")
    IS_READY = False


def safe_log(table: Optional[Table], fields: dict, max_retries: int = 3, base_delay: float = 0.5) -> None:
    """
    Écriture sécurisée vers Airtable.
    - Retry exponentiel si l'appel échoue.
    - En cas d'échec ou si Airtable non configuré, écrit un fallback local.
    """
    if not IS_READY or table is None:
        logger.warning("Skipping remote log: Airtable not ready. Using local fallback.")
        _write_local_fallback(fields)
        return

    attempt = 0
    while attempt < max_retries:
        try:
            table.create(fields)
            logger.info("Logged to Airtable table (attempt %d).", attempt + 1)
            return
        except Exception as e:
            attempt += 1
            logger.exception("Failed to write to Airtable (attempt %d/%d).", attempt, max_retries)
            # Écrire un fallback partiel à chaque échec pour ne pas perdre les données
            _write_local_fallback(fields, error=e)
            # Exponential backoff
            time.sleep(base_delay * (2 ** (attempt - 1)))

    logger.error("All retries failed when writing to Airtable. See local fallback logs.")


# --- Fonctions de log exposées ---

def log_connection_event(event_type: str, username: str, name: str, profile: str) -> None:
    fields = {
        "Timestamp": datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S'),
        "Type": str(event_type),
        "Email": str(username),
        "Nom": str(name),
        "Profile": str(profile),
        "Question": "",
        "Réponse": "",
        "Géré": False
    }
    safe_log(AIRTABLE_LOGS_STAGING, fields)


def log_interaction(user_question: str, bot_response: str, is_handled: bool, profile: str, username: str) -> None:
    fields = {
        "Timestamp": datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S'),
        "Type": "INTERACTION",
        "Email": str(username),
        "Nom": st.session_state.get("name", ""),
        "Profile": str(profile),
        "Question": str(user_question),
        "Réponse": str(bot_response),
        "Géré": bool(is_handled)
    }
    safe_log(AIRTABLE_LOGS_STAGING, fields)


def log_unhandled_question(user_question: str, profile: str, username: str) -> None:
    fields = {
        "Date": datetime.now(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S'),
        "Question": str(user_question),
        "Email": str(username),
        "Profile": str(profile),
        "Statut": "À Traiter"
    }
    safe_log(AIRTABLE_NEW_QUESTIONS, fields)