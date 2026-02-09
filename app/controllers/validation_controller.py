"""
Validation Controller - Orchestration pour les Validations
"""
import logging
from typing import Tuple
from app.services.impl import ValidationServiceImpl

logger = logging.getLogger(__name__)


class ValidationController:
    """Controller pour gérer les Validations"""

    def __init__(self):
        self.service = ValidationServiceImpl()

    def validate_answer(self, answer_id: str, is_approved: bool, admin_notes: str = "") -> Tuple[bool, str]:
        """Valider ou rejeter une réponse"""
        try:
            if not answer_id:
                return False, "L'ID de la réponse est requis."

            return self.service.validate_answer(answer_id, is_approved, admin_notes)
        except Exception as e:
            logger.error(f"Erreur dans le controller: {str(e)}")
            return False, f"❌ Erreur lors de la validation : {str(e)}"

    def mark_as_official_answer(self, answer_id: str, question_id: str) -> Tuple[bool, str]:
        """Marquer une réponse comme officielle"""
        try:
            if not answer_id or not question_id:
                return False, "Les IDs sont requis."

            return self.service.mark_as_official(answer_id, question_id)
        except Exception as e:
            logger.error(f"Erreur dans le controller: {str(e)}")
            return False, f"❌ Erreur lors de la mise à jour : {str(e)}"
