@echo off
echo 🧪 TESTING AFTER DATABASE FIX...
echo.
echo 🔍 Testing if page_status column fix worked:
node test-simple-insert.js
echo.
echo 📊 If successful, testing full API:
node test-admin-api.js
echo.
echo 🎉 Test completed!
pause 