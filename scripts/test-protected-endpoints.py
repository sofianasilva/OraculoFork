#!/usr/bin/env python3
"""
Test script for protected FastAPI endpoints (Baby-step 4).
"""
import requests
import json

DJANGO_BASE_URL = "http://localhost:8001"
FASTAPI_BASE_URL = "http://localhost:8000"

def get_jwt_token():
    """Get a valid JWT token from Django auth service."""
    print("🔑 Getting JWT token from Django...")
    
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{DJANGO_BASE_URL}/api/auth/login/", json=login_data)
    
    if response.status_code == 200:
        token = response.json()['tokens']['access']
        print(f"✅ Got JWT token: {token[:50]}...")
        return token
    else:
        print(f"❌ Failed to get token: {response.status_code}")
        return None

def test_ask_endpoint_without_auth():
    """Test /ask endpoint without authentication."""
    print("\n🧪 Testing POST /ask without authentication...")
    
    question_data = {
        "question": "How many repositories do we have?"
    }
    
    response = requests.post(f"{FASTAPI_BASE_URL}/ask", json=question_data)
    
    if response.status_code in [401, 403]:
        print("✅ Correctly rejected unauthenticated request")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_ask_endpoint_with_auth(token):
    """Test /ask endpoint with valid authentication."""
    print("\n🧪 Testing POST /ask with authentication...")
    
    headers = {"Authorization": f"Bearer {token}"}
    question_data = {
        "question": "How many repositories do we have?"
    }
    
    response = requests.post(f"{FASTAPI_BASE_URL}/ask", json=question_data, headers=headers)
    
    if response.status_code == 200:
        print("✅ Successfully accessed protected /ask endpoint")
        result = response.json()
        print(f"Response preview: {str(result)[:200]}...")
        
        # Check if user context was added
        if isinstance(result, dict) and "user_context" in result:
            print(f"✅ User context added: {result['user_context']}")
        
        return True
    else:
        print(f"❌ Request failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_static_endpoint_without_auth():
    """Test /static/graficos endpoint without authentication."""
    print("\n🧪 Testing GET /static/graficos without authentication...")
    
    # Test with a non-existent file (should still require auth)
    response = requests.get(f"{FASTAPI_BASE_URL}/static/graficos/test.png")
    
    if response.status_code in [401, 403]:
        print("✅ Correctly rejected unauthenticated request")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_static_endpoint_with_auth(token):
    """Test /static/graficos endpoint with valid authentication."""
    print("\n🧪 Testing GET /static/graficos with authentication...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with a non-existent file (should return 404 but be authenticated)
    response = requests.get(f"{FASTAPI_BASE_URL}/static/graficos/test.png", headers=headers)
    
    if response.status_code == 404:
        print("✅ Successfully authenticated, file not found (expected)")
        return True
    elif response.status_code == 200:
        print("✅ Successfully accessed static file")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_public_endpoints_still_work():
    """Test that public endpoints still work without authentication."""
    print("\n🧪 Testing public endpoints still work...")
    
    # Test auth/ping (should remain public)
    response = requests.get(f"{FASTAPI_BASE_URL}/auth/ping")
    
    if response.status_code == 200:
        print("✅ Public /auth/ping endpoint still works")
        return True
    else:
        print(f"❌ Public endpoint failed: {response.status_code}")
        return False

def main():
    """Run all protected endpoint tests."""
    print("🚀 Starting Protected Endpoints Tests (Baby-step 4)\n")
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Public endpoints still work
    if test_public_endpoints_still_work():
        tests_passed += 1
    
    # Test 2: Protected /ask without auth
    if test_ask_endpoint_without_auth():
        tests_passed += 1
    
    # Test 3: Protected /static without auth  
    if test_static_endpoint_without_auth():
        tests_passed += 1
    
    # Get JWT token for authenticated tests
    token = get_jwt_token()
    if token:
        # Test 4: Protected /ask with auth
        if test_ask_endpoint_with_auth(token):
            tests_passed += 1
        
        # Test 5: Protected /static with auth
        if test_static_endpoint_with_auth(token):
            tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All protected endpoint tests passed!")
        print("\n✅ Baby-step 4 validation successful")
        print("🔒 Critical endpoints are now protected with JWT authentication")
        print("\n📋 Protected endpoints:")
        print("   • POST /ask - AI query endpoint")
        print("   • GET /static/graficos/{filename} - File serving")
        print("\n📋 Public endpoints:")
        print("   • GET /auth/ping - Health check")
        print("   • GET /auth/me - User info (requires auth)")
    else:
        print("⚠️  Some tests failed. Please check the output above.")

if __name__ == "__main__":
    main()