"""
Question retrieval API routes
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from api.models.schemas import QuestionListResponse, Question
from src.vector_store import VectorStore
import json

router = APIRouter()

# Initialize vector store
vector_store = VectorStore()

# Load questions database
with open("data/interview_questions.json", "r", encoding="utf-8") as f:
    questions_db = json.load(f)


@router.get("/questions", response_model=QuestionListResponse)
async def get_questions(
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    search: Optional[str] = Query(None, description="Semantic search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results")
):
    """
    Retrieve interview questions with optional filtering and semantic search.
    """
    try:
        if search:
            # Semantic search using vector store
            results = vector_store.search_questions(query=search, n_results=limit)
            questions = [
                Question(
                    id=r.get("id", str(i)),
                    question=r.get("question", ""),
                    category=r.get("category", "General"),
                    difficulty=r.get("difficulty", "Medium"),
                    hints=r.get("answer_hints", [])
                )
                for i, r in enumerate(results)
            ]
        else:
            # Filter questions by category and/or difficulty
            filtered = questions_db.copy()
            
            if category:
                filtered = [q for q in filtered if q.get("category", "").lower() == category.lower()]
            
            if difficulty:
                filtered = [q for q in filtered if q.get("difficulty", "").lower() == difficulty.lower()]
            
            # Limit results
            filtered = filtered[:limit]
            
            questions = [
                Question(
                    id=str(i),
                    question=q.get("question", ""),
                    category=q.get("category", "General"),
                    difficulty=q.get("difficulty", "Medium"),
                    hints=q.get("answer_hints", [])
                )
                for i, q in enumerate(filtered)
            ]
        
        return QuestionListResponse(
            questions=questions,
            total=len(questions)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve questions: {str(e)}")


@router.get("/questions/{question_id}")
async def get_question_by_id(question_id: str):
    """
    Get a specific question by ID.
    """
    try:
        question_idx = int(question_id)
        if 0 <= question_idx < len(questions_db):
            q = questions_db[question_idx]
            return Question(
                id=question_id,
                question=q.get("question", ""),
                category=q.get("category", "General"),
                difficulty=q.get("difficulty", "Medium"),
                hints=q.get("answer_hints", [])
            )
        else:
            raise HTTPException(status_code=404, detail="Question not found")
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid question ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def get_categories():
    """
    Get list of all question categories.
    """
    try:
        categories = list(set(q.get("category", "General") for q in questions_db))
        return {"categories": sorted(categories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
