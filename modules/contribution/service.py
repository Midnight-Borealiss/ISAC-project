import streamlit as st
# AJOUTE CETTE LIGNE :
from db_connector import mongo_db 

class ContributionService:
    def submit_question(self, question, author_name, author_email, category):
        if mongo_db is None:
            st.error("La base de données n'est pas connectée.")
            return
        
        contribution_data = {
            "question": question,
            "author_name": author_name,
            # ... reste de tes données
        }
        # C'est ici que mongo_db est utilisé
        return mongo_db.contributions.insert_one(contribution_data)