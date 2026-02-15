import streamlit as st
from db_connector import db_manager
from datetime import datetime

def render_health_page():
    st.title("📅 Mon Bilan & Prévention")
    
    tab1, tab2 = st.tabs(["📝 Déclarer un Symptôme", "🔔 Mes Rappels"])

    with tab1:
        st.subheader("Bilan pour le médecin")
        with st.form("health_form"):
            symptome = st.selectbox("Symptôme principal", ["Douleur", "Fièvre", "Toux", "Fatigue", "Autre"])
            description = st.text_area("Détails supplémentaires (Ex: douleur pulsatile, aggravée par le bruit)")
            intensite = st.select_slider("Intensité de la douleur", options=range(1, 11))
            
            if st.form_submit_button("Enregistrer le bilan"):
                # Sauvegarde dans la collection 'consultations'
                db_manager.save_anamnese(st.session_state.username, {
                    "symptome": symptome,
                    "description": description,
                    "intensite": intensite,
                    "metrics": st.session_state.get("health_metrics")
                })
                st.success("✅ Votre bilan a été enregistré. Vous pourrez le présenter à votre médecin.")

    with tab2:
        st.info("Prochainement : Programmation de vos rappels de vaccins et de prises de médicaments.")