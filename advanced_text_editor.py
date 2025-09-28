import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
import os
import shutil
from datetime import datetime

class AdvancedTextEditorTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text Editor Tool - Công cụ chỉnh sửa file mô tả item")
        self.root.geometry("1400x900")
        
        # Dữ liệu file
        self.file_path = ""
        self.data = []  # List các dictionary chứa id, raw_content, display_content, color_codes
        self.original_data = []  # Backup dữ liệu gốc
        self.other_lines = []  # List các dòng khác (comment, metadata, etc.)
        self.modified = False
        
        # Khởi tạo các biến UI trước khi setup UI
        self.show_color_var = tk.BooleanVar()
        self.show_colors_var = tk.BooleanVar(value=True)
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Tạo menu
        self.create_menu()
        
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(1, weight=1)
        
        # Frame buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        ttk.Button(button_frame, text="📁 Mở File", command=self.open_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="💾 Lưu File", command=self.save_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="➕ Thêm Item", command=self.add_new_item).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="�️ Xóa nhiều Item", command=self.delete_multiple_items).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="�🔍 Tìm kiếm", command=self.search_item).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🔄 Làm mới", command=self.refresh_all).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📝 Xem dòng khác", command=self.show_other_lines).pack(side=tk.LEFT, padx=(0, 10))
        
        # Separator
        ttk.Separator(button_frame, orient='vertical').pack(side=tk.LEFT, padx=10, fill='y')
        
        # Label hiển thị trạng thái
        self.status_frame = ttk.Frame(button_frame)
        self.status_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        self.file_label = ttk.Label(self.status_frame, text="Chưa mở file nào")
        self.file_label.pack(anchor=tk.W)
        
        self.status_label = ttk.Label(self.status_frame, text="", foreground="green")
        self.status_label.pack(anchor=tk.W)
        
        # Frame danh sách items (bên trái)
        list_frame = ttk.LabelFrame(main_frame, text="📋 Danh sách Items", padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Frame tìm kiếm nhanh
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Tìm:").grid(row=0, column=0, padx=(0, 5))
        self.filter_var = tk.StringVar()
        self.filter_entry = ttk.Entry(search_frame, textvariable=self.filter_var)
        self.filter_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.filter_var.trace('w', self.filter_items)
        
        
        # Treeview cho danh sách items với khả năng chọn nhiều item
        self.tree = ttk.Treeview(list_frame, columns=("ID", "Preview"), show="headings", height=20, selectmode='extended')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Preview", text="Nội dung (preview)")
        self.tree.column("ID", width=80)
        self.tree.column("Preview", width=250)
        
        # Scrollbar cho treeview
        tree_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        self.tree.bind('<Double-1>', self.on_item_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)  # Right click
        
        # Tạo context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="🗑️ Xóa item đã chọn", command=self.delete_selected_items)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✅ Chọn tất cả", command=self.select_all_items)
        self.context_menu.add_command(label="❌ Bỏ chọn tất cả", command=self.deselect_all_items)
        
        # Frame chỉnh sửa (bên phải)
        edit_frame = ttk.LabelFrame(main_frame, text="✏️ Chỉnh sửa nội dung", padding="5")
        edit_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        edit_frame.columnconfigure(0, weight=1)
        edit_frame.rowconfigure(2, weight=1)
        
        # Thông tin item hiện tại
        info_frame = ttk.Frame(edit_frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="ID:").grid(row=0, column=0, sticky=tk.W)
        self.current_id_label = ttk.Label(info_frame, text="", font=("Arial", 12, "bold"))
        self.current_id_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(info_frame, text="Mã màu:").grid(row=1, column=0, sticky=tk.W)
        self.color_codes_label = ttk.Label(info_frame, text="", foreground="blue")
        self.color_codes_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Checkbox hiển thị mã màu
        self.show_color_check = ttk.Checkbutton(
            info_frame, 
            text="Hiển thị mã màu trong editor", 
            variable=self.show_color_var,
            command=self.toggle_color_display
        )
        self.show_color_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Checkbox hiển thị màu sắc
        self.show_colors_check = ttk.Checkbutton(
            info_frame, 
            text="Hiển thị màu sắc thực tế", 
            variable=self.show_colors_var,
            command=self.toggle_color_display
        )
        self.show_colors_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(2, 0))
        
        # Buttons cho việc chỉnh sửa
        edit_button_frame = ttk.Frame(edit_frame)
        edit_button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(edit_button_frame, text="✅ Cập nhật", command=self.update_item).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(edit_button_frame, text="❌ Hủy thay đổi", command=self.cancel_changes).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(edit_button_frame, text="📋 Copy", command=self.copy_content).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(edit_button_frame, text="📄 Paste", command=self.paste_content).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(edit_button_frame, text="🎨 Chọn màu", command=self.show_color_picker).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(edit_button_frame, text="🗑️ Xóa Item", command=self.delete_item).pack(side=tk.LEFT)
        
        # Text editor với line numbers
        editor_frame = ttk.Frame(edit_frame)
        editor_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        editor_frame.columnconfigure(1, weight=1)
        editor_frame.rowconfigure(0, weight=1)
        
        # Line numbers
        self.line_numbers = tk.Text(editor_frame, width=4, padx=5, takefocus=0,
                                  border=0, background='lightgray', state='disabled')
        self.line_numbers.grid(row=0, column=0, sticky=(tk.N, tk.S))
        
        # Text editor với hỗ trợ màu sắc
        self.text_editor = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, 
                                                   width=60, height=25, undo=True)
        self.text_editor.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình các tag màu sắc
        self.setup_color_tags()
        
        # Bind events cho text editor
        self.text_editor.bind('<KeyRelease>', self.on_text_change)
        self.text_editor.bind('<Button-1>', self.on_text_change)
        self.text_editor.bind('<MouseWheel>', self.on_scroll)
        
        # Biến lưu trữ item đang chỉnh sửa
        self.current_editing_index = -1
        
        # Thiết lập phím tắt
        self.setup_keyboard_shortcuts()
        
        # Update line numbers initially
        self.update_line_numbers()
    
    def setup_keyboard_shortcuts(self):
        """Thiết lập các phím tắt"""
        # Phím Delete để xóa item đã chọn
        self.root.bind('<Delete>', self.on_delete_key)
        self.root.bind('<Control-d>', self.on_delete_key)  # Ctrl+D để xóa
        
        # Ctrl+A để chọn tất cả
        self.root.bind('<Control-a>', self.on_select_all_key)
        
        # Escape để bỏ chọn
        self.root.bind('<Escape>', self.on_escape_key)
    
    def on_delete_key(self, event):
        """Xử lý phím Delete và Ctrl+D"""
        # Kiểm tra xem focus có đang ở treeview không
        if self.root.focus_get() == self.tree or self.tree.focus():
            selected_items = self.tree.selection()
            if selected_items:
                self.delete_selected_items()
        return "break"
    
    def on_select_all_key(self, event):
        """Xử lý Ctrl+A"""
        # Kiểm tra xem focus có đang ở treeview không
        if self.root.focus_get() == self.tree or self.tree.focus():
            self.select_all_items()
            return "break"
    
    def on_escape_key(self, event):
        """Xử lý phím Escape"""
        # Nếu đang ở treeview, bỏ chọn tất cả
        if self.root.focus_get() == self.tree or self.tree.focus():
            self.deselect_all_items()
            return "break"
    
    def setup_color_tags(self):
        """Thiết lập các tag màu sắc cho text editor"""
        # Một số màu mặc định
        default_colors = {
            'ffffff': '#ffffff',  # trắng
            '000000': '#000000',  # đen
            'ff0000': '#ff0000',  # đỏ
            '00ff00': '#00ff00',  # xanh lá
            '0000ff': '#0000ff',  # xanh dương
            'ffff00': '#ffff00',  # vàng
            'ff00ff': '#ff00ff',  # tím
            '00ffff': '#00ffff',  # cyan
            'ffcb4a': '#ffcb4a',  # vàng cam
            '6cfb4b': '#6cfb4b',  # xanh lá nhạt
            '0090ff': '#0090ff',  # xanh dương nhạt
        }
        
        for color_code, hex_color in default_colors.items():
            self.text_editor.tag_configure(f"color_{color_code}", foreground=hex_color)
    
    def hex_to_color(self, hex_code):
        """Chuyển đổi hex code thành màu"""
        if len(hex_code) == 6:
            return f"#{hex_code}"
        return "#000000"  # mặc định màu đen
    
    def apply_colors_to_text(self, content):
        """Áp dụng màu sắc cho text trong editor"""
        # Xóa tất cả tags cũ
        for tag in self.text_editor.tag_names():
            if tag.startswith("color_"):
                self.text_editor.tag_delete(tag)
        
        # Tìm tất cả mã màu và vị trí của chúng
        color_pattern = r'\^([0-9a-fA-F]{6})'
        matches = list(re.finditer(color_pattern, content))
        
        if not matches:
            return
        
        # Áp dụng màu từ cuối về đầu để không làm thay đổi vị trí
        for i in range(len(matches) - 1, -1, -1):
            match = matches[i]
            color_code = match.group(1).lower()
            start_pos = match.end()  # Vị trí sau mã màu
            
            # Tìm vị trí kết thúc (mã màu tiếp theo hoặc cuối text)
            if i < len(matches) - 1:
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(content)
            
            # Chuyển đổi vị trí thành format tkinter (line.column)
            text_before_start = content[:start_pos]
            lines_before = text_before_start.count('\n')
            if lines_before == 0:
                col_start = start_pos
            else:
                col_start = start_pos - text_before_start.rfind('\n') - 1
            
            text_before_end = content[:end_pos]
            lines_before_end = text_before_end.count('\n')
            if lines_before_end == 0:
                col_end = end_pos
            else:
                col_end = end_pos - text_before_end.rfind('\n') - 1
            
            start_index = f"{lines_before + 1}.{col_start}"
            end_index = f"{lines_before_end + 1}.{col_end}"
            
            # Tạo tag và áp dụng màu
            tag_name = f"color_{color_code}"
            hex_color = self.hex_to_color(color_code)
            
            self.text_editor.tag_configure(tag_name, foreground=hex_color)
            self.text_editor.tag_add(tag_name, start_index, end_index)
    
    def create_menu(self):
        """Tạo menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Mở File...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Lưu", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Lưu thành...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.on_closing)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Thêm Item mới...", command=self.add_new_item, accelerator="Ctrl+N")
        edit_menu.add_separator()
        edit_menu.add_command(label="Tìm kiếm...", command=self.search_item, accelerator="Ctrl+F")
        edit_menu.add_command(label="Tìm và thay thế...", command=self.find_replace)
        edit_menu.add_separator()
        edit_menu.add_command(label="Copy", command=self.copy_content, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_content, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Chọn màu...", command=self.show_color_picker, accelerator="Ctrl+M")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Hiển thị mã màu", variable=self.show_color_var, 
                                command=self.toggle_color_display)
        view_menu.add_checkbutton(label="Hiển thị màu sắc thực tế", variable=self.show_colors_var, 
                                command=self.toggle_color_display)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-f>', lambda e: self.search_item())
        self.root.bind('<Control-n>', lambda e: self.add_new_item())
        self.root.bind('<Control-m>', lambda e: self.show_color_picker())
    
    def parse_line(self, line):
        """Phân tích một dòng trong file txt"""
        line = line.strip()
        if not line:
            return None
            
        # Tìm tab đầu tiên để tách ID và content
        tab_index = line.find('\t')
        if tab_index == -1:
            return None
            
        try:
            item_id = line[:tab_index].strip()
            content_part = line[tab_index+1:].strip()
            
            # Loại bỏ dấu ngoặc kép bao quanh
            if content_part.startswith('"') and content_part.endswith('"'):
                content_part = content_part[1:-1]
            
            # Trích xuất mã màu
            color_codes = re.findall(r'\^[0-9a-fA-F]{6}', content_part)
            
            # Chuyển đổi nội dung để hiển thị
            display_content = self.convert_to_display(content_part)
            
            return {
                'id': item_id,
                'raw_content': content_part,
                'display_content': display_content,
                'color_codes': color_codes
            }
        except:
            return None
    
    def convert_to_display(self, raw_content):
        """Chuyển đổi nội dung raw thành nội dung hiển thị với màu sắc"""
        # Chuyển \r thành xuống dòng thật
        content = raw_content.replace('\\r', '\n')
        return content
    
    def convert_to_display_with_colors(self, raw_content):
        """Chuyển đổi nội dung raw thành nội dung hiển thị có mã màu"""
        # Chỉ chuyển \r thành xuống dòng, giữ nguyên mã màu
        content = raw_content.replace('\\r', '\n')
        return content
    
    def convert_to_raw(self, display_content, original_raw=None):
        """Chuyển nội dung hiển thị về dạng raw"""
        if self.show_color_var.get() and original_raw:
            # Nếu đang hiển thị mã màu, cần xử lý để giữ nguyên vị trí mã màu
            content = display_content.replace('\n', '\\r')
            return content
        else:
            # Chỉ chuyển xuống dòng thành \r
            content = display_content.replace('\n', '\\r')
            
            # Nếu có mã màu gốc, cần ghép lại
            if original_raw and self.current_editing_index >= 0:
                original_item = self.data[self.current_editing_index]
                if original_item['color_codes']:
                    # Logic phức tạp để ghép lại mã màu - tạm thời giữ nguyên
                    return original_raw.replace('\\r', '\n').replace('\n', '\\r')
            
            return content
    
    def detect_encoding(self, file_path):
        """Tự động phát hiện encoding của file"""
        # Thử sử dụng chardet nếu có
        try:
            import chardet
            # Đọc một phần file để phát hiện encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Đọc 10KB đầu
                result = chardet.detect(raw_data)
                if result['confidence'] > 0.7:
                    return result['encoding']
        except ImportError:
            pass  # chardet không có, sử dụng fallback
        except:
            pass
        
        # Fallback: thử các encoding phổ biến
        encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'utf-16le', 'utf-16be', 'gbk', 'gb2312', 'big5', 'cp1252', 'latin1', 'ascii']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read(1000)  # Đọc thử 1000 ký tự đầu
                return encoding
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        # Nếu không phát hiện được, sử dụng utf-8 với errors='replace'
        return 'utf-8'
    
    def open_file(self):
        """Mở file txt"""
        if self.modified:
            result = messagebox.askyesnocancel(
                "Lưu thay đổi?", 
                "Có thay đổi chưa được lưu. Bạn có muốn lưu trước khi mở file mới?"
            )
            if result is True:
                self.save_file()
            elif result is None:
                return
        
        file_path = filedialog.askopenfilename(
            title="Chọn file txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            # Phát hiện encoding
            detected_encoding = self.detect_encoding(file_path)
            
            self.data = []
            self.other_lines = []
            
            with open(file_path, 'r', encoding=detected_encoding, errors='replace') as f:
                for line_num, line in enumerate(f, 1):
                    parsed = self.parse_line(line)
                    if parsed:
                        # Thêm số dòng gốc để duy trì thứ tự
                        parsed['original_line_number'] = line_num
                        self.data.append(parsed)
                    else:
                        # Lưu các dòng khác (comment, metadata, empty lines)
                        self.other_lines.append({
                            'line_number': line_num,
                            'content': line.rstrip('\n')
                        })
            
            self.file_path = file_path
            self.original_data = [item.copy() for item in self.data]  # Backup
            self.modified = False
            
            self.file_label.config(text=f"File: {os.path.basename(file_path)}")
            
            other_lines_count = len(self.other_lines)
            self.status_label.config(text=f"Đã tải {len(self.data)} items, {other_lines_count} dòng khác (Encoding: {detected_encoding})", foreground="green")
            
            self.refresh_tree()
            
            # Tự động backup file gốc
            self.create_backup()
            
        except Exception as e:
            error_msg = f"Không thể mở file: {str(e)}\n\n"
            error_msg += "Các nguyên nhân có thể:\n"
            error_msg += "1. File bị hỏng hoặc không đúng định dạng\n"
            error_msg += "2. File đang được sử dụng bởi chương trình khác\n"
            error_msg += "3. Không có quyền truy cập file\n"
            error_msg += "4. Encoding của file không được hỗ trợ"
            messagebox.showerror("Lỗi", error_msg)
    
    def create_backup(self):
        """Tạo file backup"""
        if not self.file_path:
            return
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.file_path}.backup_{timestamp}"
            shutil.copy2(self.file_path, backup_path)
            self.status_label.config(text=f"Backup tạo tại: {os.path.basename(backup_path)}", 
                                   foreground="blue")
        except Exception as e:
            print(f"Không thể tạo backup: {e}")
    
    def refresh_tree(self):
        """Làm mới danh sách items"""
        # Xóa tất cả items hiện tại
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Áp dụng filter
        filter_text = self.filter_var.get().lower()
        
        # Thêm items mới
        for i, item in enumerate(self.data):
            if not filter_text or (filter_text in item['id'].lower() or 
                                 filter_text in item['display_content'].lower()):
                preview = item['display_content'][:60].replace('\n', ' ')
                if len(item['display_content']) > 60:
                    preview += "..."
                
                self.tree.insert("", "end", values=(item['id'], preview), tags=(str(i),))
    
    def filter_items(self, *args):
        """Lọc items theo từ khóa"""
        self.refresh_tree()
    
    def refresh_all(self):
        """Làm mới toàn bộ"""
        self.refresh_tree()
        if self.current_editing_index >= 0:
            self.load_item_to_editor(self.current_editing_index)
    
    def on_item_select(self, event):
        """Xử lý khi chọn một item"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Hiển thị số lượng item đã chọn
        selected_count = len(selection)
        if selected_count > 1:
            self.status_label.config(
                text=f"Đã chọn {selected_count} items", 
                foreground="blue"
            )
        else:
            # Lấy index của item được chọn
            item = self.tree.item(selection[0])
            index = int(item['tags'][0])
            
            self.load_item_to_editor(index)
    
    def on_item_double_click(self, event):
        """Xử lý double click - focus vào text editor"""
        self.text_editor.focus_set()
    
    def load_item_to_editor(self, index):
        """Load item vào editor"""
        if index < 0 or index >= len(self.data):
            return
            
        self.current_editing_index = index
        selected_item = self.data[index]
        
        self.current_id_label.config(text=selected_item['id'])
        self.color_codes_label.config(text=", ".join(selected_item['color_codes']) if selected_item['color_codes'] else "Không có")
        
        # Xóa nội dung cũ và hiển thị nội dung mới
        self.text_editor.delete('1.0', tk.END)
        
        if self.show_color_var.get():
            content = self.convert_to_display_with_colors(selected_item['raw_content'])
        else:
            content = selected_item['display_content']
            
        self.text_editor.insert('1.0', content)
        self.update_line_numbers()
        
        # Áp dụng màu sắc nếu được bật
        if self.show_colors_var.get():
            self.apply_colors_to_text(content)
    
    def toggle_color_display(self):
        """Chuyển đổi hiển thị mã màu và màu sắc"""
        if self.current_editing_index >= 0:
            self.load_item_to_editor(self.current_editing_index)
    
    def on_text_change(self, event=None):
        """Xử lý khi text thay đổi"""
        self.update_line_numbers()
        if not self.modified:
            self.modified = True
            self.root.title(self.root.title() + " *")
    
    def on_scroll(self, event):
        """Đồng bộ scroll giữa line numbers và text editor"""
        self.line_numbers.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"
    
    def update_line_numbers(self):
        """Cập nhật line numbers"""
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        
        line_count = int(self.text_editor.index('end-1c').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count))
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')
    
    def update_item(self):
        """Cập nhật nội dung item hiện tại"""
        if self.current_editing_index == -1:
            messagebox.showwarning("Cảnh báo", "Chưa chọn item nào để chỉnh sửa")
            return
        
        # Lấy nội dung từ text editor
        new_content = self.text_editor.get('1.0', tk.END).rstrip('\n')
        
        # Cập nhật dữ liệu
        item = self.data[self.current_editing_index]
        original_raw = item['raw_content']
        
        if self.show_color_var.get():
            # Nếu đang hiển thị mã màu, new_content đã có mã màu
            item['raw_content'] = new_content.replace('\n', '\\r')
            item['display_content'] = self.convert_to_display(item['raw_content'])
        else:
            # Nếu không hiển thị mã màu, cần ghép lại với mã màu gốc
            item['display_content'] = new_content
            item['raw_content'] = self.convert_to_raw(new_content, original_raw)
        
        # Cập nhật color codes
        item['color_codes'] = re.findall(r'\^[0-9a-fA-F]{6}', item['raw_content'])
        
        # Làm mới tree view
        self.refresh_tree()
        
        # Cập nhật thông tin
        self.color_codes_label.config(text=", ".join(item['color_codes']) if item['color_codes'] else "Không có")
        
        self.status_label.config(text="Đã cập nhật nội dung", foreground="green")
        messagebox.showinfo("Thành công", f"Đã cập nhật item ID: {item['id']}")
    
    def cancel_changes(self):
        """Hủy thay đổi và khôi phục nội dung gốc"""
        if self.current_editing_index == -1:
            return
            
        self.load_item_to_editor(self.current_editing_index)
        self.status_label.config(text="Đã hủy thay đổi", foreground="orange")
    
    def copy_content(self):
        """Copy nội dung"""
        try:
            selected_text = self.text_editor.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
        except tk.TclError:
            # Không có text được chọn, copy toàn bộ
            content = self.text_editor.get('1.0', tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
    
    def paste_content(self):
        """Paste nội dung"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.text_editor.insert(tk.INSERT, clipboard_content)
        except tk.TclError:
            pass  # Clipboard trống
    
    def save_file(self):
        """Lưu file với định dạng gốc và bảo toàn các dòng khác"""
        if not self.file_path:
            self.save_as_file()
            return
        
        try:
            # Phát hiện encoding của file gốc
            detected_encoding = self.detect_encoding(self.file_path)
            
            # Tạo danh sách tất cả các dòng với thứ tự gốc
            all_lines = []
            
            # Thêm các dòng khác vào danh sách
            for other_line in self.other_lines:
                all_lines.append({
                    'line_number': other_line['line_number'],
                    'content': other_line['content'],
                    'type': 'other'
                })
            
            # Thêm các item data vào danh sách
            for item in self.data:
                line_content = f"{item['id']}\t\"{item['raw_content']}\""
                all_lines.append({
                    'line_number': item.get('original_line_number', 9999),
                    'content': line_content,
                    'type': 'item'
                })
            
            # Sắp xếp theo số dòng gốc
            all_lines.sort(key=lambda x: x['line_number'])
            
            # Ghi file
            with open(self.file_path, 'w', encoding=detected_encoding, errors='replace') as f:
                for line_data in all_lines:
                    f.write(line_data['content'] + '\n')
            
            self.modified = False
            self.root.title(self.root.title().rstrip(' *'))
            self.status_label.config(text=f"Đã lưu file (Encoding: {detected_encoding}) - Bảo toàn {len(self.other_lines)} dòng khác", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")
    
    def save_as_file(self):
        """Lưu file với tên mới"""
        file_path = filedialog.asksaveasfilename(
            title="Lưu file thành",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.file_path = file_path
            self.save_file()
            self.file_label.config(text=f"File: {os.path.basename(file_path)}")
    
    def search_item(self):
        """Tìm kiếm item theo ID hoặc nội dung"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm kiếm")
        search_window.geometry("500x200")
        search_window.transient(self.root)
        search_window.grab_set()
        
        # Center the window
        search_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        frame = ttk.Frame(search_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Tìm kiếm theo ID hoặc nội dung:").pack(pady=(0, 10))
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(frame, textvariable=search_var, width=50)
        search_entry.pack(pady=(0, 10))
        search_entry.focus()
        
        # Options
        options_frame = ttk.Frame(frame)
        options_frame.pack(pady=(0, 20))
        
        case_sensitive_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Phân biệt hoa thường", variable=case_sensitive_var).pack(side=tk.LEFT)
        
        def do_search():
            query = search_var.get().strip()
            if not query:
                return
            
            case_sensitive = case_sensitive_var.get()
            if not case_sensitive:
                query = query.lower()
            
            # Tìm kiếm
            for i, item in enumerate(self.data):
                id_text = item['id'] if case_sensitive else item['id'].lower()
                content_text = item['display_content'] if case_sensitive else item['display_content'].lower()
                
                if query in id_text or query in content_text:
                    # Tìm item trong tree và chọn
                    children = self.tree.get_children()
                    for child in children:
                        child_item = self.tree.item(child)
                        if child_item['tags'] and int(child_item['tags'][0]) == i:
                            self.tree.selection_set(child)
                            self.tree.see(child)
                            self.load_item_to_editor(i)
                            search_window.destroy()
                            return
            
            messagebox.showinfo("Kết quả", "Không tìm thấy item nào phù hợp")
        
        button_frame = ttk.Frame(frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="Tìm", command=do_search).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Hủy", command=search_window.destroy).pack(side=tk.LEFT)
        
        # Bind Enter key
        search_entry.bind('<Return>', lambda e: do_search())
    
    def find_replace(self):
        """Tìm và thay thế"""
        # Tính năng tìm và thay thế nâng cao
        messagebox.showinfo("Thông báo", "Tính năng này sẽ được phát triển trong phiên bản tiếp theo")
    
    def on_closing(self):
        """Xử lý khi đóng ứng dụng"""
        if self.modified:
            result = messagebox.askyesnocancel(
                "Lưu thay đổi?", 
                "Có thay đổi chưa được lưu. Bạn có muốn lưu trước khi thoát?"
            )
            if result is True:
                self.save_file()
            elif result is None:
                return
        
        self.root.destroy()

    def add_new_item(self):
        """Thêm item mới"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm Item Mới")
        add_window.geometry("700x600")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Center the window
        add_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        main_frame = ttk.Frame(add_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # ID input
        id_frame = ttk.Frame(main_frame)
        id_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        id_frame.columnconfigure(1, weight=1)
        
        ttk.Label(id_frame, text="ID:").grid(row=0, column=0, sticky="w")
        id_var = tk.StringVar()
        id_entry = ttk.Entry(id_frame, textvariable=id_var, width=20)
        id_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        id_entry.focus()
        
        # Auto generate ID button
        def auto_generate_id():
            if self.data:
                max_id = max(int(item['id']) for item in self.data if item['id'].isdigit())
                new_id = str(max_id + 1)
            else:
                new_id = "70001"
            id_var.set(new_id)
        
        ttk.Button(id_frame, text="Auto ID", command=auto_generate_id).grid(row=0, column=2, padx=(10, 0))
        
        # Color toolbar
        color_frame = ttk.LabelFrame(main_frame, text="Màu sắc nhanh", padding="10")
        color_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        quick_colors = [
            ("🔴", "ff0000"), ("🟢", "00ff00"), ("🔵", "0000ff"), ("🟡", "ffff00"),
            ("🟣", "ff00ff"), ("🔷", "00ffff"), ("⚪", "ffffff"), ("⚫", "000000")
        ]
        
        for i, (emoji, hex_code) in enumerate(quick_colors):
            btn = tk.Button(
                color_frame,
                text=emoji,
                bg=f"#{hex_code}",
                fg="white" if hex_code in ["000000", "0000ff"] else "black",
                width=3,
                command=lambda code=hex_code: self.insert_color_in_add_window(content_text, code)
            )
            btn.grid(row=0, column=i, padx=2)
        
        ttk.Button(color_frame, text="🎨 Thêm màu...", 
                  command=lambda: self.show_color_picker_for_window(content_text)).grid(row=0, column=len(quick_colors), padx=(10, 0))
        
        # Content input
        ttk.Label(main_frame, text="Nội dung:").grid(row=3, column=0, sticky="nw", pady=(10, 5))
        
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=4, column=0, sticky="nsew", pady=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        content_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, height=20)
        content_text.grid(row=0, column=0, sticky="nsew")
        
        # Preview với màu sắc
        preview_var = tk.BooleanVar(value=True)
        preview_check = ttk.Checkbutton(main_frame, text="Xem trước với màu sắc", variable=preview_var,
                                       command=lambda: self.apply_colors_to_text_widget(content_text, preview_var.get()))
        preview_check.grid(row=5, column=0, sticky="w", pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, sticky="ew")
        
        def add_item():
            new_id = id_var.get().strip()
            new_content = content_text.get('1.0', tk.END).rstrip('\n')
            
            if not new_id:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID")
                return
            
            if not new_content:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung")
                return
            
            # Kiểm tra ID đã tồn tại chưa
            for item in self.data:
                if item['id'] == new_id:
                    messagebox.showwarning("Cảnh báo", f"ID {new_id} đã tồn tại")
                    return
            
            # Tạo item mới
            raw_content = new_content.replace('\n', '\\r')
            color_codes = re.findall(r'\^[0-9a-fA-F]{6}', raw_content)
            
            # Tìm số dòng mới (sau dòng cuối cùng)
            max_line_number = 0
            if self.data:
                max_line_number = max(item.get('original_line_number', 0) for item in self.data)
            if self.other_lines:
                max_line_number = max(max_line_number, max(line['line_number'] for line in self.other_lines))
            
            new_item = {
                'id': new_id,
                'raw_content': raw_content,
                'display_content': new_content,
                'color_codes': color_codes,
                'original_line_number': max_line_number + 1
            }
            
            self.data.append(new_item)
            self.refresh_tree()
            
            messagebox.showinfo("Thành công", f"Đã thêm item ID: {new_id}")
            add_window.destroy()
        
        ttk.Button(button_frame, text="✅ Thêm", command=add_item).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Hủy", command=add_window.destroy).pack(side=tk.LEFT)
        
        # Bind events
        content_text.bind('<KeyRelease>', lambda e: self.apply_colors_to_text_widget(content_text, preview_var.get()) if preview_var.get() else None)
    
    def insert_color_in_add_window(self, text_widget, hex_code):
        """Chèn mã màu vào text widget"""
        color_code = f"^{hex_code}"
        cursor_pos = text_widget.index(tk.INSERT)
        text_widget.insert(cursor_pos, color_code)
        text_widget.focus_set()
    
    def apply_colors_to_text_widget(self, text_widget, apply_colors):
        """Áp dụng màu sắc cho text widget bất kỳ"""
        if not apply_colors:
            # Xóa tất cả tags màu
            for tag in text_widget.tag_names():
                if tag.startswith("color_"):
                    text_widget.tag_delete(tag)
            return
        
        content = text_widget.get('1.0', tk.END)
        
        # Xóa tất cả tags cũ
        for tag in text_widget.tag_names():
            if tag.startswith("color_"):
                text_widget.tag_delete(tag)
        
        # Tìm tất cả mã màu và vị trí của chúng
        color_pattern = r'\^([0-9a-fA-F]{6})'
        matches = list(re.finditer(color_pattern, content))
        
        if not matches:
            return
        
        # Áp dụng màu từ cuối về đầu để không làm thay đổi vị trí
        for i in range(len(matches) - 1, -1, -1):
            match = matches[i]
            color_code = match.group(1).lower()
            start_pos = match.end()  # Vị trí sau mã màu
            
            # Tìm vị trí kết thúc (mã màu tiếp theo hoặc cuối text)
            if i < len(matches) - 1:
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(content)
            
            # Chuyển đổi vị trí thành format tkinter (line.column)
            text_before_start = content[:start_pos]
            lines_before = text_before_start.count('\n')
            if lines_before == 0:
                col_start = start_pos
            else:
                col_start = start_pos - text_before_start.rfind('\n') - 1
            
            text_before_end = content[:end_pos]
            lines_before_end = text_before_end.count('\n')
            if lines_before_end == 0:
                col_end = end_pos
            else:
                col_end = end_pos - text_before_end.rfind('\n') - 1
            
            start_index = f"{lines_before + 1}.{col_start}"
            end_index = f"{lines_before_end + 1}.{col_end}"
            
            # Tạo tag và áp dụng màu
            tag_name = f"color_{color_code}"
            hex_color = self.hex_to_color(color_code)
            
            text_widget.tag_configure(tag_name, foreground=hex_color)
            text_widget.tag_add(tag_name, start_index, end_index)
    
    def delete_item(self):
        """Xóa item hiện tại"""
        if self.current_editing_index == -1:
            messagebox.showwarning("Cảnh báo", "Chưa chọn item nào để xóa")
            return
        
        item = self.data[self.current_editing_index]
        result = messagebox.askyesno(
            "Xác nhận xóa", 
            f"Bạn có chắc muốn xóa item ID: {item['id']}?"
        )
        
        if result:
            self.data.pop(self.current_editing_index)
            self.current_editing_index = -1
            self.current_id_label.config(text="")
            self.color_codes_label.config(text="")
            self.text_editor.delete('1.0', tk.END)
            self.refresh_tree()
            self.status_label.config(text="Đã xóa item", foreground="orange")
    
    def delete_multiple_items(self):
        """Xóa nhiều item từ button"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Chưa chọn item nào để xóa.\nVui lòng chọn một hoặc nhiều item từ danh sách.")
            return
        
        self.delete_selected_items()
    
    def delete_selected_items(self):
        """Xóa các item đã được chọn trong treeview"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Chưa chọn item nào để xóa")
            return
        
        # Lấy thông tin các item sẽ bị xóa
        items_to_delete = []
        for selected_item in selected_items:
            item_data = self.tree.item(selected_item)
            item_id = item_data['values'][0]
            items_to_delete.append(item_id)
        
        # Hiển thị dialog xác nhận
        if len(items_to_delete) == 1:
            message = f"Bạn có chắc muốn xóa item ID: {items_to_delete[0]}?"
        else:
            items_list = ", ".join(str(item_id) for item_id in items_to_delete)
            message = f"Bạn có chắc muốn xóa {len(items_to_delete)} items?\nID: {items_list}"
        
        result = messagebox.askyesno("Xác nhận xóa", message)
        
        if result:
            # Xóa các item từ data (xóa theo index giảm dần để tránh lỗi index)
            indices_to_delete = []
            for item_id in items_to_delete:
                for i, data_item in enumerate(self.data):
                    if str(data_item['id']) == str(item_id):
                        indices_to_delete.append(i)
                        break
            
            # Sắp xếp indices giảm dần để xóa từ cuối lên đầu
            indices_to_delete.sort(reverse=True)
            
            for index in indices_to_delete:
                self.data.pop(index)
            
            # Reset trạng thái editor nếu item đang chỉnh sửa bị xóa
            if self.current_editing_index in indices_to_delete:
                self.current_editing_index = -1
                self.current_id_label.config(text="")
                self.color_codes_label.config(text="")
                self.text_editor.delete('1.0', tk.END)
            
            # Refresh tree và hiển thị thông báo
            self.refresh_tree()
            count = len(items_to_delete)
            self.status_label.config(
                text=f"Đã xóa {count} item{'s' if count > 1 else ''}", 
                foreground="orange"
            )
            self.modified = True
    
    def show_context_menu(self, event):
        """Hiển thị context menu khi click chuột phải"""
        # Chọn item tại vị trí click nếu chưa được chọn
        item = self.tree.identify_row(event.y)
        if item:
            # Nếu item chưa được chọn, chọn nó
            if item not in self.tree.selection():
                self.tree.selection_set(item)
            
            # Hiển thị menu
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def select_all_items(self):
        """Chọn tất cả items trong danh sách"""
        all_items = self.tree.get_children()
        self.tree.selection_set(all_items)
    
    def deselect_all_items(self):
        """Bỏ chọn tất cả items"""
        self.tree.selection_remove(self.tree.selection())
    
    def show_color_picker(self):
        """Hiển thị bảng chọn màu cho text editor chính"""
        self.show_color_picker_for_window(self.text_editor)
    
    def show_color_picker_for_window(self, target_text_widget):
        """Hiển thị bảng chọn màu cho text widget cụ thể"""
        color_window = tk.Toplevel(self.root)
        color_window.title("Chọn Màu")
        color_window.geometry("500x400")
        color_window.transient(self.root)
        color_window.grab_set()
        
        # Center the window
        color_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        main_frame = ttk.Frame(color_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Chọn màu để chèn vào vị trí cursor:", font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Bảng màu chính
        colors_frame = ttk.LabelFrame(main_frame, text="Màu cơ bản", padding="10")
        colors_frame.pack(fill=tk.X, pady=(0, 15))
        
        colors = [
            ("🔴 Đỏ", "ff0000"),
            ("🟢 Xanh lá", "00ff00"), 
            ("🔵 Xanh dương", "0000ff"),
            ("🟡 Vàng", "ffff00"),
            ("🟣 Tím", "ff00ff"),
            ("🔷 Cyan", "00ffff"),
            ("⚪ Trắng", "ffffff"),
            ("⚫ Đen", "000000"),
            ("🟠 Cam", "ff8000"),
            ("🍀 Xanh lá nhạt", "6cfb4b"),
            ("🔹 Xanh dương nhạt", "0090ff"),
            ("🌟 Vàng cam", "ffcb4a"),
            ("🔸 Xám", "888888"),
            ("💎 Bạc", "c0c0c0"),
            ("🟤 Nâu", "8b4513"),
            ("💖 Hồng", "ff69b4")
        ]
        
        # Tạo grid 4 cột
        for i, (name, hex_code) in enumerate(colors):
            row = i // 4
            col = i % 4
            
            color_button = tk.Button(
                colors_frame,
                text=name,
                bg=f"#{hex_code}",
                fg="white" if hex_code in ["000000", "0000ff", "8b4513"] else "black",
                width=15,
                height=2,
                command=lambda code=hex_code: self.insert_color_code_to_widget(color_window, target_text_widget, code)
            )
            color_button.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
        
        # Cấu hình grid
        for i in range(4):
            colors_frame.grid_columnconfigure(i, weight=1)
        
        # Custom color input
        custom_frame = ttk.LabelFrame(main_frame, text="Màu tùy chỉnh", padding="10")
        custom_frame.pack(fill=tk.X, pady=(0, 15))
        
        input_frame = ttk.Frame(custom_frame)
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="Nhập mã hex (6 ký tự):").pack(side=tk.LEFT)
        custom_var = tk.StringVar()
        custom_entry = ttk.Entry(input_frame, textvariable=custom_var, width=15)
        custom_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        # Preview color
        preview_label = tk.Label(input_frame, text="Preview", width=10, height=1, relief="solid")
        preview_label.pack(side=tk.LEFT, padx=(10, 10))
        
        def update_preview(*args):
            hex_code = custom_var.get().strip()
            if len(hex_code) == 6 and all(c in '0123456789abcdefABCDEF' for c in hex_code):
                try:
                    preview_label.config(bg=f"#{hex_code}")
                except:
                    preview_label.config(bg="white")
            else:
                preview_label.config(bg="white")
        
        custom_var.trace('w', update_preview)
        
        def insert_custom():
            hex_code = custom_var.get().strip()
            if len(hex_code) == 6 and all(c in '0123456789abcdefABCDEF' for c in hex_code):
                self.insert_color_code_to_widget(color_window, target_text_widget, hex_code.lower())
            else:
                messagebox.showwarning("Lỗi", "Mã hex phải có 6 ký tự (0-9, a-f)")
        
        ttk.Button(input_frame, text="Chèn màu", command=insert_custom).pack(side=tk.LEFT)
        custom_entry.bind('<Return>', lambda e: insert_custom())
        
        # Color palette examples
        palette_frame = ttk.LabelFrame(main_frame, text="Bảng màu game phổ biến", padding="10")
        palette_frame.pack(fill=tk.X)
        
        game_colors = [
            ("Legendary", "ffa500"), ("Epic", "9966cc"), ("Rare", "0099ff"),
            ("Uncommon", "00ff00"), ("Common", "ffffff"), ("Damage", "ff6666")
        ]
        
        for i, (name, hex_code) in enumerate(game_colors):
            btn = tk.Button(
                palette_frame,
                text=name,
                bg=f"#{hex_code}",
                fg="black" if hex_code in ["ffa500", "00ff00", "ffffff"] else "white",
                width=12,
                command=lambda code=hex_code: self.insert_color_code_to_widget(color_window, target_text_widget, code)
            )
            btn.grid(row=0, column=i, padx=2, pady=5)
    
    def insert_color_code_to_widget(self, window, text_widget, hex_code):
        """Chèn mã màu vào text widget cụ thể"""
        color_code = f"^{hex_code}"
        
        # Chèn vào vị trí cursor trong text widget
        cursor_pos = text_widget.index(tk.INSERT)
        text_widget.insert(cursor_pos, color_code)
        
        # Áp dụng màu sắc nếu có thể
        if text_widget == self.text_editor and self.show_colors_var.get():
            content = self.text_editor.get('1.0', tk.END).rstrip('\n')
            self.apply_colors_to_text(content)
        elif text_widget != self.text_editor:
            # Áp dụng màu cho text widget khác
            self.apply_colors_to_text_widget(text_widget, True)
        
        # Focus về text widget
        text_widget.focus_set()
        
        window.destroy()
        self.status_label.config(text=f"Đã chèn mã màu: {color_code}", foreground="green")

    def show_other_lines(self):
        """Hiển thị các dòng khác đã được bảo toàn"""
        if not self.other_lines:
            messagebox.showinfo("Thông tin", "Không có dòng nào khác trong file (chỉ có items)")
            return
        
        other_window = tk.Toplevel(self.root)
        other_window.title("Dòng khác được bảo toàn")
        other_window.geometry("600x400")
        other_window.transient(self.root)
        
        # Center the window
        other_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        main_frame = ttk.Frame(other_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Các dòng khác được bảo toàn ({len(self.other_lines)} dòng):", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Text widget để hiển thị các dòng
        text_widget = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20, width=70)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Hiển thị các dòng
        for other_line in sorted(self.other_lines, key=lambda x: x['line_number']):
            content = other_line['content']
            line_num = other_line['line_number']
            
            # Phân loại dòng
            if content.startswith('//'):
                line_type = "Comment"
            elif content.startswith('#'):
                line_type = "Metadata" 
            elif content.startswith('/*') or content.endswith('*/'):
                line_type = "Block Comment"
            elif content.strip() == '':
                line_type = "Empty"
            else:
                line_type = "Other"
            
            text_widget.insert(tk.END, f"Dòng {line_num:3d} [{line_type:12s}]: {content}\n")
        
        text_widget.config(state='disabled')
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Đóng", command=other_window.destroy).pack(side=tk.RIGHT)
        
        info_text = f"""
ℹ️ Thông tin:
• Tool tự động bảo toàn tất cả dòng không phải item data
• Các dòng này sẽ được giữ nguyên vị trí khi lưu file
• Bao gồm: comment (//, /* */), metadata (#), dòng trống
        """
        ttk.Label(button_frame, text=info_text.strip(), foreground="blue").pack(side=tk.LEFT)

def main():
    root = tk.Tk()
    app = AdvancedTextEditorTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
