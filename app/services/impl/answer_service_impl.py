"""
Answer Service Implementation
"""
import logging
from typing import List, Optional
from app.dto import AnswerDTO, CreateAnswerDTO
from app.mappers import AnswerMapper
from app.repositories.impl import AnswerRepositoryImpl
from app.services.answer_service import AnswerService

logger = logging.getLogger(__name__)


class AnswerServiceImpl(AnswerService):
    """Implémentation du service Answer"""

    def __init__(self):
        self.answer_repo = AnswerRepositoryImpl()

    def create_answer(self, create_dto: CreateAnswerDTO) -> AnswerDTO:
        """Créer une nouvelle réponse"""
        try:
            # Convertir DTO → Entity
            answer_entity = AnswerMapper.to_entity(create_dto)
            
            # Persister
            saved_entity = self.answer_repo.create(answer_entity)
            
            # Convertir Entity → DTO
            return AnswerMapper.to_dto(saved_entity)
        except Exception as e:
            logger.error(f"Erreur lors de la création de la réponse: {str(e)}")
            raise

    def get_answer(self, answer_id: str) -> Optional[AnswerDTO]:
        """Récupérer une réponse"""
        try:
            entity = self.answer_repo.get_by_id(answer_id)
            return AnswerMapper.to_dto(entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la réponse: {str(e)}")
            return None

    def get_answers_for_question(self, question_id: str) -> List[AnswerDTO]:
        """Récupérer les réponses pour une question"""
        try:
            entities = self.answer_repo.get_by_question_id(question_id)
            return [AnswerMapper.to_dto(e) for e in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réponses: {str(e)}")
            return []

    def get_pending_answers(self) -> List[AnswerDTO]:
        """Récupérer les réponses en attente de validation"""
        try:
            entities = self.answer_repo.get_pending()
            return [AnswerMapper.to_dto(e) for e in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réponses en attente: {str(e)}")
            return []

    def get_all_answers(self) -> List[AnswerDTO]:
        """Récupérer toutes les réponses"""
        try:
            entities = self.answer_repo.get_all()
            return [AnswerMapper.to_dto(e) for e in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réponses: {str(e)}")
            return []
