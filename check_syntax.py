import ast
import sys

def check_python_syntax(filename):
    """Kiểm tra syntax của file Python"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Compile để kiểm tra syntax
        ast.parse(source_code, filename=filename)
        print(f"✅ {filename}: Syntax OK!")
        return True
        
    except SyntaxError as e:
        print(f"❌ {filename}: Syntax Error!")
        print(f"   Dòng {e.lineno}: {e.text}")
        print(f"   Lỗi: {e.msg}")
        return False
        
    except Exception as e:
        print(f"❌ {filename}: Lỗi khác: {e}")
        return False

if __name__ == "__main__":
    files_to_check = [
        "text_editor_tool.py",
        "advanced_text_editor.py"
    ]
    
    print("🔍 Kiểm tra syntax các file Python...")
    print("=" * 50)
    
    all_ok = True
    for filename in files_to_check:
        ok = check_python_syntax(filename)
        all_ok = all_ok and ok
        print()
    
    if all_ok:
        print("🎉 Tất cả file đều OK! Tool có thể chạy được.")
    else:
        print("⚠️ Có lỗi cần sửa trước khi chạy tool.")
    
    input("\nNhấn Enter để thoát...")
