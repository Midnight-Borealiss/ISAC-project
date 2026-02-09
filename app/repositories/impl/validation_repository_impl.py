"""
Validation Repository Implementation - Airtable
"""
import logging
from typing import List, Optional
from pyairtable import Api
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, VALIDATIONS_TABLE_ID
from app.models import Validation
from app.repositories.validation_repository import ValidationRepository

logger = logging.getLogger(__name__)

# Initialiser Airtable
api = Api(AIRTABLE_API_KEY)
base = api.base(AIRTABLE_BASE_ID)
validations_table = base.table(VALIDATIONS_TABLE_ID)


class ValidationRepositoryImpl(ValidationRepository):
    """Implémentation Airtable du repository Validation"""

    def create(self, entity: Validation) -> Validation:
        """Créer une validation"""
        try:
            result = validations_table.create(entity.to_dict())
            entity.id = result['id']
            return entity
        except Exception as e:
            logger.error(f"Erreur lors de la création de la validation: {str(e)}")
            raise

    def get_by_id(self, entity_id: str) -> Optional[Validation]:
        """Récupérer une validation par ID"""
        try:
            all_validations = self.get_all()
            return next((v for v in all_validations if v.id == entity_id), None)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la validation: {str(e)}")
            return None

    def get_all(self) -> List[Validation]:
        """Récupérer toutes les validations"""
        # Actuellement Airtable n'a pas de fonction pour récupérer toutes les validations
        # À implémenter si nécessaire
        logger.warning("get_all() non implémenté pour Validations")
        return []

    def update(self, entity: Validation) -> Validation:
        """Mettre à jour une validation"""
        raise NotImplementedError("Update non supporté pour les validations")

    def delete(self, entity_id: str) -> bool:
        """Supprimer une validation"""
        raise NotImplementedError("Delete non supporté pour les validations")

    def get_by_answer_id(self, answer_id: str) -> Optional[Validation]:
        """Récupérer la validation d'une réponse"""
        # À implémenter si nécessaire
        logger.warning("get_by_answer_id() non implémenté pour Validations")
        return None

    def get_by_status(self, status: str) -> List[Validation]:
        """Récupérer les validations par statut"""
        # À implémenter si nécessaire
        logger.warning("get_by_status() non implémenté pour Validations")
        return []
