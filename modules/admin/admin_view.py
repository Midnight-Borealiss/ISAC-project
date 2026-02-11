import streamlit as st
import pandas as pd
from db_connector import mongo_db

def render_admin_page():
    st.title("🛡️ Panel Administration")
    
    t1, t2 = st.tabs(["✅ Validation", "📊 Historique"])

    with t1:
        st.subheader("Modération des contributions")
        # On récupère les questions en attente
        to_check = list(mongo_db.contributions.find({"status": "en_attente"}))
        
        if not to_check:
            st.info("Aucune contribution à valider.")
            
        for item in to_check:
            # Sécurisation : on utilise .get() pour éviter le KeyError
            question = item.get('question', 'Pas de question')
            reponse_proposee = item.get('response', '') 
            auteur = item.get('author_name', 'Anonyme')

            # On n'affiche que s'il y a une réponse à valider
            if reponse_proposee:
                with st.container(border=True):
                    st.write(f"**Q:** {question}")
                    st.write(f"**Auteur:** {auteur}")
                    st.info(f"**R proposée:** {reponse_proposee}")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("✅ Approuver", key=f"ok_{item['_id']}"):
                        mongo_db.contributions.update_one(
                            {"_id": item["_id"]}, 
                            {"$set": {"status": "validé"}}
                        )
                        st.rerun()
                    if col2.button("❌ Rejeter", key=f"no_{item['_id']}"):
                        # On réinitialise la réponse ou on supprime
                        mongo_db.contributions.update_one(
                            {"_id": item["_id"]}, 
                            {"$set": {"response": "", "status": "en_attente"}}
                        )
                        st.rerun()

    with t2:
        st.subheader("Toutes les données")
        all_docs = list(mongo_db.contributions.find().sort("created_at", -1))
        if all_docs:
            df = pd.DataFrame(all_docs)
            # On s'assure que les colonnes existent dans le DataFrame pour l'affichage
            cols_to_show = ["question", "author_name", "status", "response"]
            # Filtrer seulement les colonnes qui existent réellement
            existing_cols = [c for c in cols_to_show if c in df.columns]
            st.dataframe(df[existing_cols])