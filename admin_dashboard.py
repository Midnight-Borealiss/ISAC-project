# admin_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from db_connector import get_logs_data, get_unhandled_questions 

def render_admin_dashboard():
    st.title("Tableau de Bord Administration ??")

    logs_df = get_logs_data()
    questions_df = get_unhandled_questions()

    if logs_df.empty:
        st.info("Aucune donnée de Log disponible.")
        return
        
    # KPI
    st.header("Performance")
    interactions = logs_df[logs_df['Type'] == 'INTERACTION']
    total = len(interactions)
    # Conversion sure si Airtable envoie des chaines ou des booléens
    # On suppose que la colonne 'Géré' est un Checkbox (True/False) ou texte
    if 'Géré' in interactions.columns:
        success = interactions['Géré'].apply(lambda x: True if x == True or str(x).lower() == 'true' else False).sum()
    else:
        success = 0
        
    col1, col2 = st.columns(2)
    col1.metric("Total Interactions", total)
    col2.metric("Taux de Succés", f"{(success/total):.1%}" if total else "0%")

    # Questions � traiter
    st.header("Questions à Traiter")
    if not questions_df.empty:
        st.dataframe(questions_df)
    else:
        st.success("Aucune question en attente.")

    # Logs
    st.header("Historique")
    st.dataframe(logs_df)
