import streamlit as st
from db_connector import mongo_db

def render_contribution_page():
    """Fonction principale de l'onglet Contribution."""
    st.title("🌍 Hub de Contribution ISMaiLa")
    st.markdown("Aidez la communauté en enrichissant la base de connaissances.")

    # Création de deux sous-onglets pour organiser l'espace
    tab_ask, tab_answer = st.tabs(["❓ Proposer une Question", "💬 Répondre à un étudiant"])

    with tab_ask:
        st.subheader("Soumettre une nouvelle interrogation")
        with st.form("new_question_form"):
            q = st.text_area("Quelle question manque-t-il à ISMaiLa ?", placeholder="Ex: Comment obtenir mon relevé de notes ?")
            cat = st.selectbox("Catégorie", ["Académique", "Administratif", "Vie Étudiante", "Autre"])
            if st.form_submit_button("Envoyer la suggestion"):
                if q:
                    # Enregistrement dans MongoDB (sans réponse pour l'instant)
                    mongo_db.add_contribution(q, "", st.session_state.name, st.session_state.username, cat)
                    st.success("✅ Question enregistrée ! Elle apparaîtra bientôt dans la liste des questions à répondre.")
                else:
                    st.error("Veuillez écrire une question.")

    with tab_answer:
        st.subheader("Questions en attente de réponse")
        # On cherche les questions qui n'ont pas encore de réponse
        pending = list(mongo_db.contributions.find({"response": "", "status": "en_attente"}))
        
        if not pending:
            st.info("Toutes les questions ont été traitées ! Revenez plus tard.")
        else:
            for item in pending:
                # Utilisation d'un container avec bordure pour chaque question
                with st.container(border=True):
                    st.write(f"**Question :** {item['question']}")
                    st.caption(f"Posté par {item['user_name']} le {item['timestamp'].strftime('%d/%m')}")
                    
                    # Formulaire de réponse spécifique à chaque ID unique
                    with st.form(key=f"ans_{item['_id']}"):
                        ans = st.text_area("Votre réponse :")
                        if st.form_submit_button("Soumettre la réponse"):
                            if ans:
                                # Mise à jour du document dans MongoDB
                                mongo_db.contributions.update_one(
                                    {"_id": item["_id"]},
                                    {"$set": {"response": ans, "respondent": st.session_state.name}}
                                )
                                st.success("Réponse envoyée à l'administration pour validation !")
                                st.rerun()