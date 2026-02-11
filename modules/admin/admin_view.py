import streamlit as st
import pandas as pd
from db_connector import mongo_db

def render_admin_page():
    st.title("🛡️ Administration")
    t1, t2 = st.tabs(["✅ Validation", "📊 Logs d'activité"])

    with t1:
        # On cherche les documents qui ont une réponse mais qui sont encore "en_attente"
        to_check = list(mongo_db.contributions.find({
            "response": {"$ne": ""}, 
            "status": "en_attente"
        }))
        
        if not to_check:
            st.info("Aucune contribution à valider.")
            
        for item in to_check:
            with st.container(border=True):
                st.write(f"**Question :** {item['question']}")
                st.write(f"**Auteur :** {item.get('author_name')}")
                st.info(f"**Réponse proposée :** {item['response']}")
                
                c1, c2 = st.columns(2)
                if c1.button("✅ Approuver", key=f"v_{item['_id']}"):
                    mongo_db.contributions.update_one(
                        {"_id": item["_id"]}, 
                        {"$set": {"status": "validé"}}
                    )
                    st.rerun()
                if c2.button("❌ Rejeter", key=f"r_{item['_id']}"):
                    # On peut soit supprimer, soit vider la réponse
                    mongo_db.contributions.delete_one({"_id": item["_id"]})
                    st.rerun()

    with t2:
        # Affichage des derniers logs
        logs = list(mongo_db.logs.find().sort("timestamp", -1).limit(100))
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(df)
        else:
            st.write("Aucun log d'activité.")