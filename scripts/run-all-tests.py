#!/usr/bin/env python3
"""
Test runner for all authentication integration tests.
Runs tests in sequence with proper error handling.
"""
import subprocess
import sys
import time

def run_test_script(script_name: str, description: str) -> bool:
    """Run a test script and return success status."""
    print(f"\n{'='*60}")
    print(f"🧪 Running {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True, 
                              timeout=60)
        
        success = result.returncode == 0
        print(f"\n{'✅ PASSED' if success else '❌ FAILED'}: {description}")
        return success
        
    except subprocess.TimeoutExpired:
        print(f"\n⏰ TIMEOUT: {description} took too long")
        return False
    except Exception as e:
        print(f"\n💥 ERROR: {description} failed with exception: {str(e)}")
        return False

def main():
    """Run all test suites in sequence."""
    print("🚀 Django-FastAPI Authentication Test Suite Runner")
    print("Running all integration tests in sequence...")
    
    tests = [
        ("scripts/quick-health-check.py", "Quick Health Check"),
        ("scripts/health-check.py", "Django Service Health Check"),
        ("scripts/test-fastapi-jwt.py", "FastAPI JWT Basic Tests"),
        ("scripts/test-protected-endpoints.py", "Protected Endpoints Tests"),
        ("scripts/test-integration-auth-fastapi.py", "Full Integration Test Suite"),
    ]
    
    passed = 0
    total = len(tests)
    
    start_time = time.time()
    
    for script, description in tests:
        if run_test_script(script, description):
            passed += 1
        
        # Small delay between tests
        time.sleep(1)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"📊 FINAL TEST RESULTS")
    print(f"{'='*60}")
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    print(f"Total Duration: {duration:.1f} seconds")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Django-FastAPI JWT authentication integration is fully operational")
        print("\n🔗 Ready for production use with the following features:")
        print("   • JWT token generation (Django)")
        print("   • JWT token validation (FastAPI)")
        print("   • Protected endpoint access control")
        print("   • Comprehensive error handling")
        print("   • Audit logging and user tracking")
        
        return True
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED")
        print("Please review the output above and fix any issues before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)