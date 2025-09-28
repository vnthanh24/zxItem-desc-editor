# Build Files cho Advanced Text Editor Tool

## 📋 Danh sách file build

### Script build chính
- **`build_exe.py`** - Script Python build chính với giao diện interactive
- **`build_exe.bat`** - Script batch cho Windows (gọi build_exe.py)
- **`build_exe.sh`** - Script shell cho Linux/macOS (gọi build_exe.py)
- **`quick_build.bat`** - Script build nhanh không hỏi (Windows)

### File cấu hình
- **`AdvancedTextEditor.spec`** - File cấu hình PyInstaller (có thể tùy chỉnh)
- **`main.py`** - Entry point chính cho exe (wrapper cho advanced_text_editor.py)

### File hỗ trợ
- **`requirements.txt`** - Dependencies cần thiết (bao gồm pyinstaller)
- **`BUILD_GUIDE.md`** - Hướng dẫn chi tiết về build process

## 🚀 Cách sử dụng

### Build cơ bản (khuyến nghị)
```bash
# Windows
build_exe.bat

# Linux/macOS  
chmod +x build_exe.sh
./build_exe.sh
```

### Build nhanh (Windows)
```bash
quick_build.bat
```

### Build thủ công
```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy build script
python build_exe.py

# Hoặc dùng PyInstaller trực tiếp
pyinstaller AdvancedTextEditor.spec
```

## 📁 Cấu trúc output

Sau khi build thành công, bạn sẽ có:

```
dist/
├── AdvancedTextEditor.exe      # File exe chính
├── Run_AdvancedTextEditor.bat  # Script chạy exe
├── README.md                   # Tài liệu
├── DELETE_MULTIPLE_ITEMS.md    # Hướng dẫn tính năng mới
└── BUILD_GUIDE.md             # Hướng dẫn build
```

## 🔧 Tùy chỉnh build

### Thay đổi tên file exe
Sửa biến `APP_NAME` trong `build_exe.py`:
```python
APP_NAME = "TenMoi"
```

### Thêm icon
1. Đặt file `app_icon.ico` vào thư mục gốc
2. Build script sẽ tự động sử dụng

### Loại bỏ module không cần
Thêm vào `excludes` trong `build_exe.py`:
```python
"--exclude-module", "ten_module",
```

### Thêm file vào exe
Thêm vào `datas` trong `AdvancedTextEditor.spec`:
```python
datas=[
    ('file.txt', '.'),
    ('folder/*', 'folder'),
]
```

## 🐛 Troubleshooting

### Lỗi "module not found"
```bash
# Thêm hidden import
--hidden-import module_name
```

### File exe quá lớn
```bash
# Loại bỏ module không cần
--exclude-module module_name
```

### Lỗi antivirus
- File exe mới build có thể bị cảnh báo false positive
- Thêm exception trong antivirus
- Hoặc build trên máy sạch

### Exe chạy chậm
- Lần đầu khởi động có thể chậm (giải nén)
- Lần sau sẽ nhanh hơn
- Cân nhặc dùng `--onedir` thay vì `--onefile`

## 🎯 Tips & Tricks

1. **Build release**: Sử dụng `--strip` và `--upx` để giảm size
2. **Debug build**: Thêm `--debug` để debug khi có lỗi
3. **Console app**: Bỏ `--windowed` nếu cần console
4. **Splash screen**: Thêm `--splash image.png` cho màn hình chờ
5. **Version info**: Tạo file version và dùng `--version-file`

## 📝 Changelog

### v1.0
- ✅ Script build cơ bản với PyInstaller
- ✅ Tự động detect virtual environment
- ✅ Tối ưu size với exclude modules
- ✅ Interactive build với confirmation
- ✅ Auto-copy documentation files
- ✅ Create runner batch file
- ✅ Cross-platform support (Windows/Linux/macOS)