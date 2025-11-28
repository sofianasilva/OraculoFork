#!/usr/bin/env python3
"""
Quick health check for Django-FastAPI integration.
Minimal version for rapid validation.
"""
import requests
import sys

def quick_check():
    """Perform quick health check of both services."""
    print("🏥 Quick Health Check - Django-FastAPI Integration")
    
    # Check Django
    try:
        response = requests.get("http://localhost:8001/api/auth/login/", timeout=3)
        django_ok = response.status_code in [200, 405]  # 405 = Method Not Allowed (GET on POST endpoint)
        print(f"Django Auth Service: {'✅ OK' if django_ok else '❌ FAIL'}")
    except Exception as e:
        django_ok = False
        print(f"Django Auth Service: ❌ FAIL ({str(e)[:50]})")
    
    # Check FastAPI
    try:
        response = requests.get("http://localhost:8000/auth/ping", timeout=3)
        fastapi_ok = response.status_code == 200
        print(f"FastAPI Service: {'✅ OK' if fastapi_ok else '❌ FAIL'}")
    except Exception as e:
        fastapi_ok = False
        print(f"FastAPI Service: ❌ FAIL ({str(e)[:50]})")
    
    # Quick token test
    if django_ok and fastapi_ok:
        try:
            # Get token
            login_response = requests.post("http://localhost:8001/api/auth/login/", 
                                         json={"username": "testuser", "password": "testpass123"}, 
                                         timeout=5)
            if login_response.status_code == 200:
                token = login_response.json()['tokens']['access']
                
                # Test token
                auth_response = requests.get("http://localhost:8000/auth/me", 
                                           headers={"Authorization": f"Bearer {token}"}, 
                                           timeout=5)
                token_ok = auth_response.status_code == 200
                print(f"JWT Token Flow: {'✅ OK' if token_ok else '❌ FAIL'}")
            else:
                token_ok = False
                print("JWT Token Flow: ❌ FAIL (login failed)")
        except Exception as e:
            token_ok = False
            print(f"JWT Token Flow: ❌ FAIL ({str(e)[:50]})")
    else:
        token_ok = False
        print("JWT Token Flow: ⏭️  SKIPPED (services not ready)")
    
    all_ok = django_ok and fastapi_ok and token_ok
    print(f"\nOverall Status: {'🎉 ALL SYSTEMS GO' if all_ok else '⚠️  ISSUES DETECTED'}")
    
    return all_ok

if __name__ == "__main__":
    success = quick_check()
    sys.exit(0 if success else 1)