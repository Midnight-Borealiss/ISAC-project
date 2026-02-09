"""
Validation Repository Interface
"""
from abc import abstractmethod
from typing import List, Optional
from app.models import Validation
from .base_repository import BaseRepository


class ValidationRepository(BaseRepository[Validation]):
    """Interface pour le repository Validation"""

    @abstractmethod
    def get_by_answer_id(self, answer_id: str) -> Optional[Validation]:
        """Récupérer la validation d'une réponse"""
        pass

    @abstractmethod
    def get_by_status(self, status: str) -> List[Validation]:
        """Récupérer les validations par statut"""
        pass
