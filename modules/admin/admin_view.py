import streamlit as st
from db_connector import mongo_db
from bson import ObjectId

def render_admin_page():
    st.title("🛡️ Espace Modération & Validation")
    st.markdown("---")

    # Onglets pour organiser l'espace admin
    tab1, tab2, tab3 = st.tabs(["⏳ À traiter", "✅ Validées récemment", "📊 Statistiques"])

    with tab1:
        st.subheader("Questions en attente")
        pending_list = mongo_db.get_contributions(status="en_attente")
        
        if not pending_list:
            st.success("🎉 Aucune question en attente.")
        else:
            for item in pending_list:
                # Chaque question est présentée dans une boîte (container)
                with st.container(border=True):
                    # On pré-remplit avec la réponse suggérée
                    suggested_resp = item.get("response", "")
                    if suggested_resp == "En attente de réponse admin...":
                        suggested_resp = ""

                    st.write(f"**Question :** {item['question']}")
                    st.caption(f"Par : {item.get('user_name')} | Catégorie : {item.get('category')}")
                    
                    # Zone de saisie pour la réponse officielle
                    admin_response = st.text_area(
                        "Réponse officielle (à modifier ou valider) :", 
                        value=suggested_resp, 
                        key=f"input_{item['_id']}"
                    )

                    c1, c2, _ = st.columns([1, 1, 2])
                    with c1:
                        if st.button("Valider ✅", key=f"v_{item['_id']}", type="primary"):
                            if admin_response.strip():
                                mongo_db.contributions.update_one(
                                    {"_id": item["_id"]},
                                    {"$set": {"response": admin_response.strip(), "status": "valide", "validated_by": st.session_state.name}}
                                )
                                st.toast("Réponse publiée avec succès !", icon="✅")
                                st.rerun()
                            else:
                                st.error("La réponse ne peut pas être vide.")
                    
                    with c2:
                        if st.button("Supprimer 🗑️", key=f"d_{item['_id']}"):
                            mongo_db.contributions.delete_one({"_id": item["_id"]})
                            st.toast("Question supprimée.")
                            st.rerun()

    with tab2:
        st.subheader("Historique récent")
        validated_list = list(mongo_db.contributions.find({"status": "valide"}).sort("_id", -1).limit(10))
        for item in validated_list:
            with st.container(border=True):
                st.write(f"**Q :** {item['question']}")
                st.success(f"**R :** {item['response']}")
                if st.button("Invalider ↩️", key=f"rev_{item['_id']}"):
                    mongo_db.contributions.update_one({"_id": item["_id"]}, {"$set": {"status": "en_attente"}})
                    st.rerun()

    with tab3:
        # Intégration de votre dashboard de statistiques
        from admin_dashboard import render_admin_dashboard
        render_admin_dashboard()