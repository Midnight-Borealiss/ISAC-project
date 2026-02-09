import st
from db_connector import mongo_db

class IsmailaAgent:
    def get_response(self, user_query, user_profile, user_email):
        """
        Cherche d'abord une réponse validée dans MongoDB.
        Si rien n'est trouvé, l'IA prend le relais.
        """
        # Recherche simple par mot-clé dans les contributions validées
        match = mongo_db.contributions.find_one({
            "status": "valide",
            "question": {"$regex": user_query, "$options": "i"}
        })

        if match:
            # On enregistre que le bot a trouvé une réponse validée
            mongo_db.log_event("CHAT_SUCCESS_DB", user_email, "System", f"Match: {match['_id']}")
            return f"✅ **Réponse Officielle :**\n\n{match['response']}", "database"

        # LOGIQUE IA (À adapter selon ton modèle : OpenAI ou Gemini)
        # Ici, on simule une réponse si rien n'est trouvé en base
        response_ia = "Désolé, je n'ai pas de réponse officielle à ce sujet. Je transmets votre question aux contributeurs !"
        
        # Enregistre que l'IA a été sollicitée
        mongo_db.log_event("CHAT_IA_FALLBACK", user_email, "System", f"Q: {user_query}")
        
        return response_ia, "llm"

ismaila_agent = IsmailaAgent()