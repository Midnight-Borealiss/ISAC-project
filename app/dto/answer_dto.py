"""
Answer DTOs - Data Transfer Objects pour Answer
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Union


class AnswerDTO(BaseModel):
    """DTO pour afficher une Answer"""
    id: Optional[str] = None
    question_id: str
    response: str
    respondent: str
    timestamp: str
    statut: List[str] = Field(default_factory=lambda: ["À VALIDER"])

    @field_validator('statut', mode='before')
    @classmethod
    def normalize_statut(cls, v):
        """Normaliser statut en liste si c'est une string"""
        if isinstance(v, str):
            return [v]
        elif isinstance(v, list):
            return v
        return ["À VALIDER"]

    class Config:
        from_attributes = True


class CreateAnswerDTO(BaseModel):
    """DTO pour créer une nouvelle Answer"""
    question_id: str = Field(..., min_length=1)
    response: str = Field(..., min_length=1, max_length=2000)
    respondent: str = Field(..., min_length=1)

    class Config:
        from_attributes = True
