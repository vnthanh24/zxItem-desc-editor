# Build Script cho Advanced Text Editor Tool

## Yêu cầu hệ thống
- Python 3.7+
- PyInstaller
- Các thư viện trong requirements.txt

## Hướng dẫn build

### 1. Cài đặt PyInstaller
```bash
pip install pyinstaller
```

### 2. Chạy script build
```bash
# Windows
build_exe.bat

# Hoặc chạy trực tiếp
python build_exe.py
```

### 3. File exe sẽ được tạo trong thư mục `dist/`

## Cấu trúc build
- **One-file**: Tạo file exe đơn lẻ (khuyến nghị)
- **Windowed**: Không hiển thị console
- **Icon**: Sử dụng icon tùy chỉnh (nếu có)
- **Tối ưu size**: Loại bỏ các module không cần thiết

## Lưu ý
- File exe có thể mất vài giây để khởi động lần đầu
- Size file khoảng 20-50MB do chứa Python runtime
- Antivirus có thể cảnh báo false positive với file exe mới build

## Troubleshooting
- Nếu lỗi missing module, thêm `--hidden-import module_name`
- Nếu file quá lớn, sử dụng `--exclude-module` để loại bỏ module không cần
- Nếu lỗi path, đảm bảo sử dụng absolute path trong code