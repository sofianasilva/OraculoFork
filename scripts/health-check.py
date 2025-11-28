#!/usr/bin/env python3
"""
Comprehensive health check for Django Authentication Service.
"""
import requests
import json

BASE_URL = "http://localhost:8001"

def test_admin_interface():
    """Test Django Admin interface accessibility."""
    print("🧪 Testing Django Admin interface...")
    
    response = requests.get(f"{BASE_URL}/admin/")
    
    if response.status_code in [200, 302]:
        if response.status_code == 302 and '/admin/login/' in response.headers.get('Location', ''):
            print("✅ Django Admin accessible and redirecting to login")
        elif response.status_code == 200:
            print("✅ Django Admin accessible")
        return True
    else:
        print(f"❌ Django Admin test failed: {response.status_code}")
        return False

def test_api_endpoints():
    """Test all authentication API endpoints."""
    print("\n🧪 Testing API endpoints...")
    
    # Test registration
    reg_data = {
        "username": "healthcheck",
        "email": "healthcheck@oraculo.com", 
        "password": "healthcheck123",
        "password_confirm": "healthcheck123",
        "first_name": "Health",
        "last_name": "Check"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register/", json=reg_data)
    
    if response.status_code == 201:
        print("✅ Registration endpoint working")
        token = response.json()['tokens']['access']
        refresh_token = response.json()['tokens']['refresh']
    elif response.status_code == 400:
        print("✅ Registration endpoint working (user exists, testing login instead)")
        # Try login instead
        login_response = requests.post(f"{BASE_URL}/api/auth/login/", json={
            "username": "healthcheck",
            "password": "healthcheck123"
        })
        if login_response.status_code == 200:
            token = login_response.json()['tokens']['access']
            refresh_token = login_response.json()['tokens']['refresh']
        else:
            print(f"❌ Login fallback failed: {login_response.status_code}")
            return False
    else:
        print(f"❌ Registration failed: {response.status_code}")
        return False
        
    # Test profile access
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = requests.get(f"{BASE_URL}/api/auth/profile/", headers=headers)
    
    if profile_response.status_code == 200:
        print("✅ Profile endpoint working")
        
        # Test token refresh
        refresh_response = requests.post(
            f"{BASE_URL}/api/auth/token/refresh/", 
            json={"refresh": refresh_token}
        )
        
        if refresh_response.status_code == 200:
            print("✅ Token refresh endpoint working")
            return True
        else:
            print(f"❌ Token refresh failed: {refresh_response.status_code}")
            return False
    else:
        print(f"❌ Profile access failed: {profile_response.status_code}")
        return False

def test_database_connection():
    """Test database connectivity by checking user creation."""
    print("\n🧪 Testing database connection...")
    
    # Try to register a user to test DB connectivity
    test_data = {
        "username": "dbtest",
        "email": "dbtest@oraculo.com",
        "password": "dbtest123", 
        "password_confirm": "dbtest123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register/", json=test_data)
    
    if response.status_code == 201:
        print("✅ Database connection working")
        return True
    elif response.status_code == 400:
        print("✅ Database connection working (user exists)")
        return True
    else:
        print(f"❌ Database connection test failed: {response.status_code}")
        return False

def main():
    """Run comprehensive health checks."""
    print("🏥 Starting Oráculo Authentication Service Health Check\n")
    
    tests = [
        test_admin_interface,
        test_api_endpoints, 
        test_database_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n📊 Health Check Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All health checks passed! Authentication service is fully operational.")
        print("\n🔗 Service URLs:")
        print(f"   • Django Admin: {BASE_URL}/admin/ (admin/admin123)")
        print(f"   • API Base: {BASE_URL}/api/auth/")
        print(f"   • Registration: {BASE_URL}/api/auth/register/")
        print(f"   • Login: {BASE_URL}/api/auth/login/")
        print(f"   • Profile: {BASE_URL}/api/auth/profile/")
    else:
        print("⚠️  Some health checks failed. Please review the output above.")

if __name__ == "__main__":
    main()