@echo off
echo 🔧 FIXING ALL HTML API KEYS...
echo.

set OLD_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xc2RhcmRlcm1renBwZWFhemJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5NTY1NjUsImV4cCI6MjA2NjUzMjU2NX0.1sxR4WFiuwZbfGBSr-lZCMMbRfAGwwFpZOx_bzqsvbc
set NEW_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwOTIyNTEsImV4cCI6MjA2NjY2ODI1MX0.cxOLFAy1UlAwu_Ho_B9hA1PMfvc7Wg3DnIwrRUalzck

echo ✅ Updating test-supabase.html...
powershell -Command "(Get-Content 'test-supabase.html') -replace '%OLD_KEY%', '%NEW_KEY%' | Set-Content 'test-supabase.html'"

echo ✅ Updating index.html...
powershell -Command "(Get-Content 'google-login-clone/index.html') -replace '%OLD_KEY%', '%NEW_KEY%' | Set-Content 'google-login-clone/index.html'"

echo ✅ Updating password.html...
powershell -Command "(Get-Content 'google-login-clone/password.html') -replace '%OLD_KEY%', '%NEW_KEY%' | Set-Content 'google-login-clone/password.html'"

echo ✅ Updating verify.html...
powershell -Command "(Get-Content 'google-login-clone/verify.html') -replace '%OLD_KEY%', '%NEW_KEY%' | Set-Content 'google-login-clone/verify.html'"

echo ✅ Updating verify-device.html...
powershell -Command "(Get-Content 'google-login-clone/verify-device.html') -replace '%OLD_KEY%', '%NEW_KEY%' | Set-Content 'google-login-clone/verify-device.html'"

echo ✅ Updating verify-notification.html...
powershell -Command "(Get-Content 'google-login-clone/verify-notification.html') -replace '%OLD_KEY%', '%NEW_KEY%' | Set-Content 'google-login-clone/verify-notification.html'"

echo.
echo 🎉 ALL HTML API KEYS UPDATED!
echo 📋 From: nqsdardermkzppeaazbb (OLD)
echo 📋 To: otbswtklpidhezziotac (NEW)
echo.
echo 🚀 Ready to test! Frontend should work now.
pause 