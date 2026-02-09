"""
Answer Model - Entité Answer (Réponse)
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Answer:
    question_id: str
    response: str
    respondent: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    statut: List[str] = field(default_factory=lambda: ["À VALIDER"])
    id: Optional[str] = None

    def __post_init__(self):
        """Validation après initialisation"""
        if not self.question_id:
            raise ValueError("L'ID de la question est requis")
        if not self.response or not self.response.strip():
            raise ValueError("La réponse ne peut pas être vide")
        if not self.respondent:
            raise ValueError("Le répondeur est requis")

    def to_dict(self) -> dict:
        """Convertir en dictionnaire pour Airtable"""
        # Statut est un SingleSelect dans Airtable, donc doit être une string
        return {
            "Question_ID": self.question_id,
            "Réponse": self.response,
            "Répondeur": self.respondent,
            "Timestamp": self.timestamp,
            "Statut": self.statut[0] if self.statut else "À VALIDER"  # SingleSelect = string
        }

    @staticmethod
    def from_dict(data: dict) -> 'Answer':
        """Créer une Answer depuis un dictionnaire"""
        # Gérer les deux formats: direct et depuis Airtable (avec 'fields')
        if 'fields' in data:
            fields = data['fields']
        else:
            fields = data
        
        question_id = fields.get('Question_ID', '')
        if isinstance(question_id, list):
            question_id = question_id[0] if question_id else ''
        
        response = fields.get('Réponse', '')
        if isinstance(response, list):
            response = response[0] if response else ''
        
        respondent = fields.get('Répondeur', '')
        if isinstance(respondent, list):
            respondent = respondent[0] if respondent else ''
        
        # Normaliser statut en liste
        statut = fields.get('Statut', ['À VALIDER'])
        if isinstance(statut, str):
            statut = [statut]
        
        return Answer(
            id=data.get('id'),
            question_id=question_id,
            response=response,
            respondent=respondent,
            timestamp=fields.get('Timestamp', ''),
            statut=statut
        )
