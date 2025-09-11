@echo off
echo =====================================
echo    Text Editor Tool - Item Editor
echo =====================================
echo.
echo Chon phien ban:
echo 1. Phien ban co ban (text_editor_tool.py)
echo 2. Phien ban nang cao (advanced_text_editor.py)
echo.
set /p choice="Nhap lua chon (1 hoac 2): "

if "%choice%"=="1" (
    echo Starting Basic Text Editor Tool...
    python text_editor_tool.py
) else if "%choice%"=="2" (
    echo Starting Advanced Text Editor Tool...
    python advanced_text_editor.py
) else (
    echo Lua chon khong hop le!
    pause
    exit
)

pause
