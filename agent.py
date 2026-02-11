from db_connector import mongo_db

class IsmailaAgent:
    # On utilise 'prompt' comme nom d'argument pour correspondre à ton appel
    def get_response(self, prompt, user_profile, username):
        
        # 1. On s'assure que le prompt n'est pas vide
        if not prompt:
            return "Comment puis-je vous aider ?", "Système"

        # 2. Recherche dans MongoDB (on cherche le prompt dans le champ 'question')
        # On utilise $regex avec l'option 'i' pour ignorer la casse (Majuscules/Minuscules)
        match = mongo_db.contributions.find_one({
            "question": {"$regex": prompt.strip(), "$options": "i"},
            "status": "validé"
        })

        # 3. Vérification du résultat
        if match and match.get("response"):
            return match["response"], "Base de connaissances interne"

        # 4. Si aucune réponse validée n'est trouvée
        return "Je n'ai pas trouvé de réponse officielle validée pour cette question. Je transmets votre demande aux administrateurs.", "IA ISMaiLa"

# On instancie l'agent pour qu'il soit importable
ismaila_agent = IsmailaAgent()