import requests
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json
import os

# PROFILES STORAGE FILE  
PROFILES_FILE = "profiles_pool_v2.json"
REQUIRED_READY_PROFILES = 10

# GLOBAL COUNTRY CODES - SUPPORT ALL COUNTRIES
COUNTRY_CODES = {
    # North America
    "US": "United States", "CA": "Canada", "MX": "Mexico",
    
    # Europe  
    "UK": "United Kingdom", "DE": "Germany", "FR": "France", "IT": "Italy", 
    "ES": "Spain", "NL": "Netherlands", "SE": "Sweden", "NO": "Norway", 
    "DK": "Denmark", "FI": "Finland", "PL": "Poland", "CZ": "Czech Republic",
    "AT": "Austria", "CH": "Switzerland", "BE": "Belgium", "IE": "Ireland",
    "PT": "Portugal", "GR": "Greece", "HU": "Hungary", "RO": "Romania",
    "BG": "Bulgaria", "HR": "Croatia", "SI": "Slovenia", "SK": "Slovakia",
    "LT": "Lithuania", "LV": "Latvia", "EE": "Estonia", "LU": "Luxembourg",
    "MT": "Malta", "CY": "Cyprus", "IS": "Iceland", "RS": "Serbia",
    "BA": "Bosnia and Herzegovina", "MK": "North Macedonia", "AL": "Albania",
    "ME": "Montenegro", "MD": "Moldova", "UA": "Ukraine", "BY": "Belarus",
    "RU": "Russia", "TR": "Turkey",
    
    # Asia Pacific
    "AU": "Australia", "NZ": "New Zealand", "JP": "Japan", "KR": "South Korea",
    "CN": "China", "HK": "Hong Kong", "TW": "Taiwan", "SG": "Singapore",
    "MY": "Malaysia", "TH": "Thailand", "VN": "Vietnam", "ID": "Indonesia",
    "PH": "Philippines", "IN": "India", "PK": "Pakistan", "BD": "Bangladesh",
    "LK": "Sri Lanka", "MM": "Myanmar", "KH": "Cambodia", "LA": "Laos",
    "MN": "Mongolia", "KZ": "Kazakhstan", "UZ": "Uzbekistan", "KG": "Kyrgyzstan",
    "TJ": "Tajikistan", "TM": "Turkmenistan", "AF": "Afghanistan", "IR": "Iran",
    "IQ": "Iraq", "SY": "Syria", "LB": "Lebanon", "JO": "Jordan", "IL": "Israel",
    "PS": "Palestine", "SA": "Saudi Arabia", "AE": "UAE", "QA": "Qatar",
    "KW": "Kuwait", "BH": "Bahrain", "OM": "Oman", "YE": "Yemen",
    
    # Africa
    "ZA": "South Africa", "EG": "Egypt", "MA": "Morocco", "TN": "Tunisia",
    "DZ": "Algeria", "LY": "Libya", "SD": "Sudan", "ET": "Ethiopia",
    "KE": "Kenya", "UG": "Uganda", "TZ": "Tanzania", "RW": "Rwanda",
    "BI": "Burundi", "SO": "Somalia", "DJ": "Djibouti", "ER": "Eritrea",
    "SS": "South Sudan", "CF": "Central African Republic", "TD": "Chad",
    "CM": "Cameroon", "NG": "Nigeria", "NE": "Niger", "BF": "Burkina Faso",
    "ML": "Mali", "SN": "Senegal", "GM": "Gambia", "GW": "Guinea-Bissau",
    "GN": "Guinea", "SL": "Sierra Leone", "LR": "Liberia", "CI": "Côte d'Ivoire",
    "GH": "Ghana", "TG": "Togo", "BJ": "Benin", "GA": "Gabon", "GQ": "Equatorial Guinea",
    "ST": "São Tomé and Príncipe", "AO": "Angola", "ZM": "Zambia", "ZW": "Zimbabwe",
    "BW": "Botswana", "NA": "Namibia", "SZ": "Eswatini", "LS": "Lesotho",
    "MW": "Malawi", "MZ": "Mozambique", "MG": "Madagascar", "MU": "Mauritius",
    "SC": "Seychelles", "KM": "Comoros",
    
    # South America
    "BR": "Brazil", "AR": "Argentina", "CL": "Chile", "PE": "Peru",
    "CO": "Colombia", "VE": "Venezuela", "EC": "Ecuador", "BO": "Bolivia",
    "PY": "Paraguay", "UY": "Uruguay", "GY": "Guyana", "SR": "Suriname",
    "GF": "French Guiana",
    
    # Central America & Caribbean
    "GT": "Guatemala", "BZ": "Belize", "SV": "El Salvador", "HN": "Honduras",
    "NI": "Nicaragua", "CR": "Costa Rica", "PA": "Panama", "CU": "Cuba",
    "JM": "Jamaica", "HT": "Haiti", "DO": "Dominican Republic", "PR": "Puerto Rico",
    "TT": "Trinidad and Tobago", "BB": "Barbados", "LC": "Saint Lucia",
    "GD": "Grenada", "VC": "Saint Vincent and the Grenadines", "AG": "Antigua and Barbuda",
    "DM": "Dominica", "KN": "Saint Kitts and Nevis", "BS": "Bahamas",
    
    # Oceania
    "FJ": "Fiji", "PG": "Papua New Guinea", "SB": "Solomon Islands",
    "VU": "Vanuatu", "NC": "New Caledonia", "PF": "French Polynesia",
    "TO": "Tonga", "WS": "Samoa", "KI": "Kiribati", "TV": "Tuvalu",
    "NR": "Nauru", "PW": "Palau", "FM": "Micronesia", "MH": "Marshall Islands"
}

def generate_random_name():
    return ''.join(random.choices(string.ascii_letters, k=6))

def load_profile_pool():
    """Load profile pool from JSON file"""
    try:
        if os.path.exists(PROFILES_FILE):
            with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
                pool = json.load(f)
                ready_count = len([p for p in pool if p.get('status') == 'ready'])
                completed_count = len([p for p in pool if p.get('status') == 'completed'])
                in_use_count = len([p for p in pool if p.get('status') == 'in_use'])
                print(f"📂 LOADED PROFILE POOL: {ready_count} Ready + {in_use_count} In Use + {completed_count} Completed")
                return pool
        else:
            print(f"📂 NO PROFILE POOL FOUND - WILL CREATE NEW")
            return []
    except Exception as e:
        print(f"❌ ERROR LOADING PROFILE POOL: {e}")
        return []

def save_profile_pool(pool):
    """Save profile pool to JSON file"""
    try:
        with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(pool, f, indent=2, ensure_ascii=False)
        ready_count = len([p for p in pool if p.get('status') == 'ready'])
        completed_count = len([p for p in pool if p.get('status') == 'completed'])
        in_use_count = len([p for p in pool if p.get('status') == 'in_use'])
        print(f"💾 SAVED PROFILE POOL: {ready_count} Ready + {in_use_count} In Use + {completed_count} Completed")
    except Exception as e:
        print(f"❌ ERROR SAVING PROFILE POOL: {e}")

def create_blank_profile():
    """Create a blank profile (no proxy, not started)"""
    api_token = "02cd9463949f4b6e94204c3dacdb0e01"
    url = "https://app.octobrowser.net/api/v2/automation/profiles"
    headers = {"X-Octo-Api-Token": api_token, "Content-Type": "application/json"}
    
    profile_id = f"POOL_{random.randint(10000,99999)}"
    print(f"🚀 CREATING BLANK PROFILE [{profile_id}]...")
    
    data = {
        "title": f"POOL_PROFILE_{profile_id}_{int(time.time())}",
        "fingerprint": {"os": "win"}
        # NO PROXY - will be set later based on country
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        time.sleep(2)  # Delay for stability
        
        if response.status_code == 201:
            result = response.json()
            profile_uuid = result.get('data', {}).get('uuid')
            print(f"✅ CREATED BLANK PROFILE [{profile_id}]")
            
            # Create profile data (not started yet)
            profile_data = {
                "uuid": profile_uuid,
                "profile_id": profile_id,
                "title": data["title"],
                "status": "ready",
                "created_time": int(time.time()),
                "country": None,
                "proxy": None,
                "debug_port": None,  # Will be set when started
                "started": False
            }
            
            return profile_data
        else:
            print(f"❌ FAILED TO CREATE BLANK PROFILE: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ ERROR CREATING BLANK PROFILE: {e}")
        return None

def initialize_profile_pool():
    """Initialize and maintain 10 blank profiles"""
    print(f"🔧 INITIALIZING PROFILE POOL...")
    print("=" * 60)
    
    pool = load_profile_pool()
    ready_profiles = [p for p in pool if p.get('status') == 'ready']
    
    print(f"📊 CURRENT STATUS: {len(ready_profiles)} ready profiles")
    
    # Create missing ready profiles
    needed = REQUIRED_READY_PROFILES - len(ready_profiles)
    if needed > 0:
        print(f"🏗️ CREATING {needed} NEW BLANK PROFILES...")
        
        for i in range(needed):
            print(f"   Creating profile {i+1}/{needed}...")
            new_profile = create_blank_profile()
            if new_profile:
                pool.append(new_profile)
                time.sleep(1)  # Delay between creations
            else:
                print(f"⚠️ Failed to create profile {i+1}")
        
        save_profile_pool(pool)
    else:
        print(f"✅ POOL IS COMPLETE - {len(ready_profiles)} ready profiles available")
    
    return pool

def set_proxy_and_start_profile(profile, country):
    """Set proxy for country and start the profile"""
    profile_uuid = profile['uuid']
    profile_id = profile['profile_id']
    
    print(f"🔄 SETTING {country} PROXY FOR [{profile_id}]...")
    
    # Generate proxy config for country
    api_token = "02cd9463949f4b6e94204c3dacdb0e01"
    session_id = f"{country}{random.randint(100,999)}-{generate_random_name()}"
    
    proxy_config = {
        "type": "socks5",
        "host": "pr.oxylabs.io", 
        "port": 7777,
        "login": f"customer-xmedia_JQ2i2-cc-{country.lower()}-sessid-{session_id}-sesstime-30",
        "password": "Oxy2024=huat"
    }
    
    # Update profile with proxy
    url = f"https://app.octobrowser.net/api/v2/automation/profiles/{profile_uuid}"
    headers = {"X-Octo-Api-Token": api_token, "Content-Type": "application/json"}
    data = {"proxy": proxy_config}
    
    try:
        response = requests.patch(url, headers=headers, json=data, timeout=10)
        time.sleep(2)
        
        if response.status_code == 200:
            print(f"✅ PROXY SET FOR [{profile_id}] -> {country} ({session_id})")
            
            # Now start the profile
            print(f"⚡ STARTING [{profile_id}] WITH {country} PROXY...")
            start_data = {'uuid': profile_uuid, 'headless': False, 'debug_port': True}
            start_response = requests.post("http://localhost:58888/api/profiles/start", 
                                         json=start_data, timeout=10)
            time.sleep(3)
            
            if start_response.status_code == 200:
                start_result = start_response.json()
                debug_port = start_result.get('debug_port')
                print(f"✅ STARTED [{profile_id}] PORT: {debug_port}")
                
                # Update profile data
                profile['status'] = 'in_use'
                profile['country'] = country
                profile['proxy'] = proxy_config
                profile['debug_port'] = debug_port
                profile['started'] = True
                profile['use_time'] = int(time.time())
                
                return debug_port, proxy_config
            else:
                print(f"❌ FAILED TO START [{profile_id}]: {start_response.status_code}")
                return None, None
        else:
            print(f"❌ PROXY UPDATE FAILED [{profile_id}]: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ ERROR SETTING PROXY/STARTING [{profile_id}]: {e}")
        return None, None

def get_profile_for_country(country):
    """Get a ready profile, set proxy, and start it for specific country"""
    pool = load_profile_pool()
    ready_profiles = [p for p in pool if p.get('status') == 'ready']
    
    if not ready_profiles:
        print(f"❌ NO READY PROFILES AVAILABLE! Need to create more.")
        return None, None, None, None
    
    # Take the first ready profile
    selected_profile = ready_profiles[0]
    profile_id = selected_profile['profile_id']
    
    print(f"📱 USING PROFILE [{profile_id}] FOR {country}")
    
    # Set proxy and start profile
    debug_port, proxy_config = set_proxy_and_start_profile(selected_profile, country)
    
    if debug_port:
        # Save updated pool
        save_profile_pool(pool)
        
        return selected_profile['uuid'], debug_port, proxy_config, profile_id
    else:
        print(f"❌ FAILED TO PREPARE PROFILE [{profile_id}] FOR {country}")
        return None, None, None, None

def mark_profile_completed(profile_uuid, success=True):
    """Mark profile as completed and create new blank profile"""
    pool = load_profile_pool()
    
    for profile in pool:
        if profile['uuid'] == profile_uuid:
            if success:
                profile['status'] = 'completed'
                profile['completed_time'] = int(time.time())
                
                # Rename profile title to Mission Completed
                api_token = "02cd9463949f4b6e94204c3dacdb0e01"
                url = f"https://app.octobrowser.net/api/v2/automation/profiles/{profile_uuid}"
                headers = {"X-Octo-Api-Token": api_token, "Content-Type": "application/json"}
                
                new_title = f"MISSION_COMPLETED_{profile['profile_id']}_{int(time.time())}"
                data = {"title": new_title}
                
                try:
                    response = requests.patch(url, headers=headers, json=data, timeout=10)
                    if response.status_code == 200:
                        profile['title'] = new_title
                        print(f"✅ MARKED AS COMPLETED: {profile['profile_id']}")
                    else:
                        print(f"⚠️ Failed to rename profile: {response.status_code}")
                except Exception as e:
                    print(f"⚠️ Error renaming profile: {e}")
            else:
                # If failed, mark as ready again
                profile['status'] = 'ready'
                profile['country'] = None
                profile['proxy'] = None
                profile['debug_port'] = None
                profile['started'] = False
                print(f"♻️ MARKED AS READY AGAIN: {profile['profile_id']}")
            
            break
    
    save_profile_pool(pool)
    
    # Create a new blank profile to maintain pool
    if success:
        print(f"🏗️ CREATING NEW BLANK PROFILE TO MAINTAIN POOL...")
        new_profile = create_blank_profile()
        if new_profile:
            pool.append(new_profile)
            save_profile_pool(pool)
            print(f"✅ POOL MAINTAINED: New blank profile created!")
        else:
            print(f"⚠️ Failed to create new profile for pool")

def display_country_options():
    """Display available countries in organized format"""
    print("\n🌍 AVAILABLE COUNTRIES:")
    print("=" * 80)
    
    regions = {
        "🇺🇸 NORTH AMERICA": ["US", "CA", "MX"],
        "🇪🇺 EUROPE": ["UK", "DE", "FR", "IT", "ES", "NL", "SE", "NO", "DK", "FI", "PL", "CZ", "AT", "CH", "BE", "IE", "PT"],
        "🇦🇺 ASIA PACIFIC": ["AU", "NZ", "JP", "KR", "CN", "HK", "TW", "SG", "MY", "TH", "VN", "ID", "PH", "IN"],
        "🌍 AFRICA": ["ZA", "EG", "MA", "TN", "NG", "KE", "ET", "GH"],
        "🌎 SOUTH AMERICA": ["BR", "AR", "CL", "PE", "CO", "VE", "EC"],
        "🏝️ CARIBBEAN": ["CU", "JM", "HT", "DO", "TT", "BB"]
    }
    
    for region, countries in regions.items():
        print(f"\n{region}:")
        line = "  "
        for country in countries:
            country_name = COUNTRY_CODES.get(country, country)
            line += f"{country}({country_name[:12]}) "
            if len(line) > 70:
                print(line)
                line = "  "
        if line.strip():
            print(line)
    
    print(f"\n💡 Type country code (e.g., 'US', 'FR', 'JP') or 'list' to see all {len(COUNTRY_CODES)} countries")
    print("=" * 80)

def explore_2fa_options(driver, profile_id):
    """SMART 2FA detection and complete workflow handling"""
    print(f"🔍 SMART 2FA DETECTION [{profile_id}]")
    print("=" * 60)
    
    try:
        current_url = driver.current_url
        page_source = driver.page_source
        
        # Enhanced 2FA page verification
        page_lower = page_source.lower()
        
        # Strong indicators of 2FA page
        strong_2fa_indicators = [
            "2-step verification", "choose how you want to sign in", 
            "verification code", "authenticator", "security key",
            "backup code", "phone prompt", "tap yes"
        ]
        
        # URL indicators
        url_2fa_indicators = ["challenge", "verification", "2fa", "signin/v2", "totp", "challenge/totp"]
        
        # Must NOT be password page  
        password_page_indicators = ["enter your password", "password field"]
        
        is_2fa_page = False
        is_password_page = any(x in page_lower for x in password_page_indicators)
        
        # Special case for TOTP pages
        if "totp" in current_url or "challenge/totp" in current_url:
            is_2fa_page = True
            print(f"🔐 TOTP/Google Authenticator page detected!")
        elif not is_password_page:
            if any(x in current_url for x in url_2fa_indicators):
                is_2fa_page = True
            elif any(x in page_lower for x in strong_2fa_indicators):
                is_2fa_page = True
        
        if not is_2fa_page:
            print(f"❌ NOT ON 2FA PAGE [{profile_id}] - Still on password or other page")
            print(f"📄 Current URL: {current_url[:60]}...")
            return False
        
        print(f"✅ CONFIRMED 2FA PAGE [{profile_id}]")
        print(f"📄 URL: {current_url[:60]}...")
        
        # SMART DETECTION: Look for our 2 preferred options FIRST
        print(f"\n🎯 SMART DETECTION: Looking for preferred 2FA options...")
        print("=" * 60)
        
        # Find all elements and scan for our preferred options
        all_elements = driver.find_elements(By.CSS_SELECTOR, "div, span, button, a")
        
        phone_option = None
        authenticator_option = None
        
        for elem in all_elements:
            if elem.is_displayed():
                elem_text = elem.text.strip()
                if elem_text and len(elem_text) > 15 and len(elem_text) < 200:
                    elem_lower = elem_text.lower()
                    
                    # Check for Phone Tap Yes (highest priority)
                    if "tap yes" in elem_lower and "recovery email" in elem_lower and not phone_option:
                        phone_option = {
                            "element": elem,
                            "text": elem_text,
                            "type": "phone_tap_yes"
                        }
                        print(f"📱 FOUND PHONE TAP YES: {elem_text[:50]}...")
                        
                    # Check for Google Authenticator (second priority)  
                    elif "verification code" in elem_lower and "google authenticator" in elem_lower and not authenticator_option:
                        authenticator_option = {
                            "element": elem,
                            "text": elem_text,
                            "type": "google_authenticator"
                        }
                        print(f"🔐 FOUND GOOGLE AUTHENTICATOR: {elem_text[:50]}...")
        
        # Decision logic
        selected_option = None
        
        if phone_option:
            print(f"✅ SELECTING PHONE TAP YES (highest priority)")
            selected_option = phone_option
        elif authenticator_option:
            print(f"✅ SELECTING GOOGLE AUTHENTICATOR (second priority)")
            selected_option = authenticator_option
        else:
            print(f"⚠️ Neither preferred option found directly")
            print(f"🔍 Will try 'Try another way' to find them...")
            
            # Try "Try another way" to reveal more options
            try_another_found = False
            try_selectors = [
                "//button[contains(text(), 'Try another way')]",
                "//a[contains(text(), 'Try another way')]",
                "//div[contains(text(), 'Try another way')]",
                "//span[contains(text(), 'Try another way')]/parent::button",
                "*[role='button'][contains(text(), 'Try another way')]",
                # Multilingual
                "//button[contains(text(), 'Essayer une autre méthode')]",
                "//button[contains(text(), 'Andere Methode versuchen')]",
                "//button[contains(text(), 'Probar otra forma')]",
                "//button[contains(text(), 'Tentar de outra forma')]",
                "//button[contains(text(), 'Prova un altro modo')]",
                "//button[contains(text(), 'Thử cách khác')]"
            ]
            
            for selector in try_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            element_text = element.text.strip()
                            print(f"✅ FOUND: '{element_text}'")
                            
                            # Scroll and click
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].click();", element)
                            print(f"👆 CLICKED 'TRY ANOTHER WAY' [{profile_id}]")
                            try_another_found = True
                            time.sleep(3)
                            break
                    if try_another_found:
                        break
                except Exception as e:
                    continue
            
            if try_another_found:
                # Re-scan for our preferred options after clicking
                print(f"🔍 RE-SCANNING after 'Try another way'...")
                time.sleep(2)
                
                all_elements = driver.find_elements(By.CSS_SELECTOR, "div, span, button, a")
                
                for elem in all_elements:
                    if elem.is_displayed():
                        elem_text = elem.text.strip()
                        if elem_text and len(elem_text) > 15 and len(elem_text) < 200:
                            elem_lower = elem_text.lower()
                            
                            if "tap yes" in elem_lower and "recovery email" in elem_lower and not phone_option:
                                phone_option = {
                                    "element": elem,
                                    "text": elem_text,
                                    "type": "phone_tap_yes"
                                }
                                print(f"📱 NOW FOUND PHONE TAP YES: {elem_text[:50]}...")
                                
                            elif "verification code" in elem_lower and "google authenticator" in elem_lower and not authenticator_option:
                                authenticator_option = {
                                    "element": elem,
                                    "text": elem_text,
                                    "type": "google_authenticator"
                                }
                                print(f"🔐 NOW FOUND GOOGLE AUTHENTICATOR: {elem_text[:50]}...")
                
                # Re-select after try another way
                if phone_option:
                    print(f"✅ SELECTING PHONE TAP YES (found after try another way)")
                    selected_option = phone_option
                elif authenticator_option:
                    print(f"✅ SELECTING GOOGLE AUTHENTICATOR (found after try another way)")
                    selected_option = authenticator_option
        
        print("=" * 60)
        
        # Execute the selected option workflow
        if selected_option:
            option_type = selected_option["type"]
            target_element = selected_option["element"]
            
            print(f"🚀 EXECUTING {option_type.upper()} WORKFLOW...")
            
            # Click the selected option
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", target_element)
                time.sleep(1)
                target_element.click()
                print(f"👆 CLICKED {option_type.upper()}!")
                time.sleep(3)
            except:
                try:
                    driver.execute_script("arguments[0].click();", target_element)
                    print(f"👆 CLICKED {option_type.upper()} with JS!")
                    time.sleep(3)
                except Exception as e:
                    print(f"❌ Click failed: {e}")
                    return False
            
            # Handle workflow based on type
            if option_type == "phone_tap_yes":
                return handle_phone_verification_workflow(driver, profile_id)
            elif option_type == "google_authenticator":
                return handle_google_authenticator_workflow(driver, profile_id)
        
        else:
            print(f"❌ Neither Phone Tap Yes nor Google Authenticator found")
            print(f"💡 Manual 2FA selection required")
            return False
        
        print("=" * 60)
        return True
            
    except Exception as e:
        print(f"❌ 2FA ANALYSIS ERROR [{profile_id}]: {e}")
        return False

def handle_phone_verification_workflow(driver, profile_id):
    """Complete phone verification workflow"""
    print(f"📱 PHONE VERIFICATION WORKFLOW [{profile_id}]")
    print("=" * 50)
    
    try:
        # Wait for presend page
        time.sleep(2)
        current_url = driver.current_url
        
        if "presend" in current_url:
            print(f"✅ Reached phone verification choice page!")
            print(f"📱 Auto-clicking 'Yes' to get verification code...")
            
            # Find and click Yes button
            yes_selectors = [
                "//button[contains(text(), 'Yes')]",
                "//a[contains(text(), 'Yes')]",
                "button[type='submit']",
                "button"
            ]
            
            yes_clicked = False
            for selector in yes_selectors:
                try:
                    if selector.startswith("//"):
                        elements = driver.find_elements(By.XPATH, selector)
                    else:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for elem in elements:
                        if elem.is_displayed():
                            elem_text = elem.text.strip().lower()
                            if elem_text == "yes" or "yes" in elem_text:
                                try:
                                    elem.click()
                                    print(f"✅ CLICKED 'YES' BUTTON!")
                                    yes_clicked = True
                                    time.sleep(3)
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();", elem)
                                        print(f"✅ CLICKED 'YES' BUTTON with JS!")
                                        yes_clicked = True
                                        time.sleep(3)
                                        break
                                    except:
                                        continue
                    if yes_clicked:
                        break
                except:
                    continue
            
            if yes_clicked:
                # Extract verification code
                verification_code = extract_verification_code(driver, profile_id)
                if verification_code:
                    print(f"🎉 PHONE VERIFICATION SUCCESS!")
                    print(f"📱 CODE: {verification_code}")
                    print(f"💡 Enter this code on your phone to complete login")
                    return True
                else:
                    print(f"⚠️ Code extraction failed")
                    return False
            else:
                print(f"⚠️ Could not click 'Yes' button")
                return False
        else:
            print(f"⚠️ Not on expected presend page: {current_url}")
            return False
            
    except Exception as e:
        print(f"❌ Phone verification error: {e}")
        return False

def handle_google_authenticator_workflow(driver, profile_id):
    """Complete Google Authenticator workflow with user input and success/error detection"""
    print(f"🔐 GOOGLE AUTHENTICATOR WORKFLOW [{profile_id}]")
    print("=" * 50)
    
    try:
        # Wait for TOTP page
        time.sleep(2)
        current_url = driver.current_url
        
        if "totp" in current_url:
            print(f"✅ On Google Authenticator page!")
            
            # Give clear instructions to user
            print("\n" + "=" * 60)
            print("🔢 GOOGLE AUTHENTICATOR - NHẬP MÃ 2FA")
            print("=" * 60)
            print("📱 Mở Google Authenticator app trên điện thoại")
            print("🔍 Tìm account: tigerads1998@gmail.com")
            print("📝 Nhập mã 6 số hiện tại:")
            print("=" * 60)
            
            # Get TOTP code from user
            while True:
                try:
                    totp_code = input("👆 Nhập mã 6 số từ Authenticator app: ").strip()
                    
                    if len(totp_code) != 6 or not totp_code.isdigit():
                        print("❌ Mã phải là 6 số! Thử lại...")
                        continue
                    
                    print(f"✅ Đã nhập: {totp_code}")
                    break
                    
                except KeyboardInterrupt:
                    print("\n❌ User cancelled")
                    return False
                except Exception as e:
                    print(f"❌ Input error: {e}")
                    return False
            
            # Find input field and enter code
            print("🔍 Tìm input field...")
            
            code_input = None
            input_selectors = [
                "#totpPin",
                "input[name='totpPin']",
                "input[type='tel']",
                "input[aria-label='Enter code']",
                "input[type='text']"
            ]
            
            for selector in input_selectors:
                try:
                    inp = driver.find_element(By.CSS_SELECTOR, selector)
                    if inp.is_displayed():
                        print(f"✅ Tìm thấy input field")
                        code_input = inp
                        break
                except:
                    continue
            
            if code_input:
                try:
                    # Clear and enter code
                    code_input.clear()
                    time.sleep(0.5)
                    code_input.send_keys(totp_code)
                    print(f"📝 Đã nhập code: {totp_code}")
                    
                    # Submit the code
                    print("👆 Đang submit...")
                    
                    # Find and click submit button
                    submit_button = None
                    try:
                        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                    except:
                        try:
                            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='button']")
                        except:
                            print("⌨️ Sử dụng Enter key...")
                    
                    if submit_button:
                        submit_button.click()
                        print("✅ Đã click Submit!")
                    else:
                        from selenium.webdriver.common.keys import Keys
                        code_input.send_keys(Keys.ENTER)
                        print("✅ Đã nhấn Enter!")
                    
                    # Wait and check result
                    print("\n⏳ Đang kiểm tra kết quả...")
                    time.sleep(5)
                    
                    new_url = driver.current_url
                    print(f"🎯 URL sau khi submit: {new_url[:60]}...")
                    
                    # Check for success patterns
                    if any(pattern in new_url for pattern in ["speedbump", "passkeyenrollment", "myaccount", "youtube.com", "gmail.com"]):
                        print(f"🎊 THÀNH CÔNG! Đăng nhập 2FA hoàn tất!")
                        print(f"✅ Chuyển đến trang xác thực...")
                        
                        # Handle post-login steps
                        return handle_post_login_steps(driver, profile_id)
                    
                    # Check if still on TOTP (error case)
                    elif "totp" in new_url:
                        # Look for error messages
                        page_source = driver.page_source.lower()
                        if "wrong code" in page_source or "try again" in page_source:
                            print(f"❌ LỖI: Mã 2FA không đúng!")
                            print(f"💡 Mã có thể đã hết hạn hoặc nhập sai")
                            
                            # Ask user if they want to try again
                            retry = input("🔄 Thử lại với mã mới? (y/n): ").strip().lower()
                            if retry == 'y' or retry == 'yes':
                                return handle_google_authenticator_workflow(driver, profile_id)  # Recursive retry
                            else:
                                print("❌ User chọn không thử lại")
                                return False
                        else:
                            print("🤔 Vẫn ở trang TOTP nhưng không có lỗi rõ ràng")
                            print("💡 Có thể đang xử lý hoặc cần thời gian")
                            return False
                    else:
                        print(f"⚠️ URL không mong đợi: {new_url}")
                        return False
                    
                except Exception as e:
                    print(f"❌ Lỗi khi nhập code: {e}")
                    return False
            else:
                print("❌ Không tìm thấy input field")
                print("💡 Có thể trang đã thay đổi hoặc cần approach khác")
                return False
            
        else:
            print(f"⚠️ Không ở trang TOTP mong đợi: {current_url}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi Google Authenticator workflow: {e}")
        return False

def handle_post_login_steps(driver, profile_id):
    """Handle post-login steps like skipping passkey enrollment"""
    print(f"🔄 POST-LOGIN HANDLING [{profile_id}]")
    print("=" * 40)
    
    try:
        time.sleep(2)
        current_url = driver.current_url
        
        # Check if on passkey enrollment page
        if "passkey" in current_url or "speedbump" in current_url:
            print(f"📋 On passkey enrollment page - skipping...")
            
            # Find and click "Not now"
            not_now_selectors = [
                "//button[contains(text(), 'Not now')]",
                "//a[contains(text(), 'Not now')]",
                "//button[contains(text(), 'not now')]",
                "//button[contains(text(), 'Skip')]",
                "//button[contains(text(), 'skip')]"
            ]
            
            not_now_clicked = False
            for selector in not_now_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for elem in elements:
                        if elem.is_displayed():
                            elem_text = elem.text.strip()
                            if "not now" in elem_text.lower() or "skip" in elem_text.lower():
                                try:
                                    elem.click()
                                    print(f"✅ CLICKED 'NOT NOW' - Skipped passkey enrollment!")
                                    not_now_clicked = True
                                    time.sleep(3)
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();", elem)
                                        print(f"✅ CLICKED 'NOT NOW' with JS!")
                                        not_now_clicked = True
                                        time.sleep(3)
                                        break
                                    except:
                                        continue
                    if not_now_clicked:
                        break
                except:
                    continue
            
            if not not_now_clicked:
                print(f"⚠️ Could not skip passkey enrollment")
        
        # Check final destination
        time.sleep(2)
        final_url = driver.current_url
        page_title = driver.title
        
        print(f"🎯 FINAL DESTINATION:")
        print(f"   URL: {final_url[:80]}...")
        print(f"   Title: {page_title}")
        
        if any(pattern in final_url for pattern in ["myaccount", "youtube.com", "gmail.com", "drive.google.com"]):
            print(f"🎊 LOGIN PROCESS COMPLETED SUCCESSFULLY!")
            print(f"✅ User is now authenticated and on final page")
            return True
        else:
            print(f"⚠️ May need additional steps")
            return True  # Still consider successful
            
    except Exception as e:
        print(f"❌ Post-login handling error: {e}")
        return True  # Don't fail the whole process

def extract_verification_code(driver, profile_id):
    """Extract verification code from device prompt page"""
    try:
        print(f"🔍 EXTRACTING VERIFICATION CODE [{profile_id}]...")
        
        # Look for prominent standalone numbers (1-3 digits)
        all_elements = driver.find_elements(By.CSS_SELECTOR, "*")
        candidate_codes = []
        
        for elem in all_elements:
            if elem.is_displayed():
                elem_text = elem.text.strip()
                
                # Look for standalone 1-3 digit numbers
                if re.match(r'^\d{1,3}$', elem_text):
                    try:
                        font_size = driver.execute_script("return window.getComputedStyle(arguments[0]).fontSize;", elem)
                        font_size_num = float(font_size.replace('px', ''))
                        
                        candidate_codes.append({
                            'code': elem_text,
                            'font_size': font_size_num
                        })
                    except:
                        continue
        
        if candidate_codes:
            # Find the most prominent (largest font) code
            prominent_code = max(candidate_codes, key=lambda x: x['font_size'])
            
            print(f"🎊 VERIFICATION CODE FOUND: {prominent_code['code']}")
            print(f"📏 Font size: {prominent_code['font_size']}px")
            print("=" * 50)
            print(f"📱 ENTER THIS CODE ON YOUR PHONE: {prominent_code['code']}")
            print("=" * 50)
            
            return prominent_code['code']
        else:
            print("⚠️ No verification code found")
            return None
            
    except Exception as e:
        print(f"❌ Error extracting code: {e}")
        return None

def ultra_fast_login(debug_port, profile_id):
    """ULTRA SPEED LOGIN with improved password detection"""
    print(f"⚡ ULTRA LOGIN [{profile_id}]")
    
    # ULTRA FAST Chrome with English Language
    chrome_options = Options()
    chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{debug_port}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-images')
    chrome_options.add_argument('--disable-plugins')
    # Force English language regardless of IP location
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_argument('--accept-lang=en-US,en;q=0.9')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print(f"🔗 CONNECTED [{profile_id}]")
    except Exception as e:
        print(f"❌ CONNECT FAILED [{profile_id}]")
        return None
    
    try:
        # INSTANT focus
        driver.execute_script("window.focus();")
        
        # DIRECT TO GOOGLE WITH ENGLISH LANGUAGE
        print(f"🌐 GOOGLE [{profile_id}] - FORCING ENGLISH")
        driver.get("https://accounts.google.com/signin?hl=en")
        
        # ULTRA FAST email
        email_input = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        
        email = "tigerads1998@gmail.com"
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", email_input, email)
        print(f"📧 EMAIL [{profile_id}]")
        
        # INSTANT Next
        next_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, "identifierNext"))
        )
        driver.execute_script("arguments[0].click();", next_button)
        print(f"👆 NEXT [{profile_id}]")
        
        # CHECK FOR EMAIL ERRORS
        print(f"🔍 CHECKING EMAIL VALIDITY [{profile_id}]...")
        email_error = False
        
        for email_check_i in range(5):  # Check for 5 seconds
            time.sleep(1)
            current_url = driver.current_url
            page_source = driver.page_source.lower()
            
            # Email error indicators
            email_error_indicators = [
                "couldn't find your google account", "couldn't find google account",
                "enter a valid email", "invalid email", "email address not found",
                "that username is not valid", "that email address is not valid",
                "account doesn't exist", "no such user", "email not found",
                "try again", "please try again"
            ]
            
            # Check for specific email error messages
            found_email_error = None
            for error in email_error_indicators:
                if error in page_source:
                    found_email_error = error
                    break
            
            if found_email_error:
                print(f"❌ EMAIL ERROR DETECTED [{profile_id}]!")
                print(f"📧 Email: tigerads1998@gmail.com")
                print(f"📄 Error message found: '{found_email_error}'")
                
                # Look for full email error message
                try:
                    error_elements = driver.find_elements(By.CSS_SELECTOR, ".error, [role='alert'], .warning, .Df4rGb, [data-error]")
                    for elem in error_elements:
                        if elem.is_displayed() and elem.text.strip():
                            print(f"📝 Full error: {elem.text}")
                            break
                except:
                    pass
                
                print(f"💡 Email address is invalid or does not exist")
                email_error = True
                return None
            
            # Check if moved to password page (email is valid)
            if "password" in page_source or "pwd" in current_url:
                print(f"✅ EMAIL VALID [{profile_id}] - Moved to password page after {email_check_i+1}s!")
                break
        
        if email_error:
            return None
        
        # IMPROVED password detection
        password_found = False
        for i in range(12):  # 12 second max
            try:
                # Multiple password selectors
                password_selectors = [
                    "input[type='password']",
                    "input[name='password']", 
                    "#password",
                    "[aria-label*='password']",
                    "[aria-label*='Password']"
                ]
                
                for selector in password_selectors:
                    password_inputs = driver.find_elements(By.CSS_SELECTOR, selector)
                    visible_password = [p for p in password_inputs if p.is_displayed()]
                    
                    if visible_password:
                        print(f"🔑 PASSWORD [{profile_id}] {i+1}s")
                        
                        password = "lovetime01"
                        password_input = visible_password[0]
                        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", password_input, password)
                        
                        # ULTRA FAST Next click
                        next_selectors = [
                            "#passwordNext",
                            "button[type='submit']",
                            "[data-continue-text]",
                            "button[jsname]"
                        ]
                        
                        for next_sel in next_selectors:
                            try:
                                next_btns = driver.find_elements(By.CSS_SELECTOR, next_sel)
                                for btn in next_btns:
                                    if btn.is_displayed():
                                        driver.execute_script("arguments[0].click();", btn)
                                        print(f"🚀 SUBMITTED [{profile_id}]")
                                        
                                        # Wait for page to load and check result
                                        print(f"⏳ WAITING FOR PAGE LOAD [{profile_id}]...")
                                        
                                        # Check for password errors first
                                        password_error = False
                                        for check_i in range(8):  # Check for 8 seconds
                                            time.sleep(1)
                                            current_url = driver.current_url
                                            page_source = driver.page_source.lower()
                                            
                                            # Check for password error messages
                                            error_indicators = [
                                                "wrong password", "incorrect password", "invalid password",
                                                "couldn't sign you in", "password is incorrect",
                                                "try again", "password doesn't match",
                                                "your password was changed", "password was changed",
                                                "please try again", "sign-in was unsuccessful",
                                                "couldn't verify", "verification failed"
                                            ]
                                            
                                            # Check for specific error messages
                                            found_error = None
                                            for error in error_indicators:
                                                if error in page_source:
                                                    found_error = error
                                                    break
                                            
                                            if found_error:
                                                print(f"❌ PASSWORD ERROR DETECTED [{profile_id}]!")
                                                print(f"🔑 Email: tigerads1998@gmail.com")
                                                print(f"🔑 Password: lovetime01")
                                                print(f"📄 Error message found: '{found_error}'")
                                                
                                                # Look for full error message
                                                try:
                                                    error_elements = driver.find_elements(By.CSS_SELECTOR, ".error, [role='alert'], .warning, .Df4rGb")
                                                    for elem in error_elements:
                                                        if elem.is_displayed() and elem.text.strip():
                                                            print(f"📝 Full error: {elem.text}")
                                                            break
                                                except:
                                                    pass
                                                
                                                print(f"💡 Please verify password is correct and try again")
                                                password_error = True
                                                break
                                            
                                            # Check if successfully moved to 2FA page (exclude password challenges)
                                            if ("challenge" in current_url or "verification" in current_url) and "pwd" not in current_url:
                                                print(f"✅ 2FA PAGE REACHED [{profile_id}] after {check_i+1}s!")
                                                break
                                            elif "pwd" in current_url and check_i >= 2:
                                                print(f"⚠️ STILL ON PASSWORD CHALLENGE [{profile_id}] after {check_i+1}s")
                                                # Continue checking, might be processing
                                            
                                            # Check if fully logged in
                                            if "myaccount" in current_url or "accounts.google.com/b/0" in current_url:
                                                print(f"✅ FULLY LOGGED IN [{profile_id}] after {check_i+1}s!")
                                                break
                                        
                                        if password_error:
                                            return None
                                        
                                        # Final URL check
                                        current_url = driver.current_url
                                        print(f"🎉 FINAL RESULT [{profile_id}] {current_url[:30]}...")
                                        
                                        # Only confirm 2FA if NOT a password page
                                        if ("challenge" in current_url or "totp" in current_url or "verification" in current_url) and "pwd" not in current_url:
                                            print(f"✅ 2FA CONFIRMED [{profile_id}]!")
                                            # Wait a bit more for page to fully load before exploring
                                            print(f"⏳ WAITING FOR 2FA PAGE TO FULLY LOAD...")
                                            time.sleep(4)  # Extra wait for 2FA page to load completely
                                            
                                            # AUTO EXPLORE 2FA OPTIONS
                                            explore_2fa_options(driver, profile_id)
                                        elif "pwd" in current_url:
                                            print(f"❌ STILL ON PASSWORD PAGE [{profile_id}]!")
                                            print(f"🔑 Email: tigerads1998@gmail.com")
                                            print(f"🔑 Password may be incorrect: lovetime01")
                                            print(f"💡 Check if password is wrong or needs manual verification")
                                        elif "myaccount" in current_url or "accounts.google.com/b/0" in current_url:
                                            print(f"✅ FULLY LOGGED IN [{profile_id}]!")
                                        else:
                                            print(f"⚠️ UNKNOWN PAGE [{profile_id}] - Manual check needed")
                                        
                                        password_found = True
                                        return driver
                            except:
                                continue
                        
                        if password_found:
                            break
                
                if password_found:
                    break
                    
            except:
                pass
                
            time.sleep(1)
        
        if not password_found:
            print(f"⚠️ NO PASSWORD [{profile_id}]")
        
        return driver
        
    except Exception as e:
        print(f"❌ ERROR [{profile_id}]: {e}")
        return driver

def main():
    """Main function with profile pool system - set proxy then start"""
    print("⚡ ULTRA FAST LOGIN V2 - PROXY FIRST SYSTEM")
    print("🔥 SET PROXY → START PROFILE → INSTANT LOGIN") 
    print("🚀 NO PROXY SWITCHING ISSUES + ZERO WAIT TIME")
    print("🌍 SUPPORTS ALL COUNTRIES WORLDWIDE")
    print("-" * 70)
    
    # Initialize profile pool
    print("🔧 CHECKING PROFILE POOL STATUS...")
    pool = initialize_profile_pool()
    
    ready_profiles = [p for p in pool if p.get('status') == 'ready']
    completed_profiles = [p for p in pool if p.get('status') == 'completed']
    in_use_profiles = [p for p in pool if p.get('status') == 'in_use']
    
    print(f"\n📊 CURRENT POOL STATUS:")
    print(f"   ✅ Ready: {len(ready_profiles)}")
    print(f"   🎯 In Use: {len(in_use_profiles)}")
    print(f"   ✅ Completed: {len(completed_profiles)}")
    print()
    
    # Enhanced country selection
    while True:
        country_input = input(f"Country code, 'list', or ENTER for US: ").strip().upper()
        
        if not country_input:
            country = "US"
            print(f"🎯 COUNTRY: {country} (Default)")
            break
        elif country_input == "LIST":
            display_country_options()
            continue
        elif country_input in COUNTRY_CODES:
            country = country_input
            country_name = COUNTRY_CODES[country]
            print(f"🎯 COUNTRY: {country} ({country_name})")
            break
        else:
            print(f"❌ Invalid country code: {country_input}")
            print("💡 Type 'list' to see all available countries")
            continue
    
    # Get profile for the country (set proxy + start)
    profile_uuid, debug_port, proxy_config, profile_id = get_profile_for_country(country)
    
    if not debug_port:
        print("❌ FAILED TO PREPARE PROFILE!")
        return
    
    print(f"✅ PROFILE READY FOR {country} [{profile_id}] PORT: {debug_port}")
    
    # Execute login
    driver = ultra_fast_login(debug_port, profile_id)
    
    if driver:
        print(f"🎊 LOGIN SUCCESS [{profile_id}]!")
        print(f"🆔 {profile_uuid}")
        print(f"🔌 {debug_port}")
        print(f"🌐 {country}")
        if proxy_config:
            proxy_session = proxy_config["login"].split("-sessid-")[1].split("-sesstime-")[0]
            print(f"🔗 Proxy Session: {proxy_session}")
        else:
            print(f"🔗 No Proxy")
        print("🔥 MISSION COMPLETED!")
        
        # Mark profile as completed and create new one
        mark_profile_completed(profile_uuid, success=True)
        
        input(f"ENTER TO FINISH...")
    else:
        print(f"❌ LOGIN FAILED [{profile_id}]")
        # Mark profile as ready again (reusable)
        mark_profile_completed(profile_uuid, success=False)

if __name__ == "__main__":
    main() 