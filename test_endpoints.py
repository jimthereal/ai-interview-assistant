import requests
import json

print("Testing AI Interview Assistant API Endpoints\n")
print("=" * 50)

BASE_URL = "http://127.0.0.1:8000"

# Test 1: Get Categories
print("\n1. Testing GET /api/categories")
try:
    r = requests.get(f"{BASE_URL}/api/categories")
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ SUCCESS - Found {len(data['categories'])} categories")
        print(f"   Categories: {data['categories'][:3]}...")
    else:
        print(f"   ❌ FAILED - {r.text[:200]}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 2: Get Questions
print("\n2. Testing GET /api/questions?limit=5")
try:
    r = requests.get(f"{BASE_URL}/api/questions", params={"limit": 5})
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ SUCCESS - Found {data['total']} questions")
        if data['questions']:
            print(f"   First question: {data['questions'][0]['question'][:60]}...")
    else:
        print(f"   ❌ FAILED - {r.text[:200]}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 3: Explain Term
print("\n3. Testing POST /api/explain-term")
try:
    r = requests.post(f"{BASE_URL}/api/explain-term", params={"term": "Docker"})
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ SUCCESS - Got explanation")
        print(f"   Explanation: {data['explanation'][:80]}...")
    else:
        print(f"   ❌ FAILED - {r.text[:200]}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "=" * 50)
print("Testing Complete!\n")
