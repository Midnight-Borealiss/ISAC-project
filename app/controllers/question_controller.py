"""
Question Controller - Orchestration pour les Questions
"""
import logging
from typing import Tuple, List
from app.dto import QuestionDTO, CreateQuestionDTO
from app.services.impl import QuestionServiceImpl

logger = logging.getLogger(__name__)


class QuestionController:
    """Controller pour gérer les Questions"""

    def __init__(self):
        self.service = QuestionServiceImpl()

    def submit_question(self, question: str, category: str, username: str) -> Tuple[bool, str]:
        """Soumettre une nouvelle question"""
        try:
            # Validation
            if not question or not question.strip():
                return False, "La question ne peut pas être vide."
            if not category:
                return False, "La catégorie est requise."
            if not username:
                return False, "Le contributeur est requis."

            # Créer le DTO
            create_dto = CreateQuestionDTO(
                question=question.strip(),
                category=category,
                contributor=username
            )

            # Utiliser le service
            result_dto = self.service.create_question(create_dto)
            return True, f"✅ Question enregistrée avec succès dans la catégorie '{category}' !"
        except ValueError as e:
            return False, f"❌ Validation échouée : {str(e)}"
        except Exception as e:
            return False, f"❌ Erreur lors de l'enregistrement : {str(e)}"

    def get_all_questions(self) -> List[QuestionDTO]:
        """Récupérer toutes les questions"""
        return self.service.get_all_questions()

    def get_questions_by_category(self, category: str) -> List[QuestionDTO]:
        """Récupérer les questions par catégorie"""
        return self.service.get_questions_by_category(category)

    def get_questions_by_contributor(self, contributor: str) -> List[QuestionDTO]:
        """Récupérer les questions d'un contributeur"""
        return self.service.get_questions_by_contributor(contributor)
