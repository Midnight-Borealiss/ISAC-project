"""
Validation Service Implementation
"""
import logging
from typing import Tuple
from pyairtable import Api
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, ANSWERS_TABLE_ID
from app.repositories.impl import ValidationRepositoryImpl, AnswerRepositoryImpl
from app.models import Validation, Answer
from app.mappers import ValidationMapper
from app.services.validation_service import ValidationService

logger = logging.getLogger(__name__)

# Initialiser Airtable
api = Api(AIRTABLE_API_KEY)
base = api.base(AIRTABLE_BASE_ID)
answers_table = base.table(ANSWERS_TABLE_ID)


class ValidationServiceImpl(ValidationService):
    """Implémentation du service Validation"""

    def __init__(self):
        self.validation_repo = ValidationRepositoryImpl()
        self.answer_repo = AnswerRepositoryImpl()

    def validate_answer(self, answer_id: str, is_approved: bool, admin_notes: str = "") -> Tuple[bool, str]:
        """Valider ou rejeter une réponse"""
        try:
            # Créer l'entité Validation
            statut = "APPROUVÉE" if is_approved else "REJETÉE"
            validation = Validation(
                answer_id=answer_id,
                statut=statut,
                admin_notes=admin_notes
            )
            
            # Persister la validation
            self.validation_repo.create(validation)
            
            # Mettre à jour le statut de la réponse (STRING, pas LISTE)
            answers_table.update(answer_id, {
                'Statut': statut
            })
            
            return True, f"✅ Réponse {statut.lower()} avec succès !"
        except Exception as e:
            logger.error(f"Erreur lors de la validation: {str(e)}")
            return False, f"❌ Erreur lors de la validation : {str(e)}"

    def mark_as_official(self, answer_id: str, question_id: str) -> Tuple[bool, str]:
        """Marquer une réponse comme officielle"""
        try:
            # Marquer la réponse comme officielle en mettant à jour son statut (STRING)
            answers_table.update(answer_id, {
                'Statut': 'APPROUVÉE'
            })
            return True, f"✅ Réponse marquée comme officielle !"
        except Exception as e:
            logger.error(f"Erreur lors du marquage comme officielle: {str(e)}")
            return False, f"❌ Erreur lors de la mise à jour : {str(e)}"
