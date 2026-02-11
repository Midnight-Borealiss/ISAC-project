import streamlit as st
import pandas as pd
from logger import db_logger # On utilise ton logger.py

def render_admin_dashboard():
    st.header("📊 Dashboard Analyse ISMaiLa")

    # 1. Récupération des données depuis la bonne collection
    # Ton logger utilise 'logs_interactions'
    logs_data = list(db_logger.logs.find())
    df = pd.DataFrame(logs_data)

    if df.empty:
        st.warning("Aucune interaction enregistrée pour le moment.")
        return

    # Nettoyage de l'ID MongoDB
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    # 2. Conversion du temps
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['heure'] = df['timestamp'].dt.hour

    # 3. Indicateurs Clés (KPIs) avec les bons noms de colonnes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Questions", len(df))
    with col2:
        # Dans ton logger c'est 'username' et non 'user_email'
        n_users = df['username'].nunique() if 'username' in df.columns else 0
        st.metric("Utilisateurs Uniques", n_users)
    with col3:
        st.metric("Heure de pointe", f"{df['heure'].mode()[0]}h" if not df['heure'].empty else "N/A")

    st.divider()

    # --- Section Affluence (Graphique) ---
    st.subheader("📈 Affluence par heure")
    affluence_chart = df['heure'].value_counts().sort_index()
    st.bar_chart(affluence_chart, color="#1f77b4")

    st.divider()

    # 4. RÉGLAGE DU KEYERROR (La partie qui bloquait)
    st.subheader("📝 Dernières interactions")
    
    # On définit les colonnes réelles présentes dans ton MongoLogger.log_interaction
    # colonnes : timestamp, username, profil, question, reponse
    cols_to_show = ['timestamp', 'username', 'question', 'reponse']
    
    # On vérifie lesquelles sont présentes dans le DF pour éviter le plantage
    existing_cols = [c for c in cols_to_show if c in df.columns]
    
    if existing_cols:
        st.dataframe(
            df[existing_cols].sort_values(by='timestamp', ascending=False).head(10),
            use_container_width=True
        )