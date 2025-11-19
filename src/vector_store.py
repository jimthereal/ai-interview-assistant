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
        
        # Initialize local embedding model only if embeddings are enabled
        if Config.USE_EMBEDDINGS:
            print("Using local embeddings (sentence-transformers)")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            print("Embeddings disabled - using keyword-based search for production")
            self.embedding_model = None
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="interview_questions",
            metadata={"hnsw:space": "cosine"}
        )
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using local model"""
        if self.embedding_model:
            return self.embedding_model.encode(text).tolist()
        else:
            # Return dummy embedding for production (won't be used)
            return [0.0] * 384
    
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
        Search for relevant questions using semantic search or keyword matching
        
        Args:
            query: Search query (e.g., job description or skills)
            n_results: Number of results to return
            category: Filter by category
            difficulty: Filter by difficulty
            
        Returns:
            List of relevant questions with metadata
        """
        # If embeddings disabled, use keyword-based search from JSON
        if not Config.USE_EMBEDDINGS:
            return self._keyword_search(query, n_results, category, difficulty)
        
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
    
    def _keyword_search(
        self, 
        query: str, 
        n_results: int = 5,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> List[Dict]:
        """
        Lightweight keyword-based search for production (low memory)
        """
        # Load questions from JSON
        questions_file = Config.BASE_DIR / "data" / "interview_questions.json"
        with open(questions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_questions = data.get('questions', [])
        
        # Filter by category/difficulty
        filtered = []
        for q in all_questions:
            if category and q.get('category') != category:
                continue
            if difficulty and q.get('difficulty') != difficulty:
                continue
            filtered.append(q)
        
        # Score by keyword matching
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_questions = []
        for q in filtered:
            score = 0
            # Check question text
            q_text = q.get('question', '').lower()
            score += sum(1 for word in query_words if word in q_text) * 2
            
            # Check keywords
            keywords = q.get('keywords', [])
            if isinstance(keywords, str):
                keywords = [k.strip() for k in keywords.split(',')]
            score += sum(1 for kw in keywords if kw.lower() in query_lower) * 3
            
            # Check category
            if q.get('category', '').lower() in query_lower:
                score += 2
            
            if score > 0:
                scored_questions.append((score, q))
        
        # Sort by score and return top results
        scored_questions.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for _, q in scored_questions[:n_results]:
            hints = q.get('answer_hints', '')
            if isinstance(hints, str):
                hints = [hints] if hints else []
            
            results.append({
                'question': q.get('question', ''),
                'category': q.get('category', ''),
                'difficulty': q.get('difficulty', ''),
                'answer_hints': hints,
                'keywords': q.get('keywords', []) if isinstance(q.get('keywords'), list) else []
            })
        
        return results
    
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
