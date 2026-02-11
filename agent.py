from db_connector import mongo_db

class IsmailaAgent:
    # On utilise 'prompt' comme nom d'argument pour correspondre à ton appel
    def get_response(self, prompt, user_profile, username):
        
        # 1. On s'assure que le prompt n'est pas vide
        if not prompt:
            return "Comment puis-je vous aider ?", "Système"

        # 2. Recherche dans MongoDB (on cherche le prompt dans le champ 'question')
        # On utilise $regex avec l'option 'i' pour ignorer la casse (Majuscules/Minuscules)
        # Dans agent.py
        match = mongo_db.contributions.find_one({
            "question": {"$regex": prompt.strip(), "$options": "i"},
            "status": "valide"  # Changé de "validé" à "valide" pour correspondre à db_connector.py
        })

        # 3. Vérification du résultat
        if match and match.get("response"):
            return match["response"], "Base de connaissances interne"

        # --- NOUVELLE LOGIQUE : AUTO-AJOUT ---
        # Si on arrive ici, c'est qu'aucune réponse n'a été trouvée
    
         # On vérifie si la question n'existe pas déjà en attente pour éviter les doublons
        existing = mongo_db.contributions.find_one({"question": prompt.strip(), "status": "en_attente"})
    
        if not existing:
            mongo_db.add_contribution(
        question=prompt.strip(),
        response="En attente de réponse...", # Message par défaut pour l'admin
        user_name=username,
        user_email="auto@ismaila.ai",
        category="Question non répondue"
        )

        return "Je n'ai pas trouvé de réponse officielle. Votre question a été transmise aux administrateurs pour validation.", "IA ISMaiLa"

# On instancie l'agent pour qu'il soit importable
ismaila_agent = IsmailaAgent()