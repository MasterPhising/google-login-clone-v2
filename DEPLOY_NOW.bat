@echo off
echo ========================================
echo  DEPLOY NOW - AFTER CREATING GITHUB REPO
echo ========================================

echo [1/3] Push to GitHub...
git push -u origin master

echo [2/3] Tag release...
git tag -a v2.1-clean -m "Version 2.1 - Clean Auto-Login folder"
git push origin v2.1-clean

echo [3/3] Repository ready!
echo.
echo ========================================
echo  GITHUB DEPLOYED! NEXT: NETLIFY
echo ========================================
echo.
echo Frontend V2:
echo https://app.netlify.com/start/deploy?repository=https://github.com/tigerads1998/google-login-clone-v2
echo.
echo Admin GUI V2:  
echo Same repo, different publish directory
echo.
echo ========================================

pause 