# 🚀 MANUAL DEPLOYMENT GUIDE

## ⚠️ HIỆN TẠI: FUNCTION CHƯA ĐƯỢC DEPLOY

Function đã được cập nhật với code đúng cho project mới, nhưng chưa được deploy lên Supabase.

---

## 📋 BƯỚC 1: DEPLOY EDGE FUNCTION

### **1.1 Vào Supabase Dashboard**
- URL: https://supabase.com/dashboard/project/otbswtklpidhezziotac
- Click **"Edge Functions"** ở sidebar trái

### **1.2 Tạo Function Mới**
- Click **"Create a new function"**
- Function name: `admin-api`
- Template: Blank hoặc Hello World
- Click **"Create function"**

### **1.3 Deploy Code**
- Xóa toàn bộ code template có sẵn
- Copy toàn bộ code từ file: **`DEPLOY_EDGE_FUNCTION_CODE.ts`** 
- Paste vào code editor
- Click **"Deploy"** hoặc **"Save"**
- Chờ deploy hoàn tất (có thể mất 30-60 giây)

### **1.4 Verify Deploy**
- Status function phải là **"Active"** (màu xanh)
- Test URL: `https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api/`

---

## 📋 BƯỚC 2: SETUP DATABASE SCHEMA

### **2.1 Vào SQL Editor**
- Click **"SQL Editor"** ở sidebar trái
- Click **"New Query"**

### **2.2 Chạy Schema Script**
- Copy toàn bộ nội dung từ file: **`DEPLOY_DATABASE_SCHEMA.sql`**
- Paste vào SQL Editor

### **2.3 Chạy Script**
- Click **"Run"** (hoặc Ctrl+Enter)
- Verify: Có thông báo "SUCCESS: Database schema created successfully..."
- Kiểm tra **Table Editor** → có table `requests` với 5 sample records

---

## 📋 BƯỚC 3: TEST SAU KHI DEPLOY

Sau khi hoàn thành 2 bước trên, chạy lại test:

```bash
node test-new-project-api.js
```

**Expected Results:**
- ✅ ROOT Status: 200 (thay vì 404)
- ✅ Function response: "NEW PROJECT ADMIN API WORKING! 🚀"
- ✅ Version: "2.1-AUTO-LOGIN-NEW-PROJECT-WITH-COUNTRY"
- ✅ Auto Login: Enabled
- ✅ Country Detection: Enabled

---

## 🎯 TROUBLESHOOTING

### **Function Still 404:**
1. Kiểm tra function name chính xác: `admin-api`
2. Đảm bảo function status là "Active" 
3. Thử redeploy function
4. Clear browser cache và thử lại

### **Database Errors:**
1. Kiểm tra table `requests` đã được tạo
2. Verify có sample data (3 test records)
3. Kiểm tra RLS policies enabled

### **Permission Errors:**
1. Đảm bảo dùng đúng service role key trong function
2. Kiểm tra API keys trong Supabase Settings

---

## ✅ VERIFICATION CHECKLIST

- [ ] Edge function `admin-api` deployed successfully
- [ ] Function status is "Active" 
- [ ] Database table `requests` created
- [ ] Sample data inserted (3 test records)
- [ ] Test script returns 200 status codes
- [ ] Frontend có thể gửi data thành công

---

**🎉 SAU KHI HOÀN THÀNH: Frontend sẽ có thể gửi dữ liệu đến Supabase thành công!**

---

## 📁 FILES ĐƯỢC TẠO:

- **`DEPLOY_EDGE_FUNCTION_CODE.ts`** - Complete Edge Function code (Copy vào Supabase Edge Functions)
- **`DEPLOY_DATABASE_SCHEMA.sql`** - Complete database schema (Copy vào Supabase SQL Editor)
- **`MANUAL_DEPLOY_GUIDE.md`** - Hướng dẫn chi tiết deployment

**📋 Chỉ cần copy/paste 2 files trên vào Supabase là xong!** 