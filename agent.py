from db_connector import mongo_db
from logger import db_logger
from datetime import datetime

class IsmailaAgent:
    def get_response(self, prompt, user_profile, username):
        if not prompt:
            return "Comment puis-je vous aider ?", "Système"

        # 1. Recherche dans la base de connaissances (status: valide)
        match = mongo_db.contributions.find_one({
            "question": {"$regex": prompt.strip(), "$options": "i"},
            "status": "valide"
        })

        if match and match.get("response"):
            response = match["response"]
            source = "Base de connaissances interne"
            is_handled = True
        else:
            # 2. Si inconnu : Ajout automatique pour l'admin
            is_handled = False
            existing = mongo_db.contributions.find_one({
                "question": prompt.strip(),
                "status": "en_attente"
            })

            if not existing:
                mongo_db.add_contribution(
                    question=prompt.strip(),
                    response="En attente de réponse admin...",
                    user_name=username,
                    user_email=username,
                    category="Auto-généré"
                )
            
            response = "Je n'ai pas encore la réponse officielle. Votre question a été transmise aux administrateurs."
            source = "IA ISMaiLa"

        # 3. Logging de l'interaction
        db_logger.log_interaction(
            user_id=username,
            question=prompt,
            reponse=response,
            is_handled=is_handled,
            profil=user_profile,
            username=username
        )

        return response, source

ismaila_agent = IsmailaAgent()