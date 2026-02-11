import streamlit as st
from db_connector import mongo_db

def render_admin_page():
    st.title("🛡️ Administration ISMaiLa")
    
    # Onglets pour séparer les statistiques des actions
    tab1, tab2 = st.tabs(["📝 Questions à traiter", "📊 Statistiques"])

    with tab1:
        st.subheader("Questions posées par les étudiants (en attente)")
        
        # On récupère les questions avec le statut 'en_attente'
        # (Celles ajoutées automatiquement par l'agent ou par le formulaire de contribution)
        pending_list = mongo_db.get_contributions(status="en_attente")

        if not pending_list:
            st.success("✅ Toutes les questions ont été traitées !")
        else:
            for item in pending_list:
                # Création d'une petite carte pour chaque question
                with st.expander(f"❓ {item['question'][:80]}...", expanded=True):
                    st.write(f"**Question complète :** {item['question']}")
                    st.caption(f"Par : {item.get('user_name', 'Anonyme')} ({item.get('user_email', 'N/A')})")
                    
                    # Zone de texte pour rédiger la réponse officielle
                    # On utilise l'ID MongoDB pour que chaque champ soit unique
                    admin_res = st.text_area(
                        "Rédiger la réponse officielle :", 
                        key=f"res_{item['_id']}",
                        placeholder="Tapez ici la réponse que le chatbot donnera..."
                    )
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button("Valider ✅", key=f"val_{item['_id']}"):
                            if admin_res.strip():
                                # 1. On met à jour la réponse et le statut dans MongoDB
                                mongo_db.contributions.update_one(
                                    {"_id": item["_id"]},
                                    {"$set": {
                                        "response": admin_res.strip(),
                                        "status": "valide", # On utilise 'valide' comme dans ton agent
                                        "validated_by": st.session_state.name
                                    }}
                                )
                                st.success("Réponse enregistrée et publiée !")
                                st.rerun() # Rafraîchit pour faire disparaître la question traitée
                            else:
                                st.error("Tu dois écrire une réponse avant de valider.")

    with tab2:
        # Ici tu peux appeler ta fonction existante qui affiche les graphiques
        # provenant de admin_dashboard.py
        from admin_dashboard import render_admin_dashboard
        render_admin_dashboard()