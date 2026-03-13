import os
import streamlit as st
from pymongo import MongoClient
import os

class MongoDBConnector:
    def __init__(self):
        # LOG DE DEBUG 1
        st.write("🔍 Analyse des secrets Streamlit...")
        
        self.uri = st.secrets.get("MONGO_URI")
        
        if not self.uri:
            st.error("❌ MONGO_URI introuvable dans les Secrets !")
            self.client = None
            return

        try:
            # LOG DE DEBUG 2
            st.write("🔌 Tentative de connexion au Cluster...")
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping') # Test de réponse
            self.db = self.client['isac_db']
            st.write("✅ Cluster joint avec succès.")
        except Exception as e:
            st.error(f"❌ Erreur réseau : {e}")
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
# On crée l'instance ICI pour qu'elle soit partagée
db_connector = MongoDBConnector()

