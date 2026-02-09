"""
Answer Service Interface
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.dto import AnswerDTO, CreateAnswerDTO


class AnswerService(ABC):
    """Interface pour le service Answer"""

    @abstractmethod
    def create_answer(self, create_dto: CreateAnswerDTO) -> AnswerDTO:
        """Créer une nouvelle réponse"""
        pass

    @abstractmethod
    def get_answer(self, answer_id: str) -> Optional[AnswerDTO]:
        """Récupérer une réponse"""
        pass

    @abstractmethod
    def get_answers_for_question(self, question_id: str) -> List[AnswerDTO]:
        """Récupérer les réponses pour une question"""
        pass

    @abstractmethod
    def get_pending_answers(self) -> List[AnswerDTO]:
        """Récupérer les réponses en attente de validation"""
        pass

    @abstractmethod
    def get_all_answers(self) -> List[AnswerDTO]:
        """Récupérer toutes les réponses"""
        pass
