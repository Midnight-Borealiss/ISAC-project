import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Charge le .env seulement s'il existe (local)
# En ligne, Streamlit utilisera ses propres "Secrets"
if os.path.exists(".env"):
    load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Test de sécurité pour éviter le chargement infini
if not MONGO_URI:
    raise ValueError("MONGO_URI non trouvée ! Vérifiez les Secrets Streamlit.")

class MongoManager:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI")
        self.client = MongoClient(self.uri)
        self.db = self.client["ismaila_db"]
        self.faq_collection = self.db["faq"]
        self.logs_collection = self.db["logs_interactions"]

    def get_knowledge_base(self):
        """Récupère la FAQ depuis MongoDB."""
        try:
            # On récupère tout et on transforme en liste
            cursor = self.faq_collection.find({})
            return list(cursor)
        except Exception as e:
            print(f"Erreur lecture FAQ: {e}")
            return []

    def get_logs_data(self):
        """Récupère les logs pour le dashboard."""
        try:
            data = list(self.logs_collection.find({}))
            return pd.DataFrame(data)
        except Exception:
            return pd.DataFrame()

    def get_unhandled_questions(self):
        """Récupère les questions où le bot a séché."""
        try:
            # On filtre les logs où is_handled était False
            data = list(self.logs_collection.find({"is_handled": False}))
            return pd.DataFrame(data)
        except Exception:
            return pd.DataFrame()

# Instance unique pour l'app
mongo_db = MongoManager()

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000) # 5 secondes max
try:
    client.admin.command('ping')
    print("✅ MongoDB Connected")
except Exception as e:
    print(f"❌ Connection error: {e}")