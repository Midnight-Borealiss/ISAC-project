"""
Question Service Implementation
"""
import logging
from typing import List, Optional
from app.dto import QuestionDTO, CreateQuestionDTO
from app.mappers import QuestionMapper
from app.repositories.impl import QuestionRepositoryImpl
from app.services.question_service import QuestionService

logger = logging.getLogger(__name__)


class QuestionServiceImpl(QuestionService):
    """Implémentation du service Question"""

    def __init__(self):
        self.question_repo = QuestionRepositoryImpl()

    def create_question(self, create_dto: CreateQuestionDTO) -> QuestionDTO:
        """Créer une nouvelle question"""
        try:
            # Convertir DTO → Entity
            question_entity = QuestionMapper.to_entity(create_dto)
            
            # Persister
            saved_entity = self.question_repo.create(question_entity)
            
            # Convertir Entity → DTO
            return QuestionMapper.to_dto(saved_entity)
        except Exception as e:
            logger.error(f"Erreur lors de la création de la question: {str(e)}")
            raise

    def get_question(self, question_id: str) -> Optional[QuestionDTO]:
        """Récupérer une question"""
        try:
            entity = self.question_repo.get_by_id(question_id)
            return QuestionMapper.to_dto(entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la question: {str(e)}")
            return None

    def get_all_questions(self) -> List[QuestionDTO]:
        """Récupérer toutes les questions"""
        try:
            entities = self.question_repo.get_all()
            return [QuestionMapper.to_dto(e) for e in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des questions: {str(e)}")
            return []

    def get_questions_by_category(self, category: str) -> List[QuestionDTO]:
        """Récupérer les questions par catégorie"""
        try:
            entities = self.question_repo.get_by_category(category)
            return [QuestionMapper.to_dto(e) for e in entities]
        except Exception as e:
            logger.error(f"Erreur lors du filtrage par catégorie: {str(e)}")
            return []

    def get_questions_by_contributor(self, contributor: str) -> List[QuestionDTO]:
        """Récupérer les questions d'un contributeur"""
        try:
            entities = self.question_repo.get_by_contributor(contributor)
            return [QuestionMapper.to_dto(e) for e in entities]
        except Exception as e:
            logger.error(f"Erreur lors du filtrage par contributeur: {str(e)}")
            return []
