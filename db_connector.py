import os
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import streamlit as st

# Récupération de l'URI depuis les secrets de Streamlit
try:
    # Dans Streamlit Cloud, on utilise st.secrets
    MONGO_URI = st.secrets["MONGO_URI"]
    client = MongoClient(MONGO_URI)
    # On définit mongo_db pour qu'il soit exportable
    mongo_db = client["ismaila_db"] 
    
    # Test de connexion rapide
    client.admin.command('ping')
except Exception as e:
    st.error(f"Erreur de connexion MongoDB : {e}")
    mongo_db = None

try:
    mongo_db.command('ping')
    print("✅ Connexion MongoDB réussie")
except Exception as e:
    print(f"❌ Erreur MongoDB : {e}")

class MongoManager:
    def __init__(self):
        # Récupère l'URI de connexion depuis les secrets Streamlit (Cloud) ou variables d'environnement (Local)
        self.uri = st.secrets["MONGO_URI"] if "MONGO_URI" in st.secrets else os.getenv("MONGO_URI")
        self.client = MongoClient(self.uri)
        self.db = self.client['ismaila_db']
        # Collections
        self.logs = self.db['logs']
        self.contributions = self.db['contributions']

    def log_event(self, event_type, email, name, details=""):
        """Enregistre chaque action importante (Login, Question) dans la collection logs."""
        self.logs.insert_one({
            "event_type": event_type,
            "user_email": email,
            "user_name": name,
            "details": details,
            "timestamp": datetime.now()
        })

    def add_contribution(self, question, response, user_name, user_email, category="Autre"):
        """Ajoute une nouvelle proposition (question ou réponse) dans la base de données."""
        return self.contributions.insert_one({
            "question": question,
            "response": response,
            "user_name": user_name,
            "user_email": user_email,
            "category": category,
            "status": "en_attente", # Par défaut, nécessite une validation admin
            "timestamp": datetime.now()
        })

    def get_contributions(self, status="en_attente"):
        """Récupère la liste des contributions filtrées par statut (ex: en_attente ou valide)."""
        return list(self.contributions.find({"status": status}))

    def validate_contribution(self, contrib_id):
        """Change le statut d'une contribution à 'valide' pour qu'elle soit utilisée par le chatbot."""
        return self.contributions.update_one(
            {"_id": ObjectId(contrib_id)},
            {"$set": {"status": "valide", "validated_at": datetime.now()}}
        )

# Instance unique pour être utilisée partout dans le projet
mongo_db = MongoManager()