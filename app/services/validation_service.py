"""
Validation Service Interface
"""
from abc import ABC, abstractmethod
from typing import Tuple
from app.dto import ValidationDTO


class ValidationService(ABC):
    """Interface pour le service Validation"""

    @abstractmethod
    def validate_answer(self, answer_id: str, is_approved: bool, admin_notes: str = "") -> Tuple[bool, str]:
        """Valider ou rejeter une réponse"""
        pass

    @abstractmethod
    def mark_as_official(self, answer_id: str, question_id: str) -> Tuple[bool, str]:
        """Marquer une réponse comme officielle"""
        pass
