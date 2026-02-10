from db_connector import mongo_db
from datetime import datetime

class ContributionService:
    @staticmethod
    def submit_question(question, user_name, user_email, category):
        """Soumet une question brute sans réponse."""
        return mongo_db.contributions.insert_one({
            "question": question,
            "response": "",
            "user_name": user_name,
            "user_email": user_email,
            "category": category,
            "status": "en_attente",
            "timestamp": datetime.now()
        })

    @staticmethod
    def get_validated_for_rag():
        """Récupère uniquement les données prêtes pour le RAG (Validées)."""
        return list(mongo_db.contributions.find({"status": "valide"}))

contribution_service = ContributionService()