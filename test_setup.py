"""
Test script to verify installation and API connectivity
"""
import sys
from pathlib import Path

def test_imports():
    """Test if all required packages are installed"""
    print("Testing package imports...")
    
    required_packages = [
        ("streamlit", "Streamlit"),
        ("groq", "Groq"),
        ("chromadb", "ChromaDB"),
        ("sentence_transformers", "Sentence Transformers"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("dotenv", "python-dotenv"),
    ]
    
    failed = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"   [OK] {name}")
        except ImportError:
            print(f"   [FAIL] {name} - Not installed")
            failed.append(name)
    
    if failed:
        print(f"\nMissing packages: {', '.join(failed)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    
    print("\nAll packages installed successfully!")
    return True


def test_config():
    """Test configuration and API keys"""
    print("\nTesting configuration...")
    
    try:
        from config.config import Config
        
        # Check Groq API key
        if not Config.GROQ_API_KEY or Config.GROQ_API_KEY == "":
            print("   [FAIL] Groq API key not set")
            print("   Get FREE key at: https://console.groq.com/")
            return False
        
        print(f"   [OK] Groq API key: {'*' * 20}{Config.GROQ_API_KEY[-4:]}")
        print(f"   [OK] Model: {Config.LLM_MODEL}")
        print(f"   [OK] Embedding: local (sentence-transformers)")
        
        return True
        
    except Exception as e:
        print(f"   [FAIL] Configuration error: {str(e)}")
        return False


def test_llm_connection():
    """Test LLM API connection"""
    print("\nTesting LLM API connection...")
    
    try:
        from config.config import Config
        from src.llm_service import LLMService
        
        llm_service = LLMService()
        
        # Test with a simple prompt
        response = llm_service._call_llm(
            messages=[{"role": "user", "content": "Say 'test successful'"}],
            max_tokens=10
        )
        
        print(f"   [OK] Groq API connection successful!")
        print(f"   Response: {response}")
        return True
        
    except Exception as e:
        print(f"   [FAIL] Groq API error: {str(e)}")
        print(f"   Check your API key and internet connection")
        return False


def test_data_files():
    """Test if required data files exist"""
    print("\nTesting data files...")
    
    try:
        from config.config import Config
        
        if Config.QUESTIONS_FILE.exists():
            print(f"   [OK] Questions file found: {Config.QUESTIONS_FILE}")
            
            # Load and check format
            import json
            with open(Config.QUESTIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                question_count = len(data.get("questions", []))
                print(f"   [OK] Loaded {question_count} questions")
            
            return True
        else:
            print(f"   [FAIL] Questions file not found: {Config.QUESTIONS_FILE}")
            return False
            
    except Exception as e:
        print(f"   [FAIL] Data file error: {str(e)}")
        return False


def test_vector_store():
    """Test vector store initialization"""
    print("\nTesting vector store...")
    
    try:
        from src.vector_store import VectorStore
        
        vector_store = VectorStore()
        stats = vector_store.get_stats()
        
        print(f"   [OK] Vector store initialized")
        print(f"   [OK] Questions in database: {stats['total_questions']}")
        
        return True
        
    except Exception as e:
        print(f"   [FAIL] Vector store error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("AI Interview Assistant - Installation Test")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("LLM Connection", test_llm_connection),
        ("Data Files", test_data_files),
        ("Vector Store", test_vector_store),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] Unexpected error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"   {status}: {test_name}")
    
    print("=" * 60)
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll tests passed! You're ready to run the application.")
        print("   Start with: streamlit run app.py")
        return 0
    else:
        print("\nSome tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
