import streamlit as st
from db_connector import mongo_db
from datetime import datetime

class ContributionService:
    def __init__(self):
        # On vérifie si mongo_db est bien initialisé
        self.db = mongo_db

    def submit_question(self, question, author_name, author_email, category):
        if self.db is None:
            st.error("Base de données non connectée.")
            return None
            
        contribution_data = {
            "question": question,
            "author_name": author_name,
            "author_email": author_email,
            "category": category,
            "status": "en_attente",
            "created_at": datetime.now()
        }
        return self.db.contributions.insert_one(contribution_data)

# --- CETTE LIGNE EST CRUCIALE ---
# C'est elle qui crée l'objet que ton fichier view.py essaie d'importer
contribution_service = ContributionService()