"""
Vector Store Module - RAG Core
Handles embeddings, vector storage, and semantic search using ChromaDB
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from config.config import Config

class VectorStore:
    """Manages vector database operations for RAG"""
    
    def __init__(self):
        """
        Initialize vector store with ChromaDB using local embeddings
        """
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize local embedding model
        print("Using local embeddings (sentence-transformers)")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="interview_questions",
            metadata={"hnsw:space": "cosine"}
        )
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using local model"""
        return self.embedding_model.encode(text).tolist()
    
    def add_questions(self, questions: List[Dict]):
        """
        Add interview questions to vector store
        
        Args:
            questions: List of question dictionaries with fields:
                - question: The question text
                - category: Question category
                - difficulty: Easy/Medium/Hard
                - answer_hints: Optional hints for answering
                - keywords: List of relevant keywords
        """
        documents = []
        metadatas = []
        ids = []
        
        for idx, q in enumerate(questions):
            # Create rich document text for better embedding
            doc_text = f"{q['question']} {' '.join(q.get('keywords', []))}"
            documents.append(doc_text)
            
            metadatas.append({
                "category": q.get("category", "General"),
                "difficulty": q.get("difficulty", "Medium"),
                "question": q["question"],
                "answer_hints": q.get("answer_hints", ""),
                "keywords": ",".join(q.get("keywords", []))
            })
            
            ids.append(f"q_{idx}")
        
        # Add to collection
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Added {len(questions)} questions to vector store")
    
    def search_questions(
        self, 
        query: str, 
        n_results: int = 5,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for relevant questions using semantic search
        
        Args:
            query: Search query (e.g., job description or skills)
            n_results: Number of results to return
            category: Filter by category
            difficulty: Filter by difficulty
            
        Returns:
            List of relevant questions with metadata
        """
        where_filter = {}
        
        if category:
            where_filter["category"] = category
        if difficulty:
            where_filter["difficulty"] = difficulty
        
        # Perform semantic search
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        # Format results
        questions = []
        if results['metadatas'] and results['metadatas'][0]:
            for metadata, distance in zip(results['metadatas'][0], results['distances'][0]):
                questions.append({
                    "question": metadata["question"],
                    "category": metadata["category"],
                    "difficulty": metadata["difficulty"],
                    "answer_hints": metadata["answer_hints"],
                    "keywords": metadata["keywords"].split(",") if metadata["keywords"] else [],
                    "relevance_score": 1 - distance  # Convert distance to similarity
                })
        
        return questions
    
    def load_questions_from_file(self, file_path: Path):
        """Load questions from JSON file and add to vector store"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            questions = data.get("questions", [])
            self.add_questions(questions)
    
    def clear_database(self):
        """Clear all data from the collection"""
        self.client.delete_collection("interview_questions")
        self.collection = self.client.get_or_create_collection(
            name="interview_questions",
            metadata={"hnsw:space": "cosine"}
        )
        print("Vector database cleared")
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        count = self.collection.count()
        return {
            "total_questions": count,
            "embedding_model": "all-MiniLM-L6-v2 (local)"
        }


def initialize_vector_store(force_reload: bool = False) -> VectorStore:
    """
    Initialize and populate vector store
    
    Args:
        force_reload: If True, clear existing data and reload
        
    Returns:
        Initialized VectorStore instance
    """
    vector_store = VectorStore()
    
    # Check if already populated
    stats = vector_store.get_stats()
    
    if stats["total_questions"] == 0 or force_reload:
        if force_reload:
            vector_store.clear_database()
        
        # Load questions from file
        if Config.QUESTIONS_FILE.exists():
            vector_store.load_questions_from_file(Config.QUESTIONS_FILE)
        else:
            print("Warning: Questions file not found. Please run data generation.")
    
    return vector_store
