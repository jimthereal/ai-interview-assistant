"""
Quick test script for FastAPI backend
Run this after starting the API server to verify all endpoints work
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n[TEST] Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_categories():
    print("\n[TEST] Get Categories...")
    response = requests.get(f"{BASE_URL}/api/categories")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Categories: {data.get('categories', [])[:5]}")
    return response.status_code == 200

def test_questions():
    print("\n[TEST] Get Questions...")
    response = requests.get(f"{BASE_URL}/api/questions?limit=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {data.get('total', 0)} questions")
    if data.get('questions'):
        print(f"First question: {data['questions'][0]['question'][:100]}...")
    return response.status_code == 200

def test_jd_analysis():
    print("\n[TEST] Job Description Analysis...")
    sample_jd = """
    We are looking for a Senior Python Developer with 5+ years of experience.
    Required skills: Python, FastAPI, React, PostgreSQL, AWS, Docker.
    Experience with machine learning and RAG systems is a plus.
    """
    
    response = requests.post(
        f"{BASE_URL}/api/analyze-jd",
        json={"job_description": sample_jd}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Summary: {data.get('summary', '')}")
        print(f"Matched questions: {len(data.get('matched_questions', []))}")
    return response.status_code == 200

def test_generate_answer():
    print("\n[TEST] Generate Answer...")
    response = requests.post(
        f"{BASE_URL}/api/generate-answer",
        json={
            "question": "What is FastAPI and why would you use it?",
            "category": "Technical",
            "difficulty": "Medium",
            "hints": ["Modern framework", "Type safety", "Auto documentation"]
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Answer (first 200 chars): {data.get('answer', '')[:200]}...")
    return response.status_code == 200

def test_evaluate_answer():
    print("\n[TEST] Evaluate Answer...")
    response = requests.post(
        f"{BASE_URL}/api/evaluate-answer",
        json={
            "question": "What is FastAPI?",
            "user_answer": "FastAPI is a modern Python web framework for building APIs.",
            "category": "Technical",
            "difficulty": "Easy"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        scores = data.get('scores', {})
        print(f"Overall Score: {scores.get('overall', 0)}/10")
        print(f"Strengths: {len(data.get('strengths', []))}")
        print(f"Improvements: {len(data.get('improvements', []))}")
    return response.status_code == 200

def main():
    print("=" * 60)
    print("FastAPI Backend Test Suite")
    print("=" * 60)
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the server is running: uvicorn api.main:app --reload")
    
    tests = [
        ("Health Check", test_health),
        ("Categories", test_categories),
        ("Questions List", test_questions),
        ("JD Analysis", test_jd_analysis),
        ("Generate Answer", test_generate_answer),
        ("Evaluate Answer", test_evaluate_answer),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, "PASS" if passed else "FAIL"))
        except Exception as e:
            print(f"ERROR: {str(e)}")
            results.append((name, "ERROR"))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    for name, status in results:
        status_symbol = "[OK]" if status == "PASS" else "[FAIL]"
        print(f"{status_symbol} {name}")
    
    passed = sum(1 for _, status in results if status == "PASS")
    print(f"\nPassed: {passed}/{len(results)}")

if __name__ == "__main__":
    main()
