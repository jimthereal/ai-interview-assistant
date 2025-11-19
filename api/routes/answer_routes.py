"""
Answer generation and evaluation API routes
"""
from fastapi import APIRouter, HTTPException
from api.models.schemas import (
    GenerateAnswerRequest,
    GenerateAnswerResponse,
    EvaluateAnswerRequest,
    EvaluateAnswerResponse,
    AnswerScores
)
from src.llm_service import LLMService
from src.answer_evaluator import AnswerEvaluator

router = APIRouter()

# Initialize services
llm_service = LLMService()
evaluator = AnswerEvaluator()


@router.post("/generate-answer", response_model=GenerateAnswerResponse)
async def generate_answer(request: GenerateAnswerRequest):
    """
    Generate an AI model answer for a given interview question.
    """
    try:
        # Check if it's a behavioral question (for STAR method)
        behavioral_keywords = ["tell me about", "describe a time", "give an example"]
        use_star = any(keyword in request.question.lower() for keyword in behavioral_keywords)
        
        # Generate answer
        answer = llm_service.generate_answer(
            question=request.question,
            job_context=request.job_context,
            answer_hints=request.hints,
            use_star_method=use_star
        )
        
        return GenerateAnswerResponse(
            answer=answer,
            formatted=use_star
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Answer generation failed: {str(e)}")


@router.post("/evaluate-answer", response_model=EvaluateAnswerResponse)
async def evaluate_answer(request: EvaluateAnswerRequest):
    """
    Evaluate a user's answer and provide detailed feedback.
    """
    try:
        # Perform comprehensive evaluation
        evaluation = evaluator.evaluate_comprehensive(
            question=request.question,
            user_answer=request.user_answer,
            category=request.category,
            difficulty=request.difficulty,
            ideal_answer=request.model_answer
        )
        
        # Extract scores
        scores = AnswerScores(
            overall=evaluation.get("overall_score", 0.0),
            clarity=evaluation.get("detailed_scores", {}).get("clarity", 0.0),
            completeness=evaluation.get("detailed_scores", {}).get("completeness", 0.0),
            accuracy=evaluation.get("detailed_scores", {}).get("accuracy", 0.0),
            professionalism=evaluation.get("detailed_scores", {}).get("professionalism", 0.0)
        )
        
        return EvaluateAnswerResponse(
            scores=scores,
            strengths=evaluation.get("strengths", []),
            improvements=evaluation.get("improvements", []),
            follow_up_questions=evaluation.get("follow_up_questions", []),
            feedback=evaluation.get("feedback", "")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
