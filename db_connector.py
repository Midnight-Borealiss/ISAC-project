# db_connector.py

import streamlit as st
import pandas as pd
from pyairtable import Table

# --- CONFIGURATION AIRTABLE ---
try:
    AIRTABLE_API_KEY = st.secrets["airtable"]["API_KEY"]
    AIRTABLE_BASE_ID = st.secrets["airtable"]["BASE_ID"]
    FAQ_TABLE_NAME = st.secrets["airtable"]["TABLE_FAQ"]
    
    # Noms des tables pour les logs (Staging pour l'écriture, Logs réels pour la lecture dashboard)
    LOGS_STAGING_TABLE_NAME = "Logs_Staging" 
    LOGS_REAL_TABLE_NAME = st.secrets["airtable"]["TABLE_LOGS"]
    NEW_QUESTIONS_TABLE_NAME = st.secrets["airtable"]["TABLE_NEW_QUESTIONS"]
except KeyError:
    AIRTABLE_API_KEY = None
    AIRTABLE_BASE_ID = None
    FAQ_TABLE_NAME = None
    LOGS_REAL_TABLE_NAME = None


@st.cache_resource
def get_airtable_table(table_name):
    """Charge un objet Table Airtable en toute sécurité."""
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID or not table_name:
        return None
    try:
        return Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, table_name)
    except Exception as e:
        print(f"DEBUG DB: Échec chargement table '{table_name}': {e}")
        return None

# --- CHARGEMENT DE LA BASE DE CONNAISSANCES (FAQ) ---

@st.cache_resource
def get_knowledge_base():
    """Charge et pré-traite la FAQ pour la recherche."""
    knowledge_base = []
    faq_table = get_airtable_table(FAQ_TABLE_NAME)
    
    if faq_table is None:
        return []

    try:
        records = faq_table.all()
        
        for record in records:
            fields = record.get('fields', {})
            # Création de l'entrée avec concaténation pour la recherche
            entry = fields.copy()
            entry['id'] = record['id']
            
            # Création du champ de recherche unifié (Question + Formulations + Mots-clés)
            search_content = (
                f"{fields.get('Questions', '')} "
                f"{fields.get('Formulations (Input RAG)', '')} "
                f"{fields.get('Mots-clés', '')}"
            )
            entry['search_text'] = search_content.lower()
            
            # Normalisation du champ réponse
            entry['reponse'] = fields.get('Réponses', '')
            
            knowledge_base.append(entry)
            
        print(f"DEBUG DB: {len(knowledge_base)} entrées FAQ chargées.")
        return knowledge_base
        
    except Exception as e:
        print(f"!!! ERREUR LECTURE FAQ !!! : {e}")
        return []

# Chargement au démarrage
knowledge_base = get_knowledge_base()


# --- CHARGEMENT DES DONNÉES POUR LE DASHBOARD ---

@st.cache_data(ttl=600)
def get_logs_data():
    """Charge les vrais logs (après automation) pour l'analyse."""
    # Note: On lit la table finale 'LOGS', pas le staging
    logs_table = get_airtable_table(LOGS_REAL_TABLE_NAME)
    if logs_table is None:
        return pd.DataFrame()

    try:
        records = logs_table.all()
        if not records: return pd.DataFrame()
        
        data = [r['fields'] for r in records]
        df = pd.DataFrame(data)
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_unhandled_questions():
    """Charge les questions non traitées."""
    q_table = get_airtable_table(NEW_QUESTIONS_TABLE_NAME)
    if q_table is None: return pd.DataFrame()

    try:
        records = q_table.all()
        if not records: return pd.DataFrame()
        
        data = [r['fields'] for r in records]
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()