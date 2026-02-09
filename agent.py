# agent.py
import streamlit as st
from db_connector import mongo_db

class IsmailaAgent:
    def get_response(self, user_query, user_profile, user_email):
        """
        Cherche d'abord une réponse validée dans MongoDB.
        Si rien n'est trouvé, l'IA prend le relais.
        """
        try:
            # Recherche simple par mot-clé dans les contributions validées
            match = mongo_db.contributions.find_one({
                "status": "valide",
                "question": {"$regex": user_query, "$options": "i"}
            })

            if match:
                # Log du succès en base
                mongo_db.log_event("CHAT_SUCCESS_DB", user_email, "System", f"Match ID: {match['_id']}")
                return f"✅ **Réponse Officielle :**\n\n{match['response']}", "database"
        
        except Exception as e:
            print(f"Erreur recherche DB: {e}")

        # LOGIQUE IA (Fallback si rien n'est trouvé en base)
        response_ia = "Je n'ai pas encore de réponse officielle pour cette question, mais je la transmets à nos contributeurs ! En attendant, n'hésitez pas à explorer l'onglet Contribution."
        
        # Enregistre que l'IA a été sollicitée
        mongo_db.log_event("CHAT_IA_FALLBACK", user_email, "System", f"Q: {user_query}")
        
        return response_ia, "llm"

ismaila_agent = IsmailaAgent()