"""
Utility script to initialize or reset the vector database
"""
from src.vector_store import VectorStore
from config.config import Config
import sys


def main():
    """Initialize vector database with questions"""
    print("AI Interview Assistant - Database Initialization")
    print("=" * 60)
    
    # Create vector store
    print("\nCreating vector store...")
    vector_store = VectorStore()
    
    # Check if questions file exists
    if not Config.QUESTIONS_FILE.exists():
        print(f"Error: Questions file not found at {Config.QUESTIONS_FILE}")
        print("Please ensure interview_questions.json exists in the data directory.")
        sys.exit(1)
    
    # Clear existing database
    print("\nClearing existing database...")
    vector_store.clear_database()
    
    # Load questions
    print(f"\nLoading questions from {Config.QUESTIONS_FILE}...")
    vector_store.load_questions_from_file(Config.QUESTIONS_FILE)
    
    # Get stats
    stats = vector_store.get_stats()
    print(f"\nDatabase initialized successfully!")
    print(f"   Total questions: {stats['total_questions']}")
    print(f"   Embedding model: {stats['embedding_model']}")
    
    # Test search
    print("\nTesting semantic search...")
    test_query = "machine learning python experience"
    results = vector_store.search_questions(test_query, n_results=3)
    
    print(f"\n   Query: '{test_query}'")
    print(f"   Found {len(results)} results:\n")
    
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['question'][:80]}...")
        print(f"      Category: {result['category']}, "
              f"Difficulty: {result['difficulty']}, "
              f"Relevance: {result['relevance_score']:.3f}\n")
    
    print("=" * 60)
    print("Setup complete! You can now run the application with:")
    print("   streamlit run app.py")


if __name__ == "__main__":
    main()
