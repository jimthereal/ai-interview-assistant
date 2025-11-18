"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Job Description Models
class JobDescriptionRequest(BaseModel):
    job_description: str = Field(..., min_length=50, description="Job description text")


class SkillExtraction(BaseModel):
    required_skills: List[str]
    preferred_skills: List[str]
    experience_level: str
    job_role: str


class JobDescriptionResponse(BaseModel):
    analysis: SkillExtraction
    summary: str
    matched_questions: List[Dict[str, Any]]


# Question Models
class QuestionQuery(BaseModel):
    category: Optional[str] = None
    difficulty: Optional[str] = None
    search_query: Optional[str] = None
    limit: int = Field(10, ge=1, le=50)


class Question(BaseModel):
    id: str
    question: str
    category: str
    difficulty: str
    hints: Optional[List[str]] = []


class QuestionListResponse(BaseModel):
    questions: List[Question]
    total: int


# Answer Models
class GenerateAnswerRequest(BaseModel):
    question: str
    category: str
    difficulty: str
    job_context: Optional[str] = None
    hints: Optional[List[str]] = []


class GenerateAnswerResponse(BaseModel):
    answer: str
    formatted: bool


class EvaluateAnswerRequest(BaseModel):
    question: str
    user_answer: str
    category: str
    difficulty: str
    model_answer: Optional[str] = None


class AnswerScores(BaseModel):
    overall: float
    clarity: float
    completeness: float
    accuracy: float
    professionalism: float


class EvaluateAnswerResponse(BaseModel):
    scores: AnswerScores
    strengths: List[str]
    improvements: List[str]
    follow_up_questions: List[str]
    feedback: str


# Progress Models
class PracticeEntry(BaseModel):
    question_id: str
    question: str
    category: str
    score: float
    timestamp: datetime


class ProgressStats(BaseModel):
    total_questions_practiced: int
    average_score: float
    category_breakdown: Dict[str, Dict[str, Any]]
    recent_practices: List[PracticeEntry]


class ProgressResponse(BaseModel):
    stats: ProgressStats
    improvement_suggestions: List[str]


# Term Explainer Models
class ExplainTermRequest(BaseModel):
    term: str = Field(..., min_length=1, max_length=100)
    context: Optional[str] = None


class ExplainTermResponse(BaseModel):
    term: str
    explanation: str
    examples: List[str]
