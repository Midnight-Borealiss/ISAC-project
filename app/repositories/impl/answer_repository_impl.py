"""
Answer Repository Implementation - Airtable
"""
import logging
from typing import List, Optional
from pyairtable import Api
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, QUESTIONS_TABLE_ID, ANSWERS_TABLE_ID
from app.models import Answer
from app.repositories.answer_repository import AnswerRepository

logger = logging.getLogger(__name__)

# Initialiser Airtable
api = Api(AIRTABLE_API_KEY)
base = api.base(AIRTABLE_BASE_ID)
questions_table = base.table(QUESTIONS_TABLE_ID)
answers_table = base.table(ANSWERS_TABLE_ID)


class AnswerRepositoryImpl(AnswerRepository):
    """Implémentation Airtable du repository Answer"""

    def create(self, entity: Answer) -> Answer:
        """Créer une réponse"""
        try:
            result = answers_table.create(entity.to_dict())
            entity.id = result['id']
            return entity
        except Exception as e:
            logger.error(f"Erreur lors de la création de la réponse: {str(e)}")
            raise

    def get_by_id(self, entity_id: str) -> Optional[Answer]:
        """Récupérer une réponse par ID"""
        try:
            all_answers = self.get_all()
            return next((a for a in all_answers if a.id == entity_id), None)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la réponse: {str(e)}")
            return None

    def get_all(self) -> List[Answer]:
        """Récupérer toutes les réponses"""
        try:
            raw_answers = answers_table.all()
            answers = []
            for a in raw_answers:
                try:
                    answers.append(Answer.from_dict(a))
                except ValueError as e:
                    logger.warning(f"Réponse ignorée: {str(e)}")
                    continue
            return answers
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réponses: {str(e)}")
            return []

    def update(self, entity: Answer) -> Answer:
        """Mettre à jour une réponse"""
        try:
            answers_table.update(entity.id, {
                'Statut': entity.statut[0] if entity.statut else "À VALIDER"
            })
            return entity
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la réponse: {str(e)}")
            raise

    def delete(self, entity_id: str) -> bool:
        """Supprimer une réponse"""
        raise NotImplementedError("Delete non supporté pour les réponses")

    def get_by_question_id(self, question_id: str) -> List[Answer]:
        """Récupérer les réponses pour une question"""
        try:
            raw_answers = answers_table.all()
            answers = []
            for a in raw_answers:
                try:
                    answer = Answer.from_dict(a)
                    if answer.question_id == question_id:
                        answers.append(answer)
                except ValueError as e:
                    logger.warning(f"Réponse ignorée: {str(e)}")
                    continue
            return answers
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réponses: {str(e)}")
            return []

    def get_by_status(self, status: str) -> List[Answer]:
        """Récupérer les réponses par statut"""
        try:
            all_answers = self.get_all()
            return [a for a in all_answers if status in a.statut]
        except Exception as e:
            logger.error(f"Erreur lors du filtrage par statut: {str(e)}")
            return []

    def get_pending(self) -> List[Answer]:
        """Récupérer les réponses en attente de validation"""
        return self.get_by_status("À VALIDER")
