#!/usr/bin/env python3
"""
Comprehensive health check for Django-FastAPI integration.
Combines Django health check with FastAPI JWT integration validation.
"""
import requests
import json
import sys

DJANGO_BASE_URL = "http://localhost:8001"
FASTAPI_BASE_URL = "http://localhost:8000"

def test_django_health():
    """Test Django service health."""
    print("🧪 Testing Django Authentication Service...")
    
    try:
        # Test admin interface
        response = requests.get(f"{DJANGO_BASE_URL}/admin/", timeout=5)
        admin_ok = response.status_code in [200, 302]
        
        # Test auth endpoints
        response = requests.get(f"{DJANGO_BASE_URL}/api/auth/register/", timeout=5)
        auth_endpoints_ok = response.status_code in [200, 405]  # 405 = Method Not Allowed for GET
        
        django_healthy = admin_ok and auth_endpoints_ok
        print(f"✅ Django service: {'Healthy' if django_healthy else 'Unhealthy'}")
        return django_healthy
        
    except Exception as e:
        print(f"❌ Django service: Error - {str(e)}")
        return False

def test_fastapi_health():
    """Test FastAPI service health."""
    print("🧪 Testing FastAPI Service...")
    
    try:
        # Test ping endpoint
        response = requests.get(f"{FASTAPI_BASE_URL}/auth/ping", timeout=5)
        ping_ok = response.status_code == 200
        
        # Test that protected endpoints exist (should return 401/403 without auth)
        response = requests.get(f"{FASTAPI_BASE_URL}/auth/me", timeout=5)
        protected_ok = response.status_code in [401, 403]
        
        fastapi_healthy = ping_ok and protected_ok
        print(f"✅ FastAPI service: {'Healthy' if fastapi_healthy else 'Unhealthy'}")
        return fastapi_healthy
        
    except Exception as e:
        print(f"❌ FastAPI service: Error - {str(e)}")
        return False

def test_jwt_integration():
    """Test JWT token flow between services."""
    print("🧪 Testing JWT Integration...")
    
    try:
        # Step 1: Get token from Django
        login_data = {"username": "testuser", "password": "testpass123"}
        response = requests.post(f"{DJANGO_BASE_URL}/api/auth/login/", 
                               json=login_data, timeout=10)
        
        if response.status_code != 200:
            print("❌ JWT Integration: Failed to get token from Django")
            return False
        
        token = response.json()['tokens']['access']
        
        # Step 2: Use token with FastAPI
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{FASTAPI_BASE_URL}/auth/me", 
                              headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ JWT Integration: Working (User: {user_data.get('user', {}).get('username', 'Unknown')})")
            return True
        else:
            print(f"❌ JWT Integration: FastAPI rejected token (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ JWT Integration: Error - {str(e)}")
        return False

def test_protected_endpoints():
    """Test that protected endpoints work with authentication."""
    print("🧪 Testing Protected Endpoints...")
    
    try:
        # Get token
        login_data = {"username": "testuser", "password": "testpass123"}
        response = requests.post(f"{DJANGO_BASE_URL}/api/auth/login/", 
                               json=login_data, timeout=10)
        
        if response.status_code != 200:
            print("❌ Protected Endpoints: Cannot get authentication token")
            return False
        
        token = response.json()['tokens']['access']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test /ask endpoint (should work with auth)
        question_data = {"question": "Test question for health check"}
        response = requests.post(f"{FASTAPI_BASE_URL}/ask", 
                               json=question_data, headers=headers, timeout=15)
        
        ask_works = response.status_code == 200
        
        # Test without auth (should fail)
        response = requests.post(f"{FASTAPI_BASE_URL}/ask", 
                               json=question_data, timeout=5)
        
        ask_protected = response.status_code in [401, 403]
        
        endpoints_ok = ask_works and ask_protected
        print(f"✅ Protected Endpoints: {'Working' if endpoints_ok else 'Issues detected'}")
        return endpoints_ok
        
    except Exception as e:
        print(f"❌ Protected Endpoints: Error - {str(e)}")
        return False

def main():
    """Run comprehensive integration health check."""
    print("🏥 Django-FastAPI Integration Health Check")
    print("=" * 50)
    
    tests = [
        ("Django Service", test_django_health),
        ("FastAPI Service", test_fastapi_health),
        ("JWT Integration", test_jwt_integration),
        ("Protected Endpoints", test_protected_endpoints),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}: Unexpected error - {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Health Check Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All systems healthy!")
        print("✅ Django-FastAPI JWT authentication is fully operational")
        
        print("\n🔗 Service URLs:")
        print(f"   • Django Admin: {DJANGO_BASE_URL}/admin/")
        print(f"   • Django API: {DJANGO_BASE_URL}/api/auth/")
        print(f"   • FastAPI Docs: {FASTAPI_BASE_URL}/docs")
        print(f"   • FastAPI Auth: {FASTAPI_BASE_URL}/auth/")
        
        return True
    else:
        print(f"⚠️  {total - passed} health check(s) failed")
        print("Please review the services and fix any issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)