# 🐍 HƯỚNG DẪN CÀI ĐẶT PYTHON ĐÚNG CÁCH

## ❌ Vấn đề hiện tại:
Bạn đang gặp lỗi này có nghĩa là Python chưa được cài đặt đúng cách hoặc chưa được thêm vào PATH.

## ✅ GIẢI PHÁP: Cài đặt Python từ python.org

### Bước 1: Tải Python
1. Vào trang chủ: **https://www.python.org/downloads/**
2. Click **"Download Python 3.xx"** (phiên bản mới nhất)
3. Tải file `.exe` về máy

### Bước 2: Cài đặt Python
1. **Chạy file .exe vừa tải**
2. **QUAN TRỌNG:** ✅ **PHẢI TICK** vào ô **"Add Python to PATH"** ở màn hình đầu tiên
3. Chọn **"Install Now"**
4. Chờ cài đặt hoàn tất

### Bước 3: Kiểm tra cài đặt
1. **Mở Command Prompt mới** (đóng cửa sổ cũ)
2. Gõ: `python --version`
3. Nếu hiện `Python 3.x.x` → Thành công! 🎉

### Bước 4: Chạy tool
```bash
cd "e:\Desktop\item desc edit"
python advanced_text_editor.py
```

## 🚨 LƯU Ý QUAN TRỌNG:

### ❌ KHÔNG cài từ Microsoft Store
- Python từ Microsoft Store thường có vấn đề với PATH
- Có thể bị giới hạn quyền

### ✅ CÀI từ python.org
- Cài đặt đầy đủ, ổn định
- Có đầy đủ pip và các thư viện

### 🔄 Nếu đã cài sai:
1. **Gỡ cài đặt** Python hiện tại từ Settings > Apps
2. **Cài lại** từ python.org với **"Add to PATH"**
3. **Restart** máy tính
4. **Test lại** với `python --version`

## 🛠️ TROUBLESHOOTING

### Lỗi: "Python was not found"
**Nguyên nhân:** Python chưa được thêm vào PATH
**Giải pháp:** 
1. Cài lại Python với "Add to PATH"
2. Hoặc thêm PATH thủ công:
   - Mở System Properties > Environment Variables
   - Thêm đường dẫn Python vào PATH (ví dụ: `C:\Python311\`)

### Lỗi: "'python' is not recognized"
**Nguyên nhân:** Tương tự trên
**Giải pháp:** Restart Command Prompt sau khi cài Python

### Test nhanh:
```bash
# Kiểm tra Python
python --version

# Kiểm tra pip
pip --version

# Chạy tool
python advanced_text_editor.py
```

## 📞 Nếu vẫn gặp vấn đề:
1. Chụp ảnh màn hình lỗi
2. Cho biết bước nào đang gặp khó khăn
3. Kiểm tra lại đã tick "Add to PATH" chưa

**Lưu ý:** Sau khi cài Python đúng cách, tool sẽ chạy ngay lập tức! 🚀
