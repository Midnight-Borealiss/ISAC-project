import streamlit as st
from db_connector import mongo_db
from bson import ObjectId

def render_admin_page():
    st.title("🛡️ Espace Modération & Validation")
    st.markdown("---")

    # Onglets pour organiser l'espace admin
    tab1, tab2, tab3 = st.tabs(["⏳ À traiter", "✅ Validées récemment", "📊 Statistiques"])

    with tab1:
        st.subheader("Questions en attente de validation")
        # On récupère les contributions qui ne sont pas encore validées
        pending_list = mongo_db.get_contributions(status="en_attente")
        
        if not pending_list:
            st.success("🎉 Aucune question en attente. La base est à jour !")
        else:
            for item in pending_list:
                # Chaque question est présentée dans une boîte (container)
                with st.container(border=True):
                    # --- LOGIQUE DE RÉCUPÉRATION DE LA RÉPONSE ---
                    # On récupère ce qui est en base
                    valeur_actuelle = item.get("response", "")
                    
                    # Si c'est le message par défaut du bot, on vide pour l'admin
                    # Sinon, on garde la proposition du contributeur
                    if valeur_actuelle == "En attente de réponse admin...":
                        reponse_a_afficher = ""
                    else:
                        reponse_a_afficher = valeur_actuelle

                    st.write(f"**Question posée :** {item['question']}")
                    st.caption(f"Auteur : {item.get('user_name', 'Anonyme')} | Catégorie : {item.get('category', 'Général')}")
                    
                    # La zone de texte est pré-remplie avec 'value'
                    admin_response = st.text_area(
                        "Réponse officielle (proposée ou à écrire) :", 
                        value=reponse_a_afficher, 
                        key=f"input_{item['_id']}",
                        height=100,
                        placeholder="Saisissez la réponse officielle ici..."
                    )

                    c1, c2, _ = st.columns([1, 1, 2])
                    with c1:
                        if st.button("Valider la réponse ✅", key=f"v_{item['_id']}", type="primary"):
                            if admin_response.strip():
                                mongo_db.contributions.update_one(
                                    {"_id": item["_id"]},
                                    {"$set": {
                                        "response": admin_response.strip(), 
                                        "status": "valide", 
                                        "validated_by": st.session_state.name
                                    }}
                                )
                                st.toast("Réponse validée et publiée !")
                                st.rerun()
                            else:
                                st.error("Veuillez saisir une réponse avant de valider.")
                    
                    with c2:
                        if st.button("Supprimer 🗑️", key=f"d_{item['_id']}"):
                            mongo_db.contributions.delete_one({"_id": item["_id"]})
                            st.toast("Question supprimée.")
                            st.rerun()

    with tab2:
        st.subheader("Historique des 10 dernières validations")
        validated_list = list(mongo_db.contributions.find({"status": "valide"}).sort("_id", -1).limit(10))
        
        if not validated_list:
            st.info("Aucune validation récente.")
        else:
            for item in validated_list:
                with st.container(border=True):
                    st.write(f"**Question :** {item['question']}")
                    st.success(f"**Réponse officielle :** {item['response']}")
                    st.caption(f"Validé par : {item.get('validated_by', 'Admin')}")
                    
                    if st.button("Modifier ou Invalider ↩️", key=f"rev_{item['_id']}"):
                        mongo_db.contributions.update_one(
                            {"_id": item["_id"]}, 
                            {"$set": {"status": "en_attente"}}
                        )
                        st.rerun()

    with tab3:
        from admin_dashboard import render_admin_dashboard
        render_admin_dashboard()