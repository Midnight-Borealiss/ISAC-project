"""
App initialization - Central exports for easy imports
"""

# Models
from app.models import Question, Answer, Validation

# DTOs
from app.dto import (
    QuestionDTO, CreateQuestionDTO,
    AnswerDTO, CreateAnswerDTO,
    ValidationDTO
)

# Mappers
from app.mappers import QuestionMapper, AnswerMapper, ValidationMapper

# Repositories
from app.repositories.impl import (
    QuestionRepositoryImpl,
    AnswerRepositoryImpl,
    ValidationRepositoryImpl
)

# Services
from app.services.impl import (
    QuestionServiceImpl,
    AnswerServiceImpl,
    ValidationServiceImpl
)

# Controllers
from app.controllers import (
    QuestionController,
    AnswerController,
    ValidationController
)

__all__ = [
    # Models
    'Question', 'Answer', 'Validation',
    
    # DTOs
    'QuestionDTO', 'CreateQuestionDTO',
    'AnswerDTO', 'CreateAnswerDTO',
    'ValidationDTO',
    
    # Mappers
    'QuestionMapper', 'AnswerMapper', 'ValidationMapper',
    
    # Repositories
    'QuestionRepositoryImpl', 'AnswerRepositoryImpl', 'ValidationRepositoryImpl',
    
    # Services
    'QuestionServiceImpl', 'AnswerServiceImpl', 'ValidationServiceImpl',
    
    # Controllers
    'QuestionController', 'AnswerController', 'ValidationController'
]
