#!/usr/bin/env python3
"""
Test script for FastAPI JWT integration (Baby-step 1).
"""
import requests
import json

DJANGO_BASE_URL = "http://localhost:8001"
FASTAPI_BASE_URL = "http://localhost:8000"

def get_jwt_token():
    """Get a valid JWT token from Django auth service."""
    print("🔑 Getting JWT token from Django...")
    
    # Try to login with existing test user
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
        print(f"Response: {response.text}")
        return None

def test_fastapi_auth_ping():
    """Test the public /auth/ping endpoint."""
    print("\n🧪 Testing FastAPI /auth/ping (public)...")
    
    response = requests.get(f"{FASTAPI_BASE_URL}/auth/ping")
    
    if response.status_code == 200:
        print("✅ Auth ping successful")
        print(f"Response: {response.json()}")
        return True
    else:
        print(f"❌ Auth ping failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_fastapi_auth_me_without_token():
    """Test the protected /auth/me endpoint without token."""
    print("\n🧪 Testing FastAPI /auth/me without token...")
    
    response = requests.get(f"{FASTAPI_BASE_URL}/auth/me")
    
    if response.status_code == 403:
        print("✅ Correctly rejected request without token")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_fastapi_auth_me_with_token(token):
    """Test the protected /auth/me endpoint with valid token."""
    print("\n🧪 Testing FastAPI /auth/me with JWT token...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{FASTAPI_BASE_URL}/auth/me", headers=headers)
    
    if response.status_code == 200:
        print("✅ Successfully authenticated with JWT token")
        result = response.json()
        print(f"User info: {json.dumps(result, indent=2)}")
        return True
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_fastapi_auth_me_with_invalid_token():
    """Test the protected /auth/me endpoint with invalid token."""
    print("\n🧪 Testing FastAPI /auth/me with invalid token...")
    
    headers = {"Authorization": "Bearer invalid-token-12345"}
    response = requests.get(f"{FASTAPI_BASE_URL}/auth/me", headers=headers)
    
    if response.status_code == 401:
        print("✅ Correctly rejected invalid token")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def main():
    """Run all FastAPI JWT integration tests."""
    print("🚀 Starting FastAPI JWT Integration Tests (Baby-step 2)\n")
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Public endpoint
    if test_fastapi_auth_ping():
        tests_passed += 1
    
    # Test 2: Protected endpoint without token
    if test_fastapi_auth_me_without_token():
        tests_passed += 1
    
    # Test 3: Get JWT token and test protected endpoint
    token = get_jwt_token()
    if token and test_fastapi_auth_me_with_token(token):
        tests_passed += 1
    
    # Test 4: Protected endpoint with invalid token
    if test_fastapi_auth_me_with_invalid_token():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All FastAPI JWT integration tests passed!")
        print("\n✅ Baby-step 2 validation successful")
        print("Ready to proceed to Baby-step 3")
    else:
        print("⚠️  Some tests failed. Please check the output above.")

if __name__ == "__main__":
    main()