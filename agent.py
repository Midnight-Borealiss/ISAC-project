# Dans streamlit_app.py
from agent import ISACAgent
from datetime import datetime
from turtle import st
from db_connector import db_connector  # On utilise ton nouveau connecteur


# Ajout de la liste manquante
URGENCES_VITALES = ["douleur thoracique", "difficulté respiratoire", "perte de connaissance", "avc", "infarctus", "hémorragie"]

class ISACAgent:
    def get_response(self, prompt, user_health_profile, username):
        if not prompt:
            return "Je suis ISAC. Décrivez-moi vos symptômes.", "Système"

        user_input = prompt.lower()
        
        # 1. ÉTAGE 1 : DÉTECTION D'URGENCE
        if any(flag in user_input for flag in URGENCES_VITALES):
            response = "⚠️ ALERTE : Vos symptômes présentent des signes de gravité. Contactez immédiatement le 15 ou le 112."
            status = "URGENCE"
            source = "Protocole de Triage Vital"
        
        # 2. ÉTAGE 2 : RECHERCHE DE BONNES PRATIQUES
        else:
            protocols_col = db_connector.get_collection("protocols")
            match = protocols_col.find_one({"keywords": {"$in": [user_input]}}) if protocols_col is not None else None
            
            if match:
                response = match["response"]
                source = "Base de Connaissances Médicales"
                status = "CONSEIL"
            else:
                pending_col = db_connector.get_collection("pending_protocols")
                if pending_col is not None:
                    pending_col.insert_one({
                        "question_patient": prompt,
                        "status": "en_attente",
                        "timestamp": datetime.now(),
                        "username": username
                    })
                response = "Je note vos symptômes. Un résumé est en cours de préparation pour votre consultation."
                source = "ISAC - Aide à la décision"
                status = "ANAMNESE"

        # 3. LOGGING
        interactions_col = db_connector.get_collection("interactions")
        if interactions_col is not None:
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
@st.cache_resource
def get_isac_agent():
    return ISACAgent()

    
