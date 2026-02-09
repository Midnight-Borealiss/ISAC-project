"""
Admin View - Interface Streamlit pour le panel administrateur
"""

import streamlit as st
from app.controllers import AnswerController, ValidationController, QuestionController
from app.services.impl import AnswerServiceImpl, QuestionServiceImpl

# Constantes
ADMIN_PASSWORD = "admin123"
PREDEFINED_CATEGORIES = [
    "Académique",
    "Administratif",
    "Financier",
    "Autre"
]

# Initialiser les controllers et services
answer_controller = AnswerController()
validation_controller = ValidationController()
question_controller = QuestionController()

# Services pour les agrégations complexes
answer_service = AnswerServiceImpl()
question_service = QuestionServiceImpl()


import streamlit as st
import pandas as pd
from db_connector import mongo_db

def render_admin_page():
    """Interface de gestion pour les administrateurs."""
    st.title("🛡️ Administration ISMaiLa")
    
    t1, t2 = st.tabs(["✅ Modération", "📊 Statistiques"])

    with t1:
        st.subheader("Contributions à valider")
        # On récupère les questions qui ont une réponse mais ne sont pas encore validées
        to_check = list(mongo_db.contributions.find({"response": {"$ne": ""}, "status": "en_attente"}))

        if not to_check:
            st.success("Aucune contribution en attente de validation.")
        else:
            for item in to_check:
                with st.container(border=True):
                    st.write(f"**Q:** {item['question']}")
                    st.write(f"**R suggérée :** {item['response']}")
                    st.caption(f"Auteur: {item['respondent']}")
                    
                    c1, c2 = st.columns(2)
                    if c1.button("✅ Approuver", key=f"ok_{item['_id']}"):
                        # Rend la réponse officielle
                        mongo_db.validate_contribution(item['_id'])
                        st.success("Contribution ajoutée au savoir du bot !")
                        st.rerun()
                    if c2.button("❌ Supprimer", key=f"no_{item['_id']}"):
                        # Supprime si c'est une mauvaise réponse
                        mongo_db.contributions.delete_one({"_id": item["_id"]})
                        st.warning("Contribution rejetée.")
                        st.rerun()

    with t2:
        st.subheader("Analyse des logs")
        # Chargement des logs dans un tableau (DataFrame)
        df_logs = pd.DataFrame(list(mongo_db.logs.find()))
        if not df_logs.empty:
            # On affiche les statistiques globales
            st.metric("Total Interactions", len(df_logs))
            st.dataframe(df_logs.sort_values("timestamp", ascending=False), use_container_width=True)