import streamlit as st
import pandas as pd
from db_connector import mongo_db

def render_admin_page():
    st.title("🛡️ Panel Administration")
    
    t1, t2, t3 = st.tabs(["✅ Validation", "📊 Toutes les Contributions", "📝 Logs"])

    # --- TAB 1 : ACTIONS DE VALIDATION ---
    with t1:
        st.subheader("Modération des réponses proposées")
        # On cherche uniquement ceux qui ont une réponse mais ne sont pas encore validés
        to_validate = list(mongo_db.contributions.find({
            "response": {"$ne": ""}, 
            "status": "en_attente"
        }))
        
        if not to_validate:
            st.info("Aucune réponse en attente de validation.")
        
        for item in to_validate:
            with st.container(border=True):
                st.write(f"**Question :** {item['question']}")
                st.write(f"**Réponse proposée :** {item['response']}")
                col1, col2 = st.columns(2)
                if col1.button("Approuver", key=f"app_{item['_id']}"):
                    mongo_db.contributions.update_one({"_id": item["_id"]}, {"$set": {"status": "validé"}})
                    st.rerun()
                if col2.button("Rejeter", key=f"rej_{item['_id']}"):
                    mongo_db.contributions.update_one({"_id": item["_id"]}, {"$set": {"response": "", "status": "en_attente"}})
                    st.rerun()

    # --- TAB 2 : VUE GLOBALE (CE QUE TU CHERCHES) ---
    with t2:
        st.subheader("Historique complet")
        # On récupère TOUT sans filtre
        all_data = list(mongo_db.contributions.find().sort("created_at", -1))
        
        if all_data:
            df = pd.DataFrame(all_data)
            # On nettoie l'ID pour l'affichage
            df['_id'] = df['_id'].astype(str)
            st.dataframe(df[["question", "author_name", "status", "category", "response"]])
        else:
            st.warning("La base de données est vide.")

    # --- TAB 3 : LOGS ---
    with t3:
        logs = list(mongo_db.logs.find().sort("timestamp", -1))
        if logs:
            st.table(pd.DataFrame(logs).head(20))