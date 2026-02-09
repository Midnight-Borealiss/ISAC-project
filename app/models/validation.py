"""
Validation Model - Entité Validation
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Validation:
    """
    Entité Validation pour la validation des réponses par l'admin
    """
    answer_id: str
    statut: str
    validation_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    admin_notes: str = ""
    id: Optional[str] = None

    def __post_init__(self):
        """Validation après initialisation"""
        if not self.answer_id:
            raise ValueError("L'ID de la réponse est requis")
        if self.statut not in ["APPROUVÉE", "REJETÉE"]:
            raise ValueError("Le statut doit être APPROUVÉE ou REJETÉE")

    def to_dict(self) -> dict:
        """Convertir en dictionnaire pour Airtable"""
        return {
            "Answer_ID": self.answer_id,  # Champ texte simple
            "Statut": self.statut,  # Déjà une string
            "Validation_Timestamp": self.validation_timestamp,
            "Notes_Admin": self.admin_notes
        }

    @staticmethod
    def from_dict(data: dict) -> 'Validation':
        """Créer une Validation depuis un dictionnaire"""
        # Gérer les deux formats: direct et depuis Airtable (avec 'fields')
        if 'fields' in data:
            fields = data['fields']
        else:
            fields = data
        
        answer_id = fields.get('Answer_ID', '')
        if isinstance(answer_id, list):
            answer_id = answer_id[0] if answer_id else ''
        
        statut = fields.get('Statut', '')
        if isinstance(statut, list):
            statut = statut[0] if statut else ''
        
        return Validation(
            id=data.get('id'),
            answer_id=answer_id,
            statut=statut,
            validation_timestamp=fields.get('Validation_Timestamp', ''),
            admin_notes=fields.get('Notes_Admin', '')
        )
