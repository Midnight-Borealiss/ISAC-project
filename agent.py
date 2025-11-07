# agent.py (VERSION AIRTABLE : Appel de l'API)

from logger import log_interaction, log_unhandled_question 
from db_connector import knowledge_base # La base est chargée par db_connector

DEFAULT_FALLBACK_ANSWER = "Désolé, je n'ai pas trouvé de réponse pertinente à votre question. Je l'ai notée pour nos administrateurs."


def get_agent_response(user_question: str, user_profile: str = "GUEST", username: str = "unknown") -> tuple[str, bool]:
    """
    Fonction principale qui cherche la réponse à la question de l'utilisateur, 
    adapte la réponse selon le profil, et journalise l'interaction via Airtable.
    """
    
    processed_question = user_question.lower().strip()
    best_match_answer = None
    
    # --- 1. Vérification de la Base de Connaissances ---
    if not knowledge_base:
        # Utiliser l'erreur stockée ou le message par défaut
        error_detail = st.session_state.get('knowledge_base_error', 'Impossible de déterminer la cause de l\'échec. Vérifiez les secrets/permissions.')
        
        # Afficher l'erreur détaillée UNIQUEMENT si l'utilisateur est un admin ou un testeur
        if user_profile == "ADMINISTRATION" or user_profile == "Testeur":
             bot_response = f"La base de connaissances n'a pas pu être chargée. (ADMIN DEBUG: {error_detail})"
        else:
             bot_response = "La base de connaissances n'a pas pu être chargée. Veuillez contacter l'administrateur."

        return bot_response, False
        
    # --- 2. Logique de Recherche Simple par Mot-Clé ---
    
    for entry in knowledge_base:
        search_text_entry = entry['search_text'] 
        
        # Le champ 'search_text' contient les Questions + Formulations concaténées
        if processed_question == search_text_entry or processed_question in search_text_entry:
            best_match_answer = entry['reponse']
            break
        
        if search_text_entry in processed_question:
             best_match_answer = entry['reponse']
             break

    # --- 3. Génération de la Réponse et Journalisation ---
    if best_match_answer:
        bot_response = best_match_answer
        
        # Logique d'adaptation pour les profils (si nécessaire)
        if user_profile == "ADMINISTRATION" and "certificat de scolarité" in processed_question:
             bot_response += "\n\n(Note Admin: Le processus interne se trouve dans le drive partagé 'Documents Administratifs')"

        is_handled = True
    else:
        # Réponse de repli
        bot_response = DEFAULT_FALLBACK_ANSWER
        is_handled = False
        
        # Enregistrer la question non gérée dans la table 'New_Questions'
        log_unhandled_question(user_question, user_profile, username)
        
    # Journalisation de l'interaction (enregistre dans la table 'Logs')
    log_interaction(user_question, bot_response, is_handled, user_profile, username)
    
    return bot_response, is_handled