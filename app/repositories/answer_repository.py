"""
Answer Repository Interface
"""
from abc import abstractmethod
from typing import List, Optional
from app.models import Answer
from .base_repository import BaseRepository


class AnswerRepository(BaseRepository[Answer]):
    """Interface pour le repository Answer"""

    @abstractmethod
    def get_by_question_id(self, question_id: str) -> List[Answer]:
        """Récupérer les réponses pour une question"""
        pass

    @abstractmethod
    def get_by_status(self, status: str) -> List[Answer]:
        """Récupérer les réponses par statut"""
        pass

    @abstractmethod
    def get_pending(self) -> List[Answer]:
        """Récupérer les réponses en attente de validation"""
        pass
