"""
Job Description Analysis API routes
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from api.models.schemas import JobDescriptionRequest, JobDescriptionResponse
from src.jd_analyzer import JDAnalyzer
from src.vector_store import VectorStore
from src.content_extractor import ContentExtractor
from config.config import Config

router = APIRouter()


class URLRequest(BaseModel):
    url: str

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


@router.post("/analyze-jd-file", response_model=JobDescriptionResponse)
async def analyze_job_description_file(file: UploadFile = File(...)):
    """
    Analyze a job description from an uploaded PDF or DOCX file
    """
    try:
        # Validate file type
        file_type = ContentExtractor.detect_file_type(file.filename)
        
        if not file_type:
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Only PDF and DOCX files are supported."
            )
        
        # Read file content
        file_bytes = await file.read()
        
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Extract text based on file type
        if file_type == 'pdf':
            job_description = ContentExtractor.extract_from_pdf(file_bytes)
        elif file_type == 'docx':
            job_description = ContentExtractor.extract_from_docx(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(
                status_code=400, 
                detail="Could not extract sufficient content from the file"
            )
        
        # Analyze job description (same as text endpoint)
        analysis = jd_analyzer.analyze(job_description)
        search_query = jd_analyzer.generate_search_query(analysis)
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
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File analysis failed: {str(e)}")


@router.post("/analyze-jd-url", response_model=JobDescriptionResponse)
async def analyze_job_description_url(request: URLRequest):
    """
    Analyze a job description from a web page URL
    """
    try:
        # Validate URL format
        if not ContentExtractor.is_valid_url(request.url):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Extract content from URL
        job_description = ContentExtractor.extract_from_url(request.url)
        
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(
                status_code=400, 
                detail="Could not extract sufficient content from the URL"
            )
        
        # Analyze job description (same as text endpoint)
        analysis = jd_analyzer.analyze(job_description)
        search_query = jd_analyzer.generate_search_query(analysis)
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
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL analysis failed: {str(e)}")


@router.post("/explain-term")
async def explain_term(term: str, context: str = None):
    """
    Explain a technical term in simple language.
    """
    try:
        explanation = jd_analyzer.explain_term(term, context)
        return explanation
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")
