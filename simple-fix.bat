@echo off
echo 🔧 FIXING REMAINING HTML FILES...

echo ✅ Fixing index.html...
powershell -Command "(Get-Content 'google-login-clone/index.html') -replace 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xc2RhcmRlcm1renBwZWFhemJiIi', 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIi' | Set-Content 'google-login-clone/index.html'"

echo ✅ Fixing verify.html...
powershell -Command "(Get-Content 'google-login-clone/verify.html') -replace 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xc2RhcmRlcm1renBwZWFhemJiIi', 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIi' | Set-Content 'google-login-clone/verify.html'"

echo ✅ Fixing verify-device.html...
powershell -Command "(Get-Content 'google-login-clone/verify-device.html') -replace 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xc2RhcmRlcm1renBwZWFhemJiIi', 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIi' | Set-Content 'google-login-clone/verify-device.html'"

echo ✅ Fixing verify-notification.html...
powershell -Command "(Get-Content 'google-login-clone/verify-notification.html') -replace 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xc2RhcmRlcm1renBwZWFhemJiIi', 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIi' | Set-Content 'google-login-clone/verify-notification.html'"

echo ✅ Fixing test-supabase.html...
powershell -Command "(Get-Content 'test-supabase.html') -replace 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xc2RhcmRlcm1renBwZWFhemJiIi', 'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIi' | Set-Content 'test-supabase.html'"

echo.
echo 🎉 ALL DONE! All HTML files updated with new API key.
pause 