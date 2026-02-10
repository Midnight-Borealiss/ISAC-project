import streamlit as st

# Configuration des accès
USER_PROFILES_RULES = {
    "ADMINISTRATION": ["minawade005@gmail.com", "ismaila.admin@uam.sn"],
    "ÉTUDIANT": ["@edu.uam.sn", "@uam.sn"]
}
DEFAULT_PROFILE = "ÉTUDIANT"

def get_user_profile(email):
    """Détermine le rôle de l'utilisateur basé sur son email"""
    clean_email = email.strip().lower()
    for profile, keywords in USER_PROFILES_RULES.items():
        for kw in keywords:
            if kw.lower() in clean_email:
                return profile
    return DEFAULT_PROFILE