import streamlit as st
from modules.contribution.service import contribution_service

def render_contribution():
    """Vue pour l'espace collaboratif"""
    st.title("🌍 Espace Contribution")
    st.info("Enrichissez ISMaiLa. Vos réponses validées alimenteront directement l'IA.")

    tab1, tab2 = st.tabs(["❓ Proposer une Question", "💬 Répondre"])

    with tab1:
        st.subheader("Soumettre une nouvelle question")
        with st.form("new_q_form"):
            q = st.text_area("Question :", placeholder="Ex: Comment s'inscrire au club robotique ?")
            cat = st.selectbox("Catégorie", ["Académique", "Administratif", "Financier", "Autre"])
            if st.form_submit_button("Envoyer la proposition"):
                if q:
                    contribution_service.submit_question(
                        q, st.session_state.name, st.session_state.username, cat
                    )
                    st.success("✅ Question enregistrée pour la communauté !")
                else:
                    st.error("La question ne peut pas être vide.")

    with tab2:
        st.subheader("Questions sans réponse")
        # On récupère les questions n'ayant pas encore de réponse via le service
        from db_connector import mongo_db
        pending = list(mongo_db.contributions.find({"response": "", "status": "en_attente"}))

        if not pending:
            st.write("Aucune question en attente. Bravo !")
        else:
            for item in pending:
                with st.container(border=True):
                    st.write(f"**Question :** {item['question']}")
                    with st.form(key=f"answer_{item['_id']}"):
                        ans = st.text_area("Votre réponse suggérée :")
                        if st.form_submit_button("Soumettre la réponse"):
                            if ans:
                                mongo_db.contributions.update_one(
                                    {"_id": item["_id"]},
                                    {"$set": {"response": ans, "respondent": st.session_state.name}}
                                )
                                st.success("Réponse envoyée pour validation !")
                                st.rerun()