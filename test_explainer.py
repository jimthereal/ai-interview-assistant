import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_explain_term():
    print("\nTesting POST /api/explain-term")
    term = "API"
    try:
        r = requests.post(f"{BASE_URL}/api/explain-term", params={"term": term})
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            print("   ✅ Response is valid JSON")
            
            required_keys = ["definition", "analogy", "key_points", "example", "why_it_matters"]
            missing_keys = [key for key in required_keys if key not in data]
            
            if not missing_keys:
                print("   ✅ All required keys present")
                print(f"   Definition: {data['definition'][:50]}...")
                print(f"   Analogy: {data['analogy'][:50]}...")
            else:
                print(f"   ❌ Missing keys: {missing_keys}")
                print(f"   Response: {data}")
        else:
            print(f"   ❌ FAILED - {r.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")

if __name__ == "__main__":
    test_explain_term()
