# 🚀 SUPABASE DEPLOYMENT - 2 FILES RIÊNG BIỆT

## 📋 **BƯỚC 1: DATABASE SETUP**

### **👆 GO TO:**
https://supabase.com/dashboard/project/otbswtklpidhezziotac

### **🗄️ SQL EDITOR → NEW QUERY:**
1. Click "SQL Editor" ở sidebar  
2. Click "New Query"
3. **Copy toàn bộ** nội dung từ file: `configs/supabase-database-schema-v2.sql`
4. **Paste** vào SQL Editor
5. **Click "Run"** (hoặc Ctrl+Enter)

**✅ Kết quả mong đợi:**
- Thông báo "Success. No rows returned"
- Tạo được table `requests` với tất cả columns
- Tạo được indexes và functions

---

## ⚡ **BƯỚC 2: EDGE FUNCTION SETUP**

### **🌐 FUNCTIONS → CREATE NEW FUNCTION:**
1. Click "Edge Functions" ở sidebar
2. Click "Create a new function"
3. **Function name**: `admin-api`
4. Copy toàn bộ** nội dung từ file: `configs/supabase-edge-function-v2.ts`
5. **Paste** vào code editor (replace all existing code)
6. **Click "Deploy"**

**✅ Kết quả mong đợi:**
- Function deploy thành công
- URL available: `https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api`

---

## 🧪 **BƯỚC 3: TEST EVERYTHING**

### **Test Edge Function:**
```bash
curl https://otbswtklpidhezziotac.supabase.co/functions/v1/admin-api/status \
  -H "apikey: YOUR_ANON_KEY"
```

**Expected response:**
```json
{
  "success": true,
  "version": "2.1-AUTO-LOGIN-WITH-COUNTRY",
  "country_detection": "enabled"
}
```

---

## 📁 **FILES SUMMARY:**

| File | Purpose | Where to use |
|------|---------|--------------|
| `supabase-database-schema-v2.sql` | Database schema | Supabase SQL Editor |
| `supabase-edge-function-v2.ts` | API backend | Supabase Edge Functions |
| `SUPABASE_DEPLOYMENT_GUIDE.md` | Instructions | This guide |

---

## 🎯 **FEATURES INCLUDED:**

✅ **Auto-Login Integration** - Real Google login tests  
✅ **Country Detection** - IP geolocation với US fallback  
✅ **2FA Automation** - Automatic verification handling  
✅ **Real-time Approval** - Instant approve/deny based on tests  
✅ **Admin Dashboard** - Complete request management  

---

**🎉 SAU KHI HOÀN THÀNH 2 BƯỚC → VERSION 2.1 READY!** 