"""
Question Mapper - Conversion Question Entity ↔ DTO
"""
from app.models import Question
from app.dto import QuestionDTO, CreateQuestionDTO
from datetime import datetime
import pytz


class QuestionMapper:
    """Mapper statique pour convertir Question Entity ↔ DTO"""

    @staticmethod
    def to_dto(question: Question) -> QuestionDTO:
        """Convertir une Question Entity en DTO"""
        return QuestionDTO(
            id=question.id,
            question=question.question,
            category=question.category,
            contributor=question.contributor,
            timestamp=question.timestamp,
            statut=question.statut
        )

    @staticmethod
    def to_entity(create_dto: CreateQuestionDTO) -> Question:
        """Convertir un CreateQuestionDTO en Question Entity"""
        return Question(
            question=create_dto.question,
            category=create_dto.category,
            contributor=create_dto.contributor,
            timestamp=datetime.now(pytz.utc).isoformat(),
            statut=["À TRAITER"]
        )

    @staticmethod
    def from_airtable(data: dict) -> Question:
        """Créer une Question depuis les données Airtable"""
        return Question.from_dict(data)
