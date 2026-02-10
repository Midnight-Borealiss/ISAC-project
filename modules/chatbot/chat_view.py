import streamlit as st
from agent import ismaila_agent

def render_chat():
    """Vue pour l'interface de discussion (Chatbot)"""
    st.title("💬 Assistant Virtuel ISMaiLa")
    st.markdown("Posez vos questions sur la vie étudiante, les inscriptions ou les cours.")

    # Affichage de l'historique des messages stockés dans la session
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Zone de saisie utilisateur
    if prompt := st.chat_input("Comment puis-je vous aider ?"):
        # Ajouter le message utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Appel de l'agent (qui vérifiera d'abord MongoDB avant d'utiliser l'IA)
        with st.spinner("Recherche dans la base de connaissances..."):
            response, source = ismaila_agent.get_response(
                prompt, 
                st.session_state.user_profile, 
                st.session_state.username
            )
            
            # Affichage de la réponse
            with st.chat_message("assistant"):
                st.markdown(response)
                if source == "database":
                    st.caption("🔍 Source : FAQ validée par l'administration")
            
            # Sauvegarde de la réponse de l'assistant
            st.session_state.messages.append({"role": "assistant", "content": response})