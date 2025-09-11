@echo off
echo =====================================
echo    Text Editor Tool - Python Finder
echo =====================================
echo.

echo Dang tim Python tren he thong...

:: Thử các đường dẫn Python phổ biến
set "PYTHON_PATHS=python.exe py.exe C:\Python311\python.exe C:\Python310\python.exe C:\Python39\python.exe C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"

set "PYTHON_FOUND="

for %%i in (%PYTHON_PATHS%) do (
    %%i --version >nul 2>&1
    if !errorlevel! equ 0 (
        echo Tim thay Python: %%i
        set "PYTHON_FOUND=%%i"
        goto :found
    )
)

echo.
echo ❌ KHONG TIM THAY PYTHON!
echo.
echo Vui long cai dat Python tu:
echo https://www.python.org/downloads/
echo.
echo Luu y: PHAI TICK "Add Python to PATH" khi cai dat!
echo.
pause
exit /b 1

:found
echo ✅ Python da san sang!
echo.
echo Chon phien ban:
echo 1. Phien ban co ban (text_editor_tool.py)
echo 2. Phien ban nang cao (advanced_text_editor.py)
echo.
set /p choice="Nhap lua chon (1 hoac 2): "

if "%choice%"=="1" (
    echo Starting Basic Text Editor Tool...
    "%PYTHON_FOUND%" text_editor_tool.py
) else if "%choice%"=="2" (
    echo Starting Advanced Text Editor Tool...
    "%PYTHON_FOUND%" advanced_text_editor.py
) else (
    echo Lua chon khong hop le!
    pause
    exit /b 1
)

if %errorlevel% neq 0 (
    echo.
    echo ❌ Co loi xay ra khi chay tool!
    echo Vui long kiem tra file log ben tren.
)

pause
