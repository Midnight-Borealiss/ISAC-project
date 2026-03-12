import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement pour le développement local
load_dotenv()

class MongoDBConnector:
    def __init__(self):
        st.write("🔍 Tentative de récupération de l'URI...")
        if "MONGO_URI" in st.secrets:
            self.uri = st.secrets["MONGO_URI"]
        else:
            self.uri = os.getenv("MONGO_URI")

        if not self.uri:
            st.error("❌ URI manquante dans les secrets !")
            return

        try:
            st.write("🔌 Connexion au cluster en cours...")
            # On réduit le timeout à 2 secondes pour ne pas attendre 30s
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)
            
            # On force un test immédiat
            self.client.admin.command('ping')
            st.write("✅ Ping réussi !")
            
            self.db = self.client['isac_db']
        except Exception as e:
            st.error(f"❌ Erreur réseau ou identifiants : {e}")
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