"""
Job Description Analysis API routes
"""
from fastapi import APIRouter, HTTPException
from api.models.schemas import JobDescriptionRequest, JobDescriptionResponse
from src.jd_analyzer import JDAnalyzer
from src.vector_store import VectorStore
from config.config import Config

router = APIRouter()

# Initialize services
jd_analyzer = JDAnalyzer()
vector_store = VectorStore()


@router.post("/analyze-jd", response_model=JobDescriptionResponse)
async def analyze_job_description(request: JobDescriptionRequest):
    """
    Analyze a job description and return extracted skills, requirements,
    and matched interview questions.
    """
    try:
        # Analyze job description
        analysis = jd_analyzer.analyze(request.job_description)
        
        # Generate search query for relevant questions
        search_query = jd_analyzer.generate_search_query(analysis)
        
        # Find matched questions
        matched_questions = vector_store.search_questions(
            query=search_query,
            n_results=10
        )
        
        return JobDescriptionResponse(
            analysis=analysis,
            summary=f"Position: {analysis.get('job_role', 'Not specified')}. "
                   f"Level: {analysis.get('experience_level', 'Not specified')}. "
                   f"Key skills: {', '.join(analysis.get('required_skills', [])[:5])}",
            matched_questions=matched_questions
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/explain-term")
async def explain_term(term: str, context: str = None):
    """
    Explain a technical term in simple language.
    """
    try:
        explanation = jd_analyzer.explain_term(term, context)
        return {
            "term": term,
            "explanation": explanation,
            "examples": []
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")
