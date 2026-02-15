import streamlit as st
from db_connector import db_manager
from bson import ObjectId
import pandas as pd

def render_admin_page():
    st.title("🛡️ Espace Praticien - Supervision ISAC")
    st.markdown("---")

    # Onglets pour le médecin
    tab1, tab2, tab3 = st.tabs(["📋 Consultations à Analyser", "📚 Protocoles & Prévention", "📊 Statistiques Sanitaires"])

    with tab1:
        st.subheader("Bilans de santé récents")
        # On récupère les dernières consultations enregistrées par les patients
        consultations = list(db_manager.consultations.find().sort("timestamp", -1).limit(20))
        
        if not consultations:
            st.info("Aucun bilan de santé n'a été soumis pour le moment.")
        else:
            for c in consultations:
                data = c.get("donnees_cliniques", {})
                metrics = data.get("metrics", {})
                
                # Couleur d'alerte selon l'intensité ou la température
                border_color = "red" if data.get("intensite", 0) >= 7 or metrics.get("temperature", 0) >= 39 else "gray"
                
                with st.container(border=True):
                    col_info, col_action = st.columns([3, 1])
                    with col_info:
                        st.write(f"**Patient :** {c.get('user_id')} | **Date :** {c.get('timestamp').strftime('%d/%m/%Y %H:%M')}")
                        st.write(f"**Symptôme :** {data.get('symptome')} (Intensité : {data.get('intensite')}/10)")
                        st.write(f"**Constantes :** {metrics.get('temperature')}°C | {metrics.get('poids')}kg | {metrics.get('age')} ans")
                        st.text_area("Observations du patient :", data.get("description"), disabled=True)
                    
                    with col_action:
                        st.button("Générer Rapport PDF 📄", key=f"pdf_{c['_id']}")
                        if st.button("Archiver ✅", key=f"arc_{c['_id']}"):
                            # Logique d'archivage ici
                            st.success("Consultation archivée")

    with tab2:
        st.subheader("Gestion des Bonnes Pratiques")
        st.info("Ajoutez ou validez des conseils qui seront donnés automatiquement par ISAC.")
        
        # Formulaire pour ajouter un nouveau conseil médical
        with st.expander("➕ Ajouter un nouveau protocole"):
            with st.form("new_protocol"):
                mots_cles = st.text_input("Mots-clés (séparés par des virgules)", placeholder="ex: tête, migraine, céphalée")
                conseil = st.text_area("Bonne pratique / Conseil à donner")
                red_flags = st.text_input("Drapeaux Rouges (Urgence)", placeholder="ex: évanouissement, paralysie")
                
                if st.form_submit_button("Enregistrer le protocole"):
                    db_manager.protocoles.insert_one({
                        "keywords": mots_cles,
                        "response": conseil,
                        "red_flags": red_flags.split(","),
                        "status": "valide",
                        "validated_by": st.session_state.name
                    })
                    st.success("Nouveau protocole ajouté à l'intelligence d'ISAC !")

    with tab3:
        # Intégration du dashboard analytique adapté à la santé
        st.subheader("Analyse des pathologies fréquentes")
        
        # Petit exemple de graphique basé sur les consultations
        if consultations:
            df = pd.DataFrame([
                {"Symptôme": c.get("donnees_cliniques", {}).get("symptome"), "Date": c.get("timestamp")} 
                for c in consultations
            ])
            st.bar_chart(df["Symptôme"].value_counts())
        else:
            st.write("Pas assez de données pour les graphiques.")