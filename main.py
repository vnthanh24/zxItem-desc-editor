"""
Advanced Text Editor Tool - Main Entry Point
Đây là file chính để khởi chạy ứng dụng
"""

import tkinter as tk
import sys
import os
from pathlib import Path

# Thêm thư mục hiện tại vào Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from advanced_text_editor import AdvancedTextEditorTool
except ImportError as e:
    print(f"Lỗi import: {e}")
    print("Đảm bảo file advanced_text_editor.py có trong cùng thư mục")
    input("Nhấn Enter để thoát...")
    sys.exit(1)

def main():
    """Hàm main để khởi chạy ứng dụng"""
    try:
        # Tạo root window
        root = tk.Tk()
        
        # Thiết lập icon nếu có
        icon_path = current_dir / "app_icon.ico"
        if icon_path.exists():
            try:
                root.iconbitmap(str(icon_path))
            except:
                pass  # Bỏ qua nếu không load được icon
        
        # Khởi tạo ứng dụng
        app = AdvancedTextEditorTool(root)
        
        # Chạy main loop
        root.mainloop()
        
    except Exception as e:
        print(f"Lỗi khi khởi chạy ứng dụng: {e}")
        input("Nhấn Enter để thoát...")
        sys.exit(1)

if __name__ == "__main__":
    main()