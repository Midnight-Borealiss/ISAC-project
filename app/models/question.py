"""
Question Model - Entité Question
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Question:
    """
    Entité Question avec tous les champs métier
    """
    question: str
    category: str
    contributor: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    statut: List[str] = field(default_factory=lambda: ["À TRAITER"])
    id: Optional[str] = None

    def __post_init__(self):
        """Validation après initialisation"""
        if not self.question or not self.question.strip():
            raise ValueError("La question ne peut pas être vide")
        if not self.category:
            raise ValueError("La catégorie est requise")
        if not self.contributor:
            raise ValueError("Le contributeur est requis")

    def to_dict(self) -> dict:
        """Convertir en dictionnaire pour Airtable"""
        result = {
            "Question": self.question,
            "Catégorie": [self.category],  
            "Contributeur": self.contributor,
            "Timestamp": self.timestamp,
            "Statut": self.statut  
        }
        return result

    @staticmethod
    def from_dict(data: dict) -> 'Question':
        """Créer une Question depuis un dictionnaire"""
        # Gérer les deux formats: direct et depuis Airtable (avec 'fields')
        if 'fields' in data:
            fields = data['fields']
        else:
            fields = data
        
        question_text = fields.get('Question', '')
        if isinstance(question_text, list):
            question_text = question_text[0] if question_text else ''
        
        category = fields.get('Catégorie', [''])[0] if isinstance(fields.get('Catégorie'), list) else fields.get('Catégorie', '')
        
        contributor = fields.get('Contributeur', '')
        if isinstance(contributor, list):
            contributor = contributor[0] if contributor else ''
        
        return Question(
            id=data.get('id'),
            question=question_text,
            category=category,
            contributor=contributor,
            timestamp=fields.get('Timestamp', ''),
            statut=fields.get('Statut', ['À TRAITER'])
        )
