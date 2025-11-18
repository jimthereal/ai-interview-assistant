"""
Progress tracking API routes
"""
from fastapi import APIRouter, HTTPException
from api.models.schemas import ProgressResponse, ProgressStats, PracticeEntry
from src.answer_evaluator import AnswerEvaluator
from typing import List
from datetime import datetime

router = APIRouter()

# Initialize evaluator (handles progress tracking)
evaluator = AnswerEvaluator()


@router.get("/progress", response_model=ProgressResponse)
async def get_progress():
    """
    Get user's practice statistics and progress.
    """
    try:
        # Get stats from evaluator
        stats_data = evaluator.get_statistics()
        
        # Format practice history
        recent_practices = []
        for entry in stats_data.get("history", [])[:10]:  # Last 10 practices
            recent_practices.append(
                PracticeEntry(
                    question_id=entry.get("question_id", ""),
                    question=entry.get("question", ""),
                    category=entry.get("category", "General"),
                    score=entry.get("score", 0.0),
                    timestamp=entry.get("timestamp", datetime.now())
                )
            )
        
        # Create stats object
        stats = ProgressStats(
            total_questions_practiced=stats_data.get("total_questions", 0),
            average_score=stats_data.get("average_score", 0.0),
            category_breakdown=stats_data.get("by_category", {}),
            recent_practices=recent_practices
        )
        
        # Generate improvement suggestions
        suggestions = []
        if stats.average_score < 7.0:
            suggestions.append("Focus on providing more detailed and structured answers")
        
        weak_categories = [
            cat for cat, data in stats.category_breakdown.items()
            if data.get("average_score", 0) < 6.5
        ]
        if weak_categories:
            suggestions.append(f"Practice more questions in: {', '.join(weak_categories)}")
        
        if stats.total_questions_practiced < 10:
            suggestions.append("Complete at least 10 practice questions to see meaningful progress")
        
        return ProgressResponse(
            stats=stats,
            improvement_suggestions=suggestions
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve progress: {str(e)}")


@router.delete("/progress")
async def reset_progress():
    """
    Reset all progress data (for testing/demo purposes).
    """
    try:
        evaluator.reset_statistics()
        return {"message": "Progress data reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset progress: {str(e)}")
