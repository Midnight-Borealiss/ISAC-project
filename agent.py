
from db_connector import db_manager
from logger import db_logger
from datetime import datetime

# LISTE DE TRIAGE (RED FLAGS)
# À enrichir selon vos recherches de "Data Scout"
URGENCES_VITALES = [
    "étouffer", "respirer", "poitrine", "inconscient", 
    "paralysie", "sang", "hémorragie", "avalé"
]

class ISACAgent:
    def get_response(self, prompt, user_health_profile, username):
        if not prompt:
            return "Je suis ISAC. Décrivez-moi vos symptômes.", "Système"

        user_input = prompt.lower()
        
        # 1. ÉTAGE 1 : DÉTECTION D'URGENCE (TRIAGE)
        if any(flag in user_input for flag in URGENCES_VITALES):
            response = "⚠️ ALERTE : Vos symptômes présentent des signes de gravité. Ne restez pas seul. Contactez immédiatement les urgences (15 ou 112) ou rendez-vous au centre de secours le plus proche."
            status = "URGENCE"
            source = "Protocole de Triage Vital"
        
        # 2. ÉTAGE 2 : RECHERCHE DE BONNES PRATIQUES (ANAMNÈSE)
        else:
            match = db_manager.get_protocol(user_input)
            
            if match:
                response = match["response"]
                source = "Base de Connaissances Médicales"
                status = "CONSEIL"
            else:
                # Si inconnu, on ne devine pas, on demande au médecin
                db_manager.protocoles.insert_one({
                    "question_patient": prompt,
                    "status": "en_attente",
                    "timestamp": datetime.now()
                })
                response = "Je note vos symptômes. En attendant l'analyse, reposez-vous et hydratez-vous. Un résumé est en cours de préparation pour votre consultation."
                source = "ISAC - Aide à la décision"
                status = "ANAMNESE"

        # 3. LOGGING MÉDICAL
        db_logger.log_interaction(
            user_id=username,
            question=prompt,
            reponse=response,
            is_handled=(status != "URGENCE"),
            profil=user_health_profile, # Contient âge, poids, etc.
            username=username
        )

        return response, source

isac_agent = ISACAgent()
