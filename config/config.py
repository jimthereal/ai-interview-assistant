"""
Configuration management for AI Interview Assistant
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Key - Groq only
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Model Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Vector Database
    BASE_DIR = Path(__file__).resolve().parent.parent
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(BASE_DIR / "data" / "chroma_db"))
    USE_EMBEDDINGS = os.getenv("USE_EMBEDDINGS", "false").lower() == "true"  # Disable for low memory
    
    # Application Settings
    MAX_QUESTIONS_PER_SESSION = int(os.getenv("MAX_QUESTIONS_PER_SESSION", "10"))
    ANSWER_MAX_TOKENS = int(os.getenv("ANSWER_MAX_TOKENS", "500"))
    
    # Data Paths
    DATA_DIR = BASE_DIR / "data"
    QUESTIONS_FILE = DATA_DIR / "interview_questions.json"
    
    # Supported Categories
    CATEGORIES = [
        "Python",
        "Data Structures & Algorithms",
        "System Design",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Computer Vision",
        "SQL & Databases",
        "Cloud Computing",
        "DevOps",
        "Behavioral",
        "General Software Engineering"
    ]
    
    DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is required.\n"
                "Get a FREE API key at: https://console.groq.com/\n"
                "Then add it to your .env file."
            )
        
        # Create necessary directories
        cls.DATA_DIR.mkdir(exist_ok=True)
        Path(cls.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        
        return True

# Validate configuration on import
Config.validate()
