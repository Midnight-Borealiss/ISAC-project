"""
Question Repository Interface
"""
from abc import abstractmethod
from typing import List, Optional
from app.models import Question
from .base_repository import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    """Interface pour le repository Question"""

    @abstractmethod
    def get_by_category(self, category: str) -> List[Question]:
        """Récupérer les questions par catégorie"""
        pass

    @abstractmethod
    def get_by_contributor(self, contributor: str) -> List[Question]:
        """Récupérer les questions d'un contributeur"""
        pass

    @abstractmethod
    def get_by_status(self, status: str) -> List[Question]:
        """Récupérer les questions par statut"""
        pass
