import os
import streamlit as st
from pymongo import MongoClient

class MongoDBConnector:
    def __init__(self):
        # On utilise st.empty() pour pouvoir effacer les messages de logs une fois fini
        status_placeholder = st.empty()
        status_placeholder.write("🔍 Analyse des secrets Streamlit...")
        
        # Récupération sécurisée
        try:
            self.uri = st.secrets["MONGO_URI"]
        except Exception:
            self.uri = os.getenv("MONGO_URI") # Pour le local
        
        if not self.uri:
            st.error("❌ MONGO_URI introuvable dans les Secrets !")
            self.client = None
            return

        try:
            status_placeholder.write("🔌 Tentative de connexion au Cluster...")
            # serverSelectionTimeoutMS est crucial pour ne pas bloquer l'interface
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            
            # Vérification réelle de la connexion
            self.client.admin.command('ping') 
            
            self.db = self.client['isac_db']
            status_placeholder.empty() # On efface les logs de debug si ça réussit
            st.sidebar.success("✅ Base de données connectée")
            
        except Exception as e:
            status_placeholder.empty()
            st.error(f"❌ Erreur réseau MongoDB : {e}")
            self.client = None

    def get_collection(self, collection_name):
        if self.client:
            return self.db[collection_name]
        return None

    def close_connection(self):
        if self.client:
            self.client.close()

# Singleton : Une seule connexion pour toute l'app
if 'db_connector' not in st.session_state:
    st.session_state.db_connector = MongoDBConnector()

db_connector = st.session_state.db_connector