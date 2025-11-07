# agent.py (VERSION FINALE GOOGLE SHEETS)

import streamlit as st
from logger import log_interaction, log_unhandled_question 
from db_connector import knowledge_base # La base est chargée par db_connector


# --- MESSAGE DE REPLI EN CAS D'ÉCHEC RAG ---
DEFAULT_FALLBACK_ANSWER = "Désolé, je n'ai pas trouvé de réponse pertinente à votre question. Je l'ai notée pour nos administrateurs."


def get_agent_response(user_question: str, user_profile: str = "GUEST", username: str = "unknown") -> tuple[str, bool]:
    """
    Fonction principale qui cherche la réponse à la question de l'utilisateur, 
    adapte la réponse selon le profil, et journalise l'interaction via Google Sheets.
    """
    
    # Prétraitement de la question de l'utilisateur
    processed_question = user_question.lower().strip()
    best_match_answer = None
    
    # --- 1. Vérification de la Base de Connaissances ---
    
    # La variable knowledge_base est chargée par db_connector.py
    if not knowledge_base:
        # Retourne le message d'erreur standard (le code de débogage a été retiré)
        bot_response = "La base de connaissances n'a pas pu être chargée. Veuillez contacter l'administrateur."
        
        # Le log ne fonctionnera probablement pas ici non plus, mais nous le tentons quand même
        try:
            log_interaction(user_question, bot_response, False, user_profile, username)
        except Exception as e:
            # L'application ne plantera pas si le log échoue
            print(f"ÉCHEC D'ÉCRITURE CRITIQUE dans Logs (base non chargée): {e}")

        return bot_response, False
        
    # --- 2. Logique de Recherche Simple par Mot-Clé --
    
    for entry in knowledge_base:
        # Assurez-vous que db_connector a bien créé la clé 'search_text'
        search_text_entry = entry.get('search_text', '') 
        
        if not search_text_entry:
            continue
            
        # Cherche une correspondance exacte ou une inclusion
        if processed_question == search_text_entry or processed_question in search_text_entry:
            best_match_answer = entry['reponse']
            break
        
        # Vérifie l'inverse (si l'entrée est dans la question)
        if search_text_entry in processed_question:
             best_match_answer = entry['reponse']
             break

    # --- 3. Génération de la Réponse et Journalisation --
    if best_match_answer:
        bot_response = best_match_answer
        
        # Logique d'adaptation pour les profils (personnalisation optionnelle)
        if user_profile == "ADMINISTRATION" and "certificat de scolarité" in processed_question:
             bot_response += "\n\n(Note Admin: Le processus interne se trouve dans le drive partagé 'Documents Administratifs')"

        is_handled = True
    else:
        # Réponse de repli
        bot_response = DEFAULT_FALLBACK_ANSWER
        is_handled = False
        
        # Enregistrer la question non gérée (dans la table 'New_Questions')
        # Bloc try/except pour sécuriser l'écriture GSheets
        try:
            log_unhandled_question(user_question, user_profile, username)
        except Exception as e:
            print(f"ÉCHEC D'ÉCRITURE dans New_Questions: {e}") 
        
    # Journalisation de l'interaction (enregistre dans la table 'Logs')
    # Ceci est l'événement de log principal, toujours entouré d'un try/except
    try:
        log_interaction(user_question, bot_response, is_handled, user_profile, username)
    except Exception as e:
        print(f"ÉCHEC D'ÉCRITURE dans Logs: {e}")
    
    return bot_response, is_handled