@echo off
title Quick Build - Advanced Text Editor

echo 🚀 QUICK BUILD - Advanced Text Editor Tool
echo.

:: Tự động build mà không hỏi
echo y | python build_exe.py

if exist "dist\AdvancedTextEditor.exe" (
    echo.
    echo ✅ Build thành công!
    echo 📂 File exe: dist\AdvancedTextEditor.exe
    echo.
    
    :: Hỏi có muốn chạy thử không
    set /p choice="❓ Chạy thử file exe? (y/N): "
    if /i "%choice%"=="y" (
        start "" "dist\AdvancedTextEditor.exe"
    )
    
    :: Hỏi có muốn mở thư mục dist không  
    set /p choice="❓ Mở thư mục dist? (y/N): "
    if /i "%choice%"=="y" (
        explorer "dist"
    )
) else (
    echo.
    echo ❌ Build thất bại!
)

pause