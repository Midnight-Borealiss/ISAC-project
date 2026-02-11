import streamlit as st
from db_connector import mongo_db
from bson import ObjectId

def render_admin_page():
    st.title("🛡️ Espace Modération & Validation")
    st.markdown("---")

    # Onglets pour organiser l'espace admin
    tab_pend, tab_stats = st.tabs(["⏳ Questions à traiter", "📊 Statistiques d'activité"])

    with tab_pend:
        st.subheader("Questions sans réponse détectées")
        
        # On récupère les questions en attente
        pending_questions = mongo_db.get_contributions(status="en_attente")

        if not pending_questions:
            st.success("🎉 Félicitations ! Toutes les questions ont été traitées.")
        else:
            st.info(f"Il y a actuellement **{len(pending_questions)}** question(s) en attente de réponse.")
            
            for item in pending_questions:
                # Chaque question est présentée dans une boîte (expander ou container)
                with st.container(border=True):
                    col_info, col_action = st.columns([3, 1])
                    
                    with col_info:
                        st.write(f"**Question :** {item['question']}")
                        st.caption(f"Posée par : {item.get('user_name', 'Anonyme')} | Catégorie : {item.get('category', 'Auto')}")
                    
                    # Zone de saisie pour la réponse officielle
                    admin_response = st.text_area(
                        "Votre réponse officielle :", 
                        key=f"input_{item['_id']}",
                        placeholder="Écrivez ici la réponse qui sera apprise par le bot..."
                    )

                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        if st.button("Valider ✅", key=f"btn_val_{item['_id']}", type="primary"):
                            if admin_response.strip():
                                # Mise à jour dans MongoDB
                                mongo_db.contributions.update_one(
                                    {"_id": item["_id"]},
                                    {"$set": {
                                        "response": admin_response.strip(),
                                        "status": "valide",
                                        "validated_by": st.session_state.name
                                    }}
                                )
                                st.toast("Réponse publiée avec succès !", icon="✅")
                                st.rerun()
                            else:
                                st.error("La réponse ne peut pas être vide.")
                    
                    with c2:
                        if st.button("Supprimer 🗑️", key=f"btn_del_{item['_id']}"):
                            mongo_db.contributions.delete_one({"_id": item["_id"]})
                            st.toast("Question supprimée.")
                            st.rerun()

    with tab_stats:
        # Intégration de votre dashboard de statistiques
        from admin_dashboard import render_admin_dashboard
        render_admin_dashboard()