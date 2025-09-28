@echo off
title Build Advanced Text Editor Tool
echo.
echo ====================================================
echo           BUILD ADVANCED TEXT EDITOR TOOL
echo ====================================================
echo.

:: Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo 💡 Vui lòng cài đặt Python và thêm vào PATH
    pause
    exit /b 1
)

:: Chạy build script
echo 🔨 Đang chạy build script...
echo.
python build_exe.py

:: Kiểm tra kết quả
if errorlevel 1 (
    echo.
    echo ❌ Build thất bại!
    pause
    exit /b 1
)

echo.
echo ✅ Build script hoàn thành!
pause