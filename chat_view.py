import streamlit as st
from agent import isac_agent # On utilise le nouvel agent ISAC

def render_chat():
    st.title("💬 Consultation ISAC")
    st.info("Décrivez vos symptômes. ISAC vous aidera à évaluer la situation.")

    # Affichage historique
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ex: J'ai mal à la tête depuis ce matin..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner("Analyse de vos symptômes..."):
            # On envoie les metrics (âge, temp) à l'agent pour un triage intelligent
            response, source = isac_agent.get_response(
                prompt, 
                st.session_state.get("health_metrics", {}), 
                st.session_state.username
            )
            
            with st.chat_message("assistant"):
                st.markdown(response)
                st.caption(f"ℹ️ Source : {source}")
            
            st.session_state.messages.append({"role": "assistant", "content": response})