"""
Question Service Interface
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.dto import QuestionDTO, CreateQuestionDTO


class QuestionService(ABC):
    """Interface pour le service Question"""

    @abstractmethod
    def create_question(self, create_dto: CreateQuestionDTO) -> QuestionDTO:
        """Créer une nouvelle question"""
        pass

    @abstractmethod
    def get_question(self, question_id: str) -> Optional[QuestionDTO]:
        """Récupérer une question"""
        pass

    @abstractmethod
    def get_all_questions(self) -> List[QuestionDTO]:
        """Récupérer toutes les questions"""
        pass

    @abstractmethod
    def get_questions_by_category(self, category: str) -> List[QuestionDTO]:
        """Récupérer les questions par catégorie"""
        pass

    @abstractmethod
    def get_questions_by_contributor(self, contributor: str) -> List[QuestionDTO]:
        """Récupérer les questions d'un contributeur"""
        pass
