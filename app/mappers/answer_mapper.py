"""
Answer Mapper - Conversion Answer Entity ↔ DTO
"""
from app.models import Answer
from app.dto import AnswerDTO, CreateAnswerDTO
from datetime import datetime
import pytz


class AnswerMapper:
    """Mapper statique pour convertir Answer Entity ↔ DTO"""

    @staticmethod
    def to_dto(answer: Answer) -> AnswerDTO:
        """Convertir une Answer Entity en DTO"""
        return AnswerDTO(
            id=answer.id,
            question_id=answer.question_id,
            response=answer.response,
            respondent=answer.respondent,
            timestamp=answer.timestamp,
            statut=answer.statut
        )

    @staticmethod
    def to_entity(create_dto: CreateAnswerDTO) -> Answer:
        """Convertir un CreateAnswerDTO en Answer Entity"""
        return Answer(
            question_id=create_dto.question_id,
            response=create_dto.response,
            respondent=create_dto.respondent,
            timestamp=datetime.now(pytz.utc).isoformat(),
            statut=["À VALIDER"]
        )

    @staticmethod
    def from_airtable(data: dict) -> Answer:
        """Créer une Answer depuis les données Airtable"""
        return Answer.from_dict(data)
