import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MongoLogger:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI")
        self.client = MongoClient(self.uri)
        self.db = self.client["ismaila_db"]
        self.logs = self.db["logs_interactions"]
        self.events = self.db["events_connexion"]

    def log_interaction(self, user_id, question, reponse, is_handled, profil, username):
        doc = {
            "timestamp": datetime.now(),
            "user_id": user_id,
            "username": username,
            "profil": profil,
            "question": question,
            "reponse": reponse,
            "is_handled": is_handled,
            "type": "INTERACTION"
        }
        self.logs.insert_one(doc)

    def log_connection_event(self, event_type, username, name, profile):
        doc = {
            "timestamp": datetime.now(),
            "event": event_type,
            "username": username,
            "name": name,
            "profile": profile
        }
        self.events.insert_one(doc)

# L'instance unique exportée
db_logger = MongoLogger()