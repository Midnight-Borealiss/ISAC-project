import streamlit as st
from db_connector import mongo_db

def render_admin_dashboard():
    st.title("Tableau de Bord Administration 📊")

    logs_df = mongo_db.get_logs_data()
    questions_df = mongo_db.get_unhandled_questions()

    if logs_df.empty:
        st.info("Aucune donnée disponible sur MongoDB.")
        return
        
    # KPI
    total = len(logs_df)
    success = logs_df[logs_df['is_handled'] == True].shape[0] if 'is_handled' in logs_df.columns else 0
        
    col1, col2 = st.columns(2)
    col1.metric("Total Interactions", total)
    col2.metric("Taux de Succès", f"{(success/total):.1%}" if total else "0%")

    st.header("Historique des Logs")
    st.dataframe(logs_df)