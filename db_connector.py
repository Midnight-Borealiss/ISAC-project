
import os
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import streamlit as st

# Configuration de la connexion
try:
    MONGO_URI = st.secrets["MONGO_URI"] if "MONGO_URI" in st.secrets else os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    # CHANGEMENT : On pointe vers la base ISAC
    mongo_db_raw = client["isac_db"] 
    client.admin.command('ping')
except Exception as e:
    st.error(f"Erreur de connexion MongoDB : {e}")
    mongo_db_raw = None

class ISACDataManager:
    def __init__(self):
        self.db = mongo_db_raw
        # RENOMMAGE DES COLLECTIONS POUR LE MÉDICAL
        self.consultations = self.db['consultations'] # Anciennement logs_interactions
        self.protocoles = self.db['protocoles']       # Anciennement contributions
        self.users = self.db['users_patients']       # Profils santé

    def save_anamnese(self, user_id, data):
        """Enregistre le bilan de santé structuré"""
        doc = {
            "user_id": user_id,
            "timestamp": datetime.now(),
            "donnees_cliniques": data,
            "statut": "complet"
        }
        return self.consultations.insert_one(doc)

    def get_protocol(self, keyword):
        """Cherche une règle de triage ou une bonne pratique"""
        return self.protocoles.find_one({
            "keywords": {"$regex": keyword, "$options": "i"},
            "status": "valide"
        })

# Instance unique pour le projet ISAC
db_manager = ISACDataManager()

