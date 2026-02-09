"""
Question Repository Implementation - Airtable
"""
import logging
from typing import List, Optional
from pyairtable import Api
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, QUESTIONS_TABLE_ID
from app.models import Question
from app.repositories.question_repository import QuestionRepository

logger = logging.getLogger(__name__)

# Initialiser Airtable
api = Api(AIRTABLE_API_KEY)
base = api.base(AIRTABLE_BASE_ID)
table = base.table(QUESTIONS_TABLE_ID)


class QuestionRepositoryImpl(QuestionRepository):
    """Implémentation Airtable du repository Question"""

    def create(self, entity: Question) -> Question:
        """Créer une question"""
        try:
            result = table.create(entity.to_dict())
            entity.id = result['id']
            return entity
        except Exception as e:
            logger.error(f"Erreur lors de la création de la question: {str(e)}")
            raise

    def get_by_id(self, entity_id: str) -> Optional[Question]:
        """Récupérer une question par ID"""
        try:
            all_questions = self.get_all()
            return next((q for q in all_questions if q.id == entity_id), None)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la question: {str(e)}")
            return None

    def get_all(self) -> List[Question]:
        """Récupérer toutes les questions"""
        try:
            raw_questions = table.all()
            questions = []
            for q in raw_questions:
                try:
                    questions.append(Question.from_dict(q))
                except ValueError as e:
                    # Ignorer les questions mal formées
                    logger.warning(f"Question ignorée: {str(e)}")
                    continue
            return questions
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des questions: {str(e)}")
            return []

    def update(self, entity: Question) -> Question:
        """Mettre à jour une question"""
        # Airtable ne supporte pas bien les mises à jour via pyairtable
        # Implémenter si nécessaire
        raise NotImplementedError("Update non supporté pour les questions")

    def delete(self, entity_id: str) -> bool:
        """Supprimer une question"""
        # Airtable ne supporte pas bien les suppressions via pyairtable
        # Implémenter si nécessaire
        raise NotImplementedError("Delete non supporté pour les questions")

    def get_by_category(self, category: str) -> List[Question]:
        """Récupérer les questions par catégorie"""
        try:
            all_questions = self.get_all()
            return [q for q in all_questions if category in q.category]
        except Exception as e:
            logger.error(f"Erreur lors du filtrage par catégorie: {str(e)}")
            return []

    def get_by_contributor(self, contributor: str) -> List[Question]:
        """Récupérer les questions d'un contributeur"""
        try:
            all_questions = self.get_all()
            return [q for q in all_questions if q.contributor == contributor]
        except Exception as e:
            logger.error(f"Erreur lors du filtrage par contributeur: {str(e)}")
            return []

    def get_by_status(self, status: str) -> List[Question]:
        """Récupérer les questions par statut"""
        try:
            all_questions = self.get_all()
            return [q for q in all_questions if status in q.statut]
        except Exception as e:
            logger.error(f"Erreur lors du filtrage par statut: {str(e)}")
            return []
