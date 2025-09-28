#!/bin/bash

# Build script cho Linux/macOS

echo "======================================================"
echo "         BUILD ADVANCED TEXT EDITOR TOOL"
echo "======================================================"
echo

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được tìm thấy!"
    echo "💡 Vui lòng cài đặt Python3"
    exit 1
fi

# Kiểm tra pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 không được tìm thấy!"
    echo "💡 Vui lòng cài đặt pip3"
    exit 1
fi

echo "🔨 Đang chạy build script..."
echo

# Chạy build script với Python3
python3 build_exe.py

# Kiểm tra kết quả
if [ $? -ne 0 ]; then
    echo
    echo "❌ Build thất bại!"
    read -p "Nhấn Enter để thoát..."
    exit 1
fi

echo
echo "✅ Build script hoàn thành!"
read -p "Nhấn Enter để thoát..."