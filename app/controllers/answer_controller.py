"""
Answer Controller - Orchestration pour les Answers
"""
import logging
from typing import Tuple, List
from app.dto import AnswerDTO, CreateAnswerDTO
from app.services.impl import AnswerServiceImpl

logger = logging.getLogger(__name__)


class AnswerController:
    """Controller pour gérer les Answers"""

    def __init__(self):
        self.service = AnswerServiceImpl()

    def submit_answer(self, question_id: str, response: str, username: str) -> Tuple[bool, str]:
        """Soumettre une nouvelle réponse"""
        try:
            # Validation
            if not question_id:
                return False, "L'ID de la question est requis."
            if not response or not response.strip():
                return False, "La réponse ne peut pas être vide."
            if not username:
                return False, "Le répondeur est requis."

            # Créer le DTO
            create_dto = CreateAnswerDTO(
                question_id=question_id,
                response=response.strip(),
                respondent=username
            )

            # Utiliser le service
            result_dto = self.service.create_answer(create_dto)
            return True, f"✅ Réponse enregistrée avec succès !"
        except ValueError as e:
            return False, f"❌ Validation échouée : {str(e)}"
        except Exception as e:
            return False, f"❌ Erreur lors de l'enregistrement : {str(e)}"

    def get_answers_for_question(self, question_id: str) -> List[AnswerDTO]:
        """Récupérer les réponses pour une question"""
        return self.service.get_answers_for_question(question_id)

    def get_pending_answers(self) -> List[AnswerDTO]:
        """Récupérer les réponses en attente de validation"""
        return self.service.get_pending_answers()

    def get_all_answers(self) -> List[AnswerDTO]:
        """Récupérer toutes les réponses"""
        return self.service.get_all_answers()
