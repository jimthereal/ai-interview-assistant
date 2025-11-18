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
    
    # LLM Provider Selection
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Model Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-70b-versatile")
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Vector Database
    BASE_DIR = Path(__file__).resolve().parent.parent
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(BASE_DIR / "data" / "chroma_db"))
    
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
        # Check if LLM provider is configured
        if cls.LLM_PROVIDER == "groq" and not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is required when using Groq provider.\n"
                "Get a FREE API key at: https://console.groq.com/\n"
                "Then add it to your .env file."
            )
        elif cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY is required when using Anthropic provider.\n"
                "Please set it in .env file or switch to Groq (free)."
            )
        elif cls.LLM_PROVIDER not in ["groq", "anthropic", "ollama"]:
            raise ValueError(
                f"Unknown LLM_PROVIDER: {cls.LLM_PROVIDER}\n"
                "Valid options: groq, anthropic, ollama"
            )
        
        # Create necessary directories
        cls.DATA_DIR.mkdir(exist_ok=True)
        Path(cls.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        
        return True

# Validate configuration on import
Config.validate()
