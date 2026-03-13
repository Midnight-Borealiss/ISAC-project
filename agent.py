from datetime import datetime
from db_connector import db_connector  # On utilise ton nouveau connecteur

class ISACAgent:
    def get_response(self, prompt, user_health_profile, username):
        if not prompt:
            return "Je suis ISAC. Décrivez-moi vos symptômes.", "Système"

        user_input = prompt.lower()
        
        # 1. ÉTAGE 1 : DÉTECTION D'URGENCE (TRIAGE)
        # Assure-toi que URGENCES_VITALES est défini dans ton fichier
        if any(flag in user_input for flag in URGENCES_VITALES):
            response = "⚠️ ALERTE : Vos symptômes présentent des signes de gravité. Ne restez pas seul. Contactez immédiatement les urgences (15 ou 112) ou rendez-vous au centre de secours le plus proche."
            status = "URGENCE"
            source = "Protocole de Triage Vital"
        
        # 2. ÉTAGE 2 : RECHERCHE DE BONNES PRATIQUES (ANAMNÈSE)
        else:
            # On récupère la collection 'protocols'
            protocols_col = db_connector.get_collection("protocols")
            
            # On cherche un protocole dont l'un des mots-clés correspond à la saisie
            match = None
            if protocols_col:
                match = protocols_col.find_one({"keywords": {"$in": [user_input]}})
            
            if match:
                response = match["response"]
                source = "Base de Connaissances Médicales"
                status = "CONSEIL"
            else:
                # Si inconnu, on enregistre dans 'pending_protocols' (anciennement db_manager.protocoles)
                pending_col = db_connector.get_collection("pending_protocols")
                if pending_col:
                    pending_col.insert_one({
                        "question_patient": prompt,
                        "status": "en_attente",
                        "timestamp": datetime.now(),
                        "username": username
                    })
                response = "Je note vos symptômes. En attendant l'analyse, reposez-vous et hydratez-vous. Un résumé est en cours de préparation pour votre consultation."
                source = "ISAC - Aide à la décision"
                status = "ANAMNESE"

        # 3. LOGGING MÉDICAL
        # On utilise directement la collection 'interactions' au lieu d'un db_logger séparé
        interactions_col = db_connector.get_collection("interactions")
        if interactions_col:
            interactions_col.insert_one({
                "user_id": username,
                "question": prompt,
                "reponse": response,
                "status": status,
                "source": source,
                "profil_sante": user_health_profile,
                "timestamp": datetime.now()
            })

        return response, status
isac_agent = ISACAgent()
