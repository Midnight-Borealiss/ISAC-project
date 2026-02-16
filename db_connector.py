import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement pour le développement local
load_dotenv()

class MongoDBConnector:
    def __init__(self):
        """
        Initialise la connexion à MongoDB en utilisant soit les secrets Streamlit (Cloud),
        soit les variables d'environnement locales (.env).
        """
        # 1. Récupération de l'URI (Priorité à Streamlit Cloud)
        if "MONGO_URI" in st.secrets:
            self.uri = st.secrets["MONGO_URI"]
        else:
            self.uri = os.getenv("MONGO_URI")

        # 2. Vérification de la présence de l'URI
        if not self.uri:
            st.error("❌ Erreur : MONGO_URI est introuvable. Vérifiez votre fichier .env ou les Secrets Streamlit.")
            self.client = None
            return

        try:
            # 3. Établissement de la connexion
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            
            # Nom de la base de données (que nous avons configurée sur ISAC-Cluster)
            self.db = self.client['isac_db']
            
            # Test de connexion rapide
            self.client.admin.command('ping')
            
        except Exception as e:
            st.error(f"❌ Erreur de connexion à MongoDB : {e}")
            self.client = None

    def get_collection(self, collection_name):
        """Récupère une collection spécifique."""
        if self.client:
            return self.db[collection_name]
        return None

    def close_connection(self):
        """Ferme la connexion proprement."""
        if self.client:
            self.client.close()

# Instance partagée pour être utilisée dans agent.py ou streamlit_app.py
db_connector = MongoDBConnector()