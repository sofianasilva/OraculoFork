#!/usr/bin/env python3
"""
Comprehensive integration test suite for Django-FastAPI JWT authentication flow.
Baby-step 5: Validates complete token flow between services.
"""
import requests
import json
import time
import sys
from typing import Optional, Dict, Any

# Service URLs
DJANGO_BASE_URL = "http://localhost:8001"
FASTAPI_BASE_URL = "http://localhost:8000"

class IntegrationTestSuite:
    """Integration test suite for Django-FastAPI authentication."""
    
    def __init__(self):
        self.token: Optional[str] = None
        self.user_info: Optional[Dict[str, Any]] = None
        self.tests_passed = 0
        self.total_tests = 0
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result with consistent formatting."""
        self.total_tests += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}")
            if details:
                print(f"   {details}")
        else:
            print(f"❌ {test_name}")
            if details:
                print(f"   {details}")
        return success
    
    def test_services_health(self) -> bool:
        """Test that both services are running and healthy."""
        print("🏥 Testing service health...")
        
        # Test Django service
        try:
            response = requests.get(f"{DJANGO_BASE_URL}/admin/", timeout=5)
            django_healthy = response.status_code in [200, 302]
        except Exception as e:
            django_healthy = False
        
        self.log_test("Django service health", django_healthy, 
                     f"Status: {'Healthy' if django_healthy else 'Unhealthy'}")
        
        # Test FastAPI service
        try:
            response = requests.get(f"{FASTAPI_BASE_URL}/auth/ping", timeout=5)
            fastapi_healthy = response.status_code == 200
        except Exception as e:
            fastapi_healthy = False
        
        self.log_test("FastAPI service health", fastapi_healthy,
                     f"Status: {'Healthy' if fastapi_healthy else 'Unhealthy'}")
        
        return django_healthy and fastapi_healthy
    
    def test_django_token_generation(self) -> bool:
        """Test Django JWT token generation via login."""
        print("\n🔑 Testing Django JWT token generation...")
        
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        try:
            response = requests.post(f"{DJANGO_BASE_URL}/api/auth/login/", 
                                   json=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('tokens', {}).get('access')
                self.user_info = data.get('user', {})
                
                success = bool(self.token)
                self.log_test("Django login and token generation", success,
                             f"Token length: {len(self.token) if self.token else 0} chars")
                return success
            else:
                self.log_test("Django login and token generation", False,
                             f"HTTP {response.status_code}: {response.text[:100]}")
                return False
                
        except Exception as e:
            self.log_test("Django login and token generation", False, f"Error: {str(e)}")
            return False
    
    def test_fastapi_auth_me(self) -> bool:
        """Test FastAPI /auth/me endpoint with Django JWT token."""
        print("\n🔐 Testing FastAPI JWT token validation...")
        
        if not self.token:
            self.log_test("FastAPI /auth/me endpoint", False, "No token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{FASTAPI_BASE_URL}/auth/me", 
                                  headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('user', {})
                
                # Validate response structure
                expected_fields = ['user_id', 'username']
                has_required_fields = all(field in user_data for field in expected_fields)
                
                self.log_test("FastAPI /auth/me endpoint", has_required_fields,
                             f"User: {user_data.get('username')} (ID: {user_data.get('user_id')})")
                return has_required_fields
            else:
                self.log_test("FastAPI /auth/me endpoint", False,
                             f"HTTP {response.status_code}: {response.text[:100]}")
                return False
                
        except Exception as e:
            self.log_test("FastAPI /auth/me endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_fastapi_protected_ask_endpoint(self) -> bool:
        """Test FastAPI protected /ask endpoint with Django JWT token."""
        print("\n🤖 Testing FastAPI protected /ask endpoint...")
        
        if not self.token:
            self.log_test("FastAPI /ask endpoint (protected)", False, "No token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            question_data = {
                "question": "How many repositories do we have in the system?"
            }
            
            response = requests.post(f"{FASTAPI_BASE_URL}/ask", 
                                   json=question_data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if user context was added (from Baby-step 4)
                has_user_context = isinstance(data, dict) and 'user_context' in data
                
                self.log_test("FastAPI /ask endpoint (protected)", True,
                             f"Response received, User context: {'Yes' if has_user_context else 'No'}")
                return True
            else:
                self.log_test("FastAPI /ask endpoint (protected)", False,
                             f"HTTP {response.status_code}: {response.text[:100]}")
                return False
                
        except Exception as e:
            self.log_test("FastAPI /ask endpoint (protected)", False, f"Error: {str(e)}")
            return False
    
    def test_token_rejection_without_auth(self) -> bool:
        """Test that protected endpoints properly reject requests without tokens."""
        print("\n🚫 Testing token rejection for unauthenticated requests...")
        
        # Test /auth/me without token
        try:
            response = requests.get(f"{FASTAPI_BASE_URL}/auth/me", timeout=5)
            auth_me_rejected = response.status_code in [401, 403]
        except Exception:
            auth_me_rejected = False
        
        self.log_test("Reject /auth/me without token", auth_me_rejected,
                     f"Status: {response.status_code if 'response' in locals() else 'Error'}")
        
        # Test /ask without token
        try:
            question_data = {"question": "Test question"}
            response = requests.post(f"{FASTAPI_BASE_URL}/ask", 
                                   json=question_data, timeout=5)
            ask_rejected = response.status_code in [401, 403]
        except Exception:
            ask_rejected = False
        
        self.log_test("Reject /ask without token", ask_rejected,
                     f"Status: {response.status_code if 'response' in locals() else 'Error'}")
        
        return auth_me_rejected and ask_rejected
    
    def test_invalid_token_rejection(self) -> bool:
        """Test that invalid tokens are properly rejected."""
        print("\n🔒 Testing invalid token rejection...")
        
        invalid_tokens = [
            "invalid-token-123",
            "Bearer invalid-token",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"
        ]
        
        all_rejected = True
        
        for i, invalid_token in enumerate(invalid_tokens, 1):
            try:
                headers = {"Authorization": f"Bearer {invalid_token}"}
                response = requests.get(f"{FASTAPI_BASE_URL}/auth/me", 
                                      headers=headers, timeout=5)
                rejected = response.status_code == 401
                
                self.log_test(f"Reject invalid token #{i}", rejected,
                             f"Status: {response.status_code}")
                
                if not rejected:
                    all_rejected = False
                    
            except Exception as e:
                self.log_test(f"Reject invalid token #{i}", False, f"Error: {str(e)}")
                all_rejected = False
        
        return all_rejected
    
    def test_token_expiration_handling(self) -> bool:
        """Test token expiration handling (informational test)."""
        print("\n⏰ Testing token expiration info...")
        
        if not self.token:
            self.log_test("Token expiration info", False, "No token available")
            return False
        
        try:
            # Decode token to check expiration (without verification for info only)
            import base64
            import json
            
            # Split token and decode payload
            parts = self.token.split('.')
            if len(parts) >= 2:
                # Add padding if needed
                payload = parts[1]
                payload += '=' * (4 - len(payload) % 4)
                
                decoded = base64.b64decode(payload)
                token_data = json.loads(decoded)
                
                exp_timestamp = token_data.get('exp', 0)
                current_time = time.time()
                time_until_expiry = exp_timestamp - current_time
                
                self.log_test("Token expiration info", True,
                             f"Expires in {int(time_until_expiry/60)} minutes")
                return True
            else:
                self.log_test("Token expiration info", False, "Invalid token format")
                return False
                
        except Exception as e:
            self.log_test("Token expiration info", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run complete integration test suite."""
        print("🚀 Starting Django-FastAPI JWT Integration Test Suite")
        print("=" * 60)
        
        # Test sequence
        tests = [
            self.test_services_health,
            self.test_django_token_generation,
            self.test_fastapi_auth_me,
            self.test_fastapi_protected_ask_endpoint,
            self.test_token_rejection_without_auth,
            self.test_invalid_token_rejection,
            self.test_token_expiration_handling,
        ]
        
        # Run all tests
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Integration Test Results: {self.tests_passed}/{self.total_tests} tests passed")
        
        success_rate = (self.tests_passed / self.total_tests * 100) if self.total_tests > 0 else 0
        
        if self.tests_passed == self.total_tests:
            print("🎉 All integration tests passed!")
            print("\n✅ Baby-step 5 validation successful")
            print("🔗 Django-FastAPI JWT authentication flow is fully operational")
            
            print("\n📋 Validated functionality:")
            print("   • Django JWT token generation")
            print("   • FastAPI JWT token validation")
            print("   • Protected endpoint access control")
            print("   • Invalid token rejection")
            print("   • Unauthenticated request rejection")
            
            return True
        else:
            print(f"⚠️  {self.total_tests - self.tests_passed} tests failed ({success_rate:.1f}% success rate)")
            print("Please check the output above for details.")
            return False


def main():
    """Main entry point for integration tests."""
    suite = IntegrationTestSuite()
    success = suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()