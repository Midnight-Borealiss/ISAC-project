"""
Validation Mapper - Conversion Validation Entity ↔ DTO
"""
from app.models import Validation
from app.dto import ValidationDTO
from datetime import datetime
import pytz


class ValidationMapper:
    """Mapper statique pour convertir Validation Entity ↔ DTO"""

    @staticmethod
    def to_entity(validation_dto: ValidationDTO, answer_id: str = None) -> Validation:
        """Convertir un ValidationDTO en Validation Entity"""
        statut = "APPROUVÉE" if validation_dto.is_approved else "REJETÉE"
        
        return Validation(
            answer_id=answer_id or validation_dto.answer_id,
            statut=statut,
            validation_timestamp=datetime.now(pytz.utc).isoformat(),
            admin_notes=validation_dto.admin_notes
        )

    @staticmethod
    def from_airtable(data: dict) -> Validation:
        """Créer une Validation depuis les données Airtable"""
        return Validation.from_dict(data)
