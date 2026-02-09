"""
Validation DTOs - Data Transfer Objects pour Validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ValidationDTO(BaseModel):
    """DTO pour créer une Validation"""
    answer_id: str = Field(..., min_length=1)
    is_approved: bool
    admin_notes: str = Field(default="")

    @field_validator('admin_notes')
    @classmethod
    def validate_notes(cls, v):
        if len(v) > 1000:
            raise ValueError("Les notes ne peuvent pas dépasser 1000 caractères")
        return v

    class Config:
        from_attributes = True
