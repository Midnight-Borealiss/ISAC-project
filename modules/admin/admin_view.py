import streamlit as st
from db_connector import mongo_db
import pandas as pd

def render_admin():
    """Vue pour l'administration et la validation RAG"""
    st.title("🛡️ Panel de Modération")
    
    t1, t2, t3 = st.tabs(["✅ Valider Contributions", "📊 Statistiques", "⚙️ Export RAG"])

    with t1:
        st.subheader("Vérification des réponses")
        # Récupère les contributions ayant une réponse mais non encore validées
        to_check = list(mongo_db.contributions.find({"response": {"$ne": ""}, "status": "en_attente"}))
        
        for item in to_check:
            with st.container(border=True):
                st.markdown(f"**Q:** {item['question']}")
                st.markdown(f"**R:** {item['response']}")
                st.caption(f"Par: {item.get('respondent', 'Anonyme')}")
                
                c1, c2 = st.columns(2)
                if c1.button("✅ Approuver (Ajouter au RAG)", key=f"v_{item['_id']}"):
                    mongo_db.validate_contribution(item['_id'])
                    st.success("Validé !")
                    st.rerun()
                if c2.button("❌ Rejeter", key=f"r_{item['_id']}"):
                    mongo_db.contributions.delete_one({"_id": item["_id"]})
                    st.rerun()

    with t2:
        st.subheader("Logs système")
        logs = pd.DataFrame(list(mongo_db.logs.find()))
        if not logs.empty:
            st.dataframe(logs.sort_values("timestamp", ascending=False))

    with t3:
        st.subheader("Préparation du passage au RAG")
        if st.button("Générer fichier d'entraînement JSON"):
            # Simulation d'export pour éprouver la FAQ avant le RAG
            valid_items = list(mongo_db.contributions.find({"status": "valide"}))
            st.download_button(
                label="Télécharger JSON pour RAG",
                data=str(valid_items),
                file_name="rag_training_data.json",
                mime="application/json"
            )