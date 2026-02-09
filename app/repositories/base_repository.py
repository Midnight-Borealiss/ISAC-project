"""
Base Repository - Interface abstraite
"""
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Interface abstraite pour tous les repositories"""

    @abstractmethod
    def create(self, entity: T) -> T:
        """Créer une entité"""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Récupérer une entité par ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Récupérer toutes les entités"""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Mettre à jour une entité"""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Supprimer une entité"""
        pass
