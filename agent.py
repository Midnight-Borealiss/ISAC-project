from db_connector import mongo_db
from logger import db_logger

class IsmailaAgent:
    def __init__(self):
        self.default_fallback = "Désolé, je n'ai pas trouvé de réponse. Je l'ai notée pour mes créateurs."

    def get_response(self, user_question, user_profile="GUEST", username="unknown"):
        processed_q = user_question.lower().strip()
        knowledge_base = mongo_db.get_knowledge_base()
        
        best_match = None
        
        # Logique de recherche (MongoDB version)
        for entry in knowledge_base:
            # Dans MongoDB, on suppose que tes questions sont dans une liste 'questions'
            questions_list = entry.get('questions', [])
            if any(processed_q in q.lower() for q in questions_list):
                best_match = entry.get('answer')
                break

        if best_match:
            response = best_match
            is_handled = True
        else:
            response = self.default_fallback
            is_handled = False
            db_logger.log_unhandled_question(user_question, user_profile, username)

        # Log final
        db_logger.log_interaction(username, user_question, response, is_handled, user_profile, username)
        
        return response, is_handled

# Instance unique
ismaila_agent = IsmailaAgent()