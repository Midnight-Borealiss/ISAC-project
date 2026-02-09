"""
Question DTOs - Data Transfer Objects pour Question
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class QuestionDTO(BaseModel):
    """DTO pour afficher une Question"""
    id: Optional[str] = None
    question: str
    category: str
    contributor: str
    timestamp: str
    statut: List[str] = Field(default_factory=lambda: ["À TRAITER"])

    class Config:
        from_attributes = True


class CreateQuestionDTO(BaseModel):
    """DTO pour créer une nouvelle Question"""
    question: str = Field(..., min_length=1, max_length=500)
    category: str
    contributor: str = Field(..., min_length=1)

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        VALID_CATEGORIES = ["Académique", "Administratif", "Financier", "Autre"]
        if v not in VALID_CATEGORIES:
            raise ValueError(f"La catégorie doit être l'une de {VALID_CATEGORIES}")
        return v

    class Config:
        from_attributes = True
