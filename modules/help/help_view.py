import streamlit as st

def render_help_page():
    st.title("📖 Centre d'aide ISMaiLa")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.expander("🎓 Comment fonctionne le Chatbot ?", expanded=True):
            st.write("""
            L'assistant utilise une base de connaissances officielle alimentée par l'administration.
            - **Réponses instantanées** : Si la question est connue, vous recevez une réponse certifiée.
            - **Apprentissage continu** : Si l'assistant ne sait pas répondre, votre question est envoyée aux administrateurs pour être traitée.
            """)

        with st.expander("🌍 Comment contribuer ?"):
            st.write("""
            Vous pouvez proposer des questions/réponses via l'onglet **Contribution**. 
            Toute proposition suit ce cycle :
            1. **Soumission** : Vous remplissez le formulaire.
            2. **Modération** : Un administrateur vérifie l'exactitude de l'information.
            3. **Publication** : Une fois validée, l'information devient accessible à tous sur le Chatbot.
            """)

    with col2:
        st.info("💡 **Astuce** : Soyez précis dans vos questions (ex: utilisez 'Modalités d'inscription' plutôt que juste 'Inscription').")
        
    st.divider()
    
    # Section spécifique si l'utilisateur est admin
    if st.session_state.user_profile == "ADMINISTRATION":
        st.subheader("🛡️ Espace Administrateur")
        st.warning("""
        **Rappels de modération :**
        - Vérifiez l'orthographe avant de valider.
        - Utilisez le bouton 'Invalider' dans l'historique pour corriger une erreur passée.
        - Surveillez le Dashboard pour identifier les questions les plus fréquentes.
        """)