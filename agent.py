# agent.py
import streamlit as st
from db_connector import mongo_db

class IsmailaAgent:
    def get_response(self, user_query, user_profile, username):
        """Recherche une réponse validée dans MongoDB"""
        
        # 1. On cherche une correspondance exacte ou partielle dans les questions validées
        # On ignore les questions "en_attente" pour garantir la qualité
        match = mongo_db.contributions.find_one({
            "question": {"$regex": user_query, "$options": "i"},
            "status": "validé"  # <--- LE FILTRE CRUCIAL
        })

        if match and match.get("response"):
            return match["response"], "Base de connaissances interne"

        # 2. Si pas de match, on peut basculer sur l'IA (LLM) ou une réponse par défaut
        # Ici, tu peux appeler OpenAI, Gemini ou ton propre moteur RAG
        return "Je n'ai pas encore de réponse validée pour cette question, mais je la transmets à mes administrateurs !", "IA ISMaiLa"

# Instance pour l'import
ismaila_agent = IsmailaAgent()