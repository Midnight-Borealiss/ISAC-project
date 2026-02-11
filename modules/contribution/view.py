import streamlit as st
from db_connector import mongo_db
from datetime import datetime

def render_contribution_page():
    st.title("🌍 Espace Contribution")
    
    tab1, tab2 = st.tabs(["❓ Proposer une Question", "💬 Répondre"])

    with tab1:
        with st.form("new_q"):
            q = st.text_area("Question :")
            cat = st.selectbox("Catégorie", ["Général", "Académique", "Administratif", "Autre"])
            if st.form_submit_button("Envoyer"):
                if q:
                    # On respecte tes noms de champs : author_name, author_email, etc.
                    mongo_db.contributions.insert_one({
                        "question": q,
                        "author_name": st.session_state.name,
                        "author_email": st.session_state.username,
                        "category": cat,
                        "status": "en_attente",
                        "response": "", # Important pour le filtre de réponse
                        "created_at": datetime.now()
                    })
                    st.success("Enregistré !")

    with tab2:
        # On cherche les questions sans réponse
        pending = list(mongo_db.contributions.find({"response": "", "status": "en_attente"}))
        if not pending:
            st.info("Aucune question en attente de réponse.")
            
        for item in pending:
            # On utilise author_name car c'est ton champ MongoDB
            with st.expander(f"Question de {item.get('author_name', 'Inconnu')}"):
                st.write(item['question'])
                with st.form(key=f"ans_{item['_id']}"):
                    ans = st.text_area("Votre réponse :")
                    if st.form_submit_button("Soumettre la réponse"):
                        mongo_db.contributions.update_one(
                            {"_id": item["_id"]},
                            {"$set": {
                                "response": ans, 
                                "respondent": st.session_state.name,
                                "updated_at": datetime.now()
                            }}
                        )
                        st.success("Réponse enregistrée !")
                        st.rerun()