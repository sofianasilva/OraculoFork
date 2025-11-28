#!/usr/bin/env python3
"""
Simple test script for Django Authentication Service endpoints.
Run this after starting the services with docker-compose up.
"""
import requests
import json

BASE_URL = "http://localhost:8001/api/auth"

def test_registration():
    """Test user registration endpoint."""
    print("🧪 Testing user registration...")
    
    data = {
        "username": "testuser",
        "email": "test@oraculo.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    
    if response.status_code == 201:
        print("✅ Registration successful!")
        result = response.json()
        print(f"   User: {result['user']['username']}")
        print(f"   Token: {result['tokens']['access'][:50]}...")
        return result['tokens']['access']
    else:
        print(f"❌ Registration failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_login():
    """Test user login endpoint."""
    print("\n🧪 Testing user login...")
    
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=data)
    
    if response.status_code == 200:
        print("✅ Login successful!")
        result = response.json()
        print(f"   User: {result['user']['username']}")
        return result['tokens']['access']
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_profile(token):
    """Test profile endpoint with authentication."""
    print("\n🧪 Testing authenticated profile access...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    
    if response.status_code == 200:
        print("✅ Profile access successful!")
        result = response.json()
        print(f"   Username: {result['username']}")
        print(f"   Email: {result['email']}")
    else:
        print(f"❌ Profile access failed: {response.status_code}")
        print(f"   Error: {response.text}")

def main():
    """Run all authentication tests."""
    print("🚀 Starting Oráculo Authentication Service Tests\n")
    
    # Test registration
    token = test_registration()
    
    if not token:
        # If registration fails (user might exist), try login
        token = test_login()
    
    if token:
        # Test authenticated endpoint
        test_profile(token)
        print("\n✅ All tests completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Visit http://localhost:8001/admin/ (admin/admin123)")
        print("   2. Check FastAPI integration in Step 4")
        print("   3. Implement ACL in Step 5")
    else:
        print("\n❌ Authentication tests failed!")

if __name__ == "__main__":
    main()