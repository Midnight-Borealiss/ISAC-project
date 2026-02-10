import streamlit as st
from modules.contribution.service import contribution_service

def render_contribution():
    st.header("🌍 Espace de Contribution")
    st.info("Aidez-nous à enrichir la base de connaissances d'ISMaiLa.")

    with st.form("form_question"):
        question = st.text_area("Votre question :")
        name = st.text_input("Votre nom :")
        email = st.text_input("Votre email :")
        category = st.selectbox("Catégorie :", ["Général", "Inscription", "Cours", "Examens"])
        
        submit = st.form_submit_state = st.form_submit_button("Envoyer ma question")

        if submit:
            if question and name:
                # Appel au service que nous avons renommé
                try:
                    contribution_service.submit_question(question, name, email, category)
                    st.success("✅ Merci ! Votre question a été enregistrée et sera traitée.")
                except Exception as e:
                    st.error(f"Erreur lors de l'enregistrement : {e}")
            else:
                st.warning("Veuillez remplir au moins la question et votre nom.")