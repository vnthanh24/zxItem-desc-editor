#!/usr/bin/env python3
"""
Build script để tạo file executable cho Advanced Text Editor Tool
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Thông tin build
APP_NAME = "AdvancedTextEditor"
MAIN_SCRIPT = "advanced_text_editor.py"
BUILD_DIR = "build"
DIST_DIR = "dist"
SPEC_FILE = f"{APP_NAME}.spec"

# Cấu hình PyInstaller
PYINSTALLER_ARGS = [
    "--name", APP_NAME,
    "--onefile",  # Tạo file exe đơn lẻ
    "--windowed",  # Không hiển thị console
    "--clean",  # Xóa cache và build cũ
    "--noconfirm",  # Không hỏi confirm khi ghi đè
    # "--icon", "icon.ico",  # Uncomment nếu có file icon
    "--add-data", "README.md;.",  # Thêm README vào exe
    "--add-data", "*.md;.",  # Thêm tất cả file .md
    "--exclude-module", "matplotlib",  # Loại bỏ các module không cần thiết
    "--exclude-module", "numpy",
    "--exclude-module", "scipy",
    "--exclude-module", "pandas",
    "--exclude-module", "PIL",
    "--hidden-import", "tkinter.filedialog",  # Đảm bảo import tkinter components
    "--hidden-import", "tkinter.messagebox",
    "--hidden-import", "tkinter.scrolledtext",
    "--hidden-import", "chardet",
]

def get_python_executable():
    """Lấy đường dẫn Python executable"""
    # Thử tìm trong virtual environment trước
    venv_paths = [
        ".venv/Scripts/python.exe",  # Windows venv
        ".venv/bin/python",          # Linux/macOS venv
        "venv/Scripts/python.exe",   # Windows venv (tên khác)
        "venv/bin/python",           # Linux/macOS venv (tên khác)
    ]
    
    for venv_path in venv_paths:
        if os.path.exists(venv_path):
            return os.path.abspath(venv_path)
    
    # Fallback to system Python
    return sys.executable

def get_pyinstaller_executable():
    """Lấy đường dẫn PyInstaller executable"""
    python_exe = get_python_executable()
    python_dir = os.path.dirname(python_exe)
    
    # Thử tìm PyInstaller trong cùng thư mục với Python
    if sys.platform == "win32":
        pyinstaller_path = os.path.join(python_dir, "pyinstaller.exe")
    else:
        pyinstaller_path = os.path.join(python_dir, "pyinstaller")
    
    if os.path.exists(pyinstaller_path):
        return pyinstaller_path
    
    # Fallback to system PyInstaller
    return "pyinstaller"

def check_requirements():
    """Kiểm tra các yêu cầu cần thiết"""
    print("🔍 Kiểm tra yêu cầu...")
    
    # Kiểm tra Python version
    if sys.version_info < (3, 7):
        print("❌ Yêu cầu Python 3.7 trở lên")
        return False
    
    python_exe = get_python_executable()
    print(f"✅ Python {sys.version} ({python_exe})")
    
    # Kiểm tra file chính
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ Không tìm thấy file {MAIN_SCRIPT}")
        return False
    print(f"✅ Tìm thấy {MAIN_SCRIPT}")
    
    # Kiểm tra PyInstaller
    try:
        pyinstaller_exe = get_pyinstaller_executable()
        result = subprocess.run([pyinstaller_exe, "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ PyInstaller {result.stdout.strip()} ({pyinstaller_exe})")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller chưa được cài đặt")
        print("💡 Chạy: pip install pyinstaller")
        return False
    
    return True

def install_dependencies():
    """Cài đặt dependencies"""
    print("\n📦 Cài đặt dependencies...")
    
    python_exe = get_python_executable()
    
    # Cài đặt PyInstaller nếu chưa có
    try:
        subprocess.run([python_exe, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller đã được cài đặt")
    except subprocess.CalledProcessError:
        print("❌ Lỗi khi cài đặt PyInstaller")
        return False
    
    # Cài đặt requirements.txt nếu có
    if os.path.exists("requirements.txt"):
        try:
            subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Đã cài đặt requirements.txt")
        except subprocess.CalledProcessError:
            print("❌ Lỗi khi cài đặt requirements.txt")
            return False
    
    return True

def clean_build_dirs():
    """Xóa các thư mục build cũ"""
    print("\n🧹 Dọn dẹp thư mục build cũ...")
    
    dirs_to_clean = [BUILD_DIR, DIST_DIR, "__pycache__"]
    files_to_clean = [SPEC_FILE]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ Đã xóa thư mục {dir_name}")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🗑️ Đã xóa file {file_name}")

def create_icon():
    """Tạo icon đơn giản nếu chưa có"""
    icon_path = "app_icon.ico"
    if not os.path.exists(icon_path):
        print(f"\n🎨 Tạo icon mặc định...")
        # Tạo icon đơn giản bằng Python (optional)
        # Có thể bỏ qua nếu không cần icon
        print(f"💡 Bạn có thể thêm file {icon_path} để có icon đẹp hơn")
        return None
    return icon_path

def build_exe():
    """Build file executable"""
    print(f"\n🔨 Bắt đầu build {APP_NAME}...")
    
    # Tạo icon (optional)
    icon_path = create_icon()
    if icon_path:
        PYINSTALLER_ARGS.extend(["--icon", icon_path])
    
    # Sử dụng PyInstaller từ virtual environment nếu có
    pyinstaller_exe = get_pyinstaller_executable()
    
    # Chạy PyInstaller
    cmd = [pyinstaller_exe] + PYINSTALLER_ARGS + [MAIN_SCRIPT]
    print(f"📝 Lệnh build: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build thành công!")
        if result.stdout:
            print("📋 Output:")
            print(result.stdout[-500:])  # Hiển thị 500 ký tự cuối
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Lỗi khi build:")
        if e.stdout:
            print("📋 STDOUT:")
            print(e.stdout[-1000:])  # Hiển thị 1000 ký tự cuối
        if e.stderr:
            print("❌ STDERR:")
            print(e.stderr[-1000:])  # Hiển thị 1000 ký tự cuối
        return False

def post_build_tasks():
    """Các tác vụ sau khi build"""
    print("\n📋 Thực hiện các tác vụ sau build...")
    
    exe_path = Path(DIST_DIR) / f"{APP_NAME}.exe"
    
    if exe_path.exists():
        # Hiển thị thông tin file exe
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"📄 File exe: {exe_path}")
        print(f"📏 Size: {size_mb:.1f} MB")
        
        # Copy các file cần thiết
        docs_to_copy = ["README.md", "DELETE_MULTIPLE_ITEMS.md", "BUILD_GUIDE.md"]
        for doc in docs_to_copy:
            if os.path.exists(doc):
                shutil.copy2(doc, DIST_DIR)
                print(f"📋 Đã copy {doc}")
        
        # Tạo batch file để chạy exe
        batch_content = f"""@echo off
title {APP_NAME}
echo Starting {APP_NAME}...
"{APP_NAME}.exe"
pause
"""
        batch_path = Path(DIST_DIR) / f"Run_{APP_NAME}.bat"
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        print(f"⚡ Đã tạo {batch_path}")
        
        print(f"\n🎉 Build hoàn thành!")
        print(f"📂 Thư mục output: {Path(DIST_DIR).absolute()}")
        print(f"🚀 Chạy: {exe_path}")
        
        return True
    else:
        print("❌ Không tìm thấy file exe sau khi build")
        return False

def main():
    """Hàm chính"""
    print("=" * 60)
    print("🔧 BUILD SCRIPT - Advanced Text Editor Tool")
    print("=" * 60)
    
    # Kiểm tra yêu cầu
    if not check_requirements():
        print("\n❌ Kiểm tra yêu cầu thất bại")
        input("Nhấn Enter để thoát...")
        return False
    
    # Hỏi người dùng có muốn tiếp tục không
    response = input("\n❓ Bạn có muốn tiếp tục build? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("⏹️ Đã hủy build")
        return False
    
    # Cài đặt dependencies
    if not install_dependencies():
        print("\n❌ Cài đặt dependencies thất bại")
        input("Nhấn Enter để thoát...")
        return False
    
    # Dọn dẹp
    clean_build_dirs()
    
    # Build
    if not build_exe():
        print("\n❌ Build thất bại")
        input("Nhấn Enter để thoát...")
        return False
    
    # Post-build tasks
    if not post_build_tasks():
        print("\n❌ Post-build tasks thất bại")
        input("Nhấn Enter để thoát...")
        return False
    
    print("\n" + "=" * 60)
    print("🎊 BUILD HOÀN THÀNH THÀNH CÔNG!")
    print("=" * 60)
    
    # Hỏi có muốn chạy thử exe không
    response = input("\n❓ Bạn có muốn chạy thử file exe? (y/N): ").lower().strip()
    if response in ['y', 'yes']:
        exe_path = Path(DIST_DIR) / f"{APP_NAME}.exe"
        try:
            subprocess.Popen([str(exe_path)])
            print(f"🚀 Đã khởi chạy {exe_path}")
        except Exception as e:
            print(f"❌ Lỗi khi chạy exe: {e}")
    
    input("\nNhấn Enter để thoát...")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Build đã bị hủy bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi không mong đợi: {e}")
        input("Nhấn Enter để thoát...")