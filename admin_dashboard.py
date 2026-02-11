import streamlit as st
import pandas as pd
from db_connector import mongo_db

def render_admin_dashboard():
    st.header("📊 Dashboard Analyse ISMaiLa")
    st.info("Suivez l'activité et l'affluence des étudiants en temps réel.")

    # 1. Récupération des données (On pointe vers la collection de logs de ton logger)
    # Ton logger.py utilise "logs_interactions"
    logs_data = list(mongo_db.db['logs_interactions'].find())
    
    if not logs_data:
        # Si vide, on essaie la collection "logs" par défaut
        logs_data = list(mongo_db.db['logs'].find())

    df = pd.DataFrame(logs_data)

    if df.empty:
        st.warning("En attente de données pour générer les analyses...")
        return

    # Nettoyage de l'ID technique MongoDB
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    # 2. Conversion du temps
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['heure'] = df['timestamp'].dt.hour

    # 3. Indicateurs Clés (KPIs)
    col1, col2, col3 = st.columns(3)
    
    # On vérifie les noms de colonnes disponibles pour éviter les crashs
    user_col = 'username' if 'username' in df.columns else ('user_email' if 'user_email' in df.columns else None)
    
    with col1:
        st.metric("Total Questions", len(df))
    with col2:
        n_users = df[user_col].nunique() if user_col else 0
        st.metric("Utilisateurs Uniques", n_users)
    with col3:
        st.metric("Heure de pointe", f"{df['heure'].mode()[0]}h" if not df['heure'].empty else "N/A")

    st.divider()

    # 4. GRAPHIQUE D'AFFLUENCE
    st.subheader("📈 Affluence par heure")
    affluence_chart = df['heure'].value_counts().sort_index()
    st.bar_chart(affluence_chart, color="#1f77b4")

    st.divider()

    # 5. DÉTAILS DES INTERACTIONS (La partie qui causait l'erreur)
    st.subheader("📝 Dernières interactions")
    
    # On définit les colonnes qu'on veut afficher si elles existent
    cols_to_show = ['timestamp', 'username', 'question', 'reponse', 'profil']
    
    # On ne garde que les colonnes qui sont réellement dans le DataFrame
    available_cols = [c for c in cols_to_show if c in df.columns]
    
    if available_cols:
        # Tri par date et affichage des 5 dernières
        st.dataframe(
            df[available_cols].sort_values(by='timestamp', ascending=False).head(5),
            use_container_width=True
        )
    else:
        # Si aucune colonne connue n'est trouvée, on affiche tout le tableau par sécurité
        st.dataframe(df.sort_values(by='timestamp', ascending=False).head(5))

    # 6. EXPORT
    st.subheader("📥 Export des données")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger les logs (CSV)", csv, "logs_ismaila.csv", "text/csv")