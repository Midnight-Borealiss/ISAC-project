# db_connector.py (VERSION GOOGLE SHEETS)

import streamlit as st
import pandas as pd
import gspread # Nouveau
from oauth2client.service_account import ServiceAccountCredentials # Nouveau
from datetime import datetime
import json

# --- CONFIGURATION GOOGLE SHEETS ---

# Utilisation d'un format spécifique pour charger les secrets GSheets
@st.cache_resource
def get_service_account_credentials():
    """Charge les credentials du compte de service GSheets."""
    try:
        # Streamlit permet de charger les secrets GSheets directement
        # en utilisant le format du fichier JSON
        gsheet_secrets = st.secrets["gsheets"]
        
        # Le secret "private_key" est le seul qui a besoin d'être traité
        # pour s'assurer que les retours à la ligne sont rétablis
        gsheet_secrets["private_key"] = gsheet_secrets["private_key"].replace('\\n', '\n')
        
        return gsheet_secrets
    except KeyError as e:
        print(f"DEBUG DB: La section 'gsheets' ou une clé manque dans secrets.toml: {e}")
        return None

# --- ACCÈS AUX DONNÉES EN LECTURE (FAQ) ---

@st.cache_resource(ttl=3600) # Rafraîchit la base toutes les heures
def get_knowledge_base():
    """Charge la base de connaissances (onglet 'FAQ') depuis Google Sheets."""
    knowledge_base = []
    for entry in knowledge_base:
            # VÉRIFIEZ L'ORTHOGRAPHE ICI
            entry['question'] = entry.get('question', '') # <-- CORRESPOND À VOTRE COLONNE DANS SHEETS
            entry['reponse'] = entry.get('reponse', '')  # <-- CORRESPOND À VOTRE COLONNE DANS SHEETS
            entry['formulations'] = entry.get('formulations', '') # Si ce champ existe
    try:
        # 1. Authentification
        credentials = get_service_account_credentials()
        gc = gspread.service_account_from_dict(credentials)
        
        # 2. Ouverture du document et de l'onglet FAQ
        sh = gc.open_by_url(st.secrets["gsheets"]["sheet_url"])
        worksheet = sh.worksheet("FAQ") # Nom de l'onglet

        # 3. Lecture des données
        data = worksheet.get_all_records()
        knowledge_base = data
        
        # <<< DÉBUT DU BLOC RAG / PRÉ-TRAITEMENT >>>
        print("DEBUG DB: Démarrage du pré-traitement RAG.")
        
        for entry in knowledge_base:
            # Assurez-vous que les clés 'question' et 'réponse' existent dans votre Sheet
            entry['question'] = entry.get('Questions', '') # Utilisez vos noms de colonnes exacts
            entry['reponse'] = entry.get('Réponses', '')  # Utilisez vos noms de colonnes exacts
            entry['formulations'] = entry.get('Formulations (Input RAG)', '') # Si vous avez ce champ
            
            search_content = (
                f"{entry['question']} "
                f"{entry.get('formulations', '')} "
                f"{entry.get('mots_cles', '')}"
            )
            entry['search_text'] = search_content.lower() 
        
        print(f"DEBUG DB: Succès. Base de connaissances chargée et prête pour le RAG avec {len(knowledge_base)} entrées.")
        
    except Exception as e:
        print(f"======================================================")
        print(f"!!! ÉCHEC DE LECTURE DE LA BASE GOOGLE SHEETS FAQ !!!")
        print(f"CAUSE PROBABLE: URL incorrecte, onglet 'FAQ' manquant, ou clés JSON invalides.")
        print(f"ERREUR GSheets: {e}") 
        print(f"======================================================")
        knowledge_base = []
        
    return knowledge_base

# Le chargement est fait au démarrage
knowledge_base = get_knowledge_base()