import streamlit as st
import pandas as pd
from db_connector import mongo_db

def render_admin_dashboard():
    st.header("📊 Dashboard Analyse ISMaiLa")
    st.info("Suivez l'activité et l'affluence des étudiants en temps réel.")

    # 1. Récupération des données
    logs_data = list(mongo_db.db['logs'].find())
    df = pd.DataFrame(logs_data)

    if df.empty:
        st.warning("En attente de données pour générer les analyses...")
        return

    # Nettoyage
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    # 2. Conversion du temps
    # On s'assure que le timestamp est au format datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extraction de l'heure pour le graphique d'affluence
    df['heure'] = df['timestamp'].dt.hour

    # 3. Indicateurs Clés (KPIs)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Questions", len(df))
    with col2:
        st.metric("Utilisateurs Uniques", df['user_email'].nunique())
    with col3:
        st.metric("Heure de pointe", f"{df['heure'].mode()[0]}h" if not df['heure'].empty else "N/A")

    st.divider()

    # 4. GRAPHIQUE D'AFFLUENCE (Histogramme des heures)
    st.subheader("📈 Affluence par heure (Heures de pointe)")
    
    # Préparation des données pour le graphique
    affluence_chart = df['heure'].value_counts().sort_index()
    
    # Affichage du graphique à barres
    st.bar_chart(affluence_chart, color="#1f77b4")
    st.caption("Ce graphique montre à quels moments de la journée les étudiants sollicitent le plus ISMaiLa.")

    st.divider()

    # 5. EXPORT & DÉTAILS
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.subheader("📥 Export")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Télécharger CSV",
            data=csv,
            file_name='stats_ismaila.csv',
            mime='text/csv'
        )

    with col_b:
        st.subheader("📋 Derniers messages")
        # On montre les 5 derniers messages uniquement pour l'aperçu
        st.dataframe(df[['timestamp', 'user_name', 'user_query']].sort_values(by='timestamp', ascending=False).head(5))