import streamlit as st

def render_help_page():
    st.title("📖 Guide d'Utilisation ISAC")
    
    st.warning("""
    **⚠️ AVERTISSEMENT MÉDICAL** ISAC est un outil d'aide à l'orientation. Il ne remplace en aucun cas une consultation médicale.  
    **En cas d'urgence vitale, appelez immédiatement le 15 ou le 112.**
    """)

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Comment fonctionne le triage ?", expanded=True):
            st.write("""
            1. **Analyse immédiate** : ISAC scanne vos mots pour détecter des signes de gravité.
            2. **Collecte** : Vos constantes (température, poids) affinent l'analyse.
            3. **Orientation** : ISAC vous suggère soit des soins à domicile, soit une consultation rapide.
            """)
    with col2:
        st.info("💡 **Astuce** : Mettez à jour votre température dans la barre latérale avant de commencer à discuter.")