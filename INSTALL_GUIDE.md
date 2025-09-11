# HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG

## ⚠️ LỖI ENCODING - GIẢI PHÁP

Nếu bạn gặp lỗi:
```
'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

**Nguyên nhân:** File của bạn không phải encoding UTF-8, có thể là:
- ANSI (Windows-1252)
- UTF-16 (Unicode)
- GB2312/GBK (Tiếng Trung)
- Big5 (Tiếng Trung Phồn thể)

**Giải pháp đã được tích hợp:**
✅ Tool đã được cập nhật để tự động phát hiện và xử lý các encoding khác nhau
✅ Không cần chuyển đổi file, tool sẽ tự động xử lý

## 🚀 CÁCH CÀI ĐẶT NHANH

### Bước 1: Cài đặt Python
1. Vào https://www.python.org/downloads/
2. Tải Python 3.9+ (khuyến nghị Python 3.11)
3. **QUAN TRỌNG:** Khi cài đặt, PHẢI tick ☑️ "Add Python to PATH"
4. Cài đặt với tùy chọn mặc định

### Bước 2: Kiểm tra cài đặt
Mở Command Prompt và gõ:
```
python --version
```
Nếu hiện Python 3.x.x thì đã thành công.

### Bước 3: Cài thư viện (tùy chọn)
Double-click vào `install_requirements.bat` hoặc chạy:
```
pip install chardet
```

### Bước 4: Chạy tool
Double-click vào `run_tool.bat`

## 🛠️ TROUBLESHOOTING

### Lỗi: "Python was not found"
**Giải pháp:**
1. Cài lại Python và nhớ tick "Add Python to PATH"
2. Hoặc restart máy sau khi cài Python
3. Hoặc sử dụng `py` thay vì `python`:
   ```
   py text_editor_tool.py
   ```

### Lỗi: "No module named 'tkinter'"
**Giải pháp:**
- Trên Windows: Tkinter có sẵn với Python
- Trên Linux: `sudo apt-get install python3-tkinter`
- Trên macOS: Cài Python từ python.org (không dùng brew)

### File không mở được
**Kiểm tra:**
1. File có đúng định dạng: `ID[TAB]"nội dung"` không?
2. File có bị khóa bởi chương trình khác không?
3. Có quyền đọc file không?

### Tool chạy nhưng không hiển thị nội dung
**Nguyên nhân:** File không đúng định dạng
**Định dạng đúng:**
```
70718	"^6cfb4bThiên cơ vô thường, thanh lục khuy mệnh.\r^ffcb4aNội dung..."
70719	"^ff0000Nội dung khác..."
```

**Lưu ý:**
- Phải có TAB (không phải space) giữa ID và nội dung
- Nội dung phải được bao bởi dấu ngoặc kép
- Mã màu có định dạng ^xxxxxx (6 ký tự hex)

## 📞 HỖ TRỢ

Nếu vẫn gặp lỗi, hãy:
1. Chụp ảnh màn hình lỗi
2. Gửi file mẫu bị lỗi (vài dòng đầu)
3. Cho biết hệ điều hành đang dùng

## 📋 CHECKLIST TRƯỚC KHI SỬ DỤNG

- ☑️ Đã cài Python 3.9+
- ☑️ Python đã được thêm vào PATH
- ☑️ Có thể chạy `python --version` trong Command Prompt
- ☑️ File .txt có đúng định dạng
- ☑️ Đã backup file gốc (tool tự động backup nhưng nên backup thêm)

## 🎯 TEST NHANH

1. Mở Command Prompt
2. Gõ: `cd "e:\Desktop\item desc edit"`
3. Gõ: `python text_editor_tool.py`
4. Mở file `sample_data.txt` để test

Nếu bước 3 báo lỗi "Python was not found" → cài lại Python
Nếu tool mở được → thành công! 🎉
