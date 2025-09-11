import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
import os

class TextEditorTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor Tool - Chỉnh sửa file mô tả item")
        self.root.geometry("1200x800")
        
        # Dữ liệu file
        self.file_path = ""
        self.data = []  # List các dictionary chứa id, raw_content, display_content
        self.other_lines = []  # List các dòng khác (comment, metadata, etc.)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Frame buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        ttk.Button(button_frame, text="📁 Mở File", command=self.open_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="💾 Lưu File", command=self.save_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="➕ Thêm Item", command=self.add_new_item).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🔍 Tìm kiếm", command=self.search_item).pack(side=tk.LEFT, padx=(0, 10))
        
        # Label hiển thị đường dẫn file
        self.file_label = ttk.Label(button_frame, text="Chưa mở file nào")
        self.file_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Frame danh sách items (bên trái)
        list_frame = ttk.LabelFrame(main_frame, text="Danh sách Items", padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview cho danh sách items
        self.tree = ttk.Treeview(list_frame, columns=("ID", "Preview"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Preview", text="Nội dung (preview)")
        self.tree.column("ID", width=100)
        self.tree.column("Preview", width=300)
        
        # Scrollbar cho treeview
        tree_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind event khi chọn item
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        
        # Frame chỉnh sửa (bên phải)
        edit_frame = ttk.LabelFrame(main_frame, text="Chỉnh sửa nội dung", padding="5")
        edit_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        edit_frame.columnconfigure(0, weight=1)
        edit_frame.rowconfigure(1, weight=1)
        
        # ID hiện tại
        id_frame = ttk.Frame(edit_frame)
        id_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Label(id_frame, text="ID:").pack(side=tk.LEFT)
        self.current_id_label = ttk.Label(id_frame, text="", font=("Arial", 10, "bold"))
        self.current_id_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Checkbox hiển thị màu sắc
        self.show_colors_var = tk.BooleanVar(value=True)
        self.show_colors_check = ttk.Checkbutton(
            id_frame, 
            text="Hiển thị màu sắc", 
            variable=self.show_colors_var,
            command=self.toggle_color_display
        )
        self.show_colors_check.pack(side=tk.LEFT, padx=(20, 0))
        
        # Text editor với hỗ trợ màu sắc
        self.text_editor = scrolledtext.ScrolledText(edit_frame, wrap=tk.WORD, width=50, height=20)
        self.text_editor.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình các tag màu sắc
        self.setup_color_tags()
        
        # Buttons cho việc chỉnh sửa
        edit_button_frame = ttk.Frame(edit_frame)
        edit_button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(edit_button_frame, text="✅ Cập nhật", command=self.update_item).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(edit_button_frame, text="❌ Hủy thay đổi", command=self.cancel_changes).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(edit_button_frame, text="🎨 Chọn màu", command=self.show_color_picker).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(edit_button_frame, text="🗑️ Xóa Item", command=self.delete_item).pack(side=tk.LEFT)
        
        # Biến lưu trữ item đang chỉnh sửa
        self.current_editing_index = -1
    
    def toggle_color_display(self):
        """Bật/tắt hiển thị màu sắc"""
        if self.current_editing_index >= 0:
            selected_item = self.data[self.current_editing_index]
            if self.show_colors_var.get():
                # Hiển thị với màu sắc
                self.apply_colors_to_text(selected_item['display_content'])
            else:
                # Xóa tất cả màu sắc
                for tag in self.text_editor.tag_names():
                    if tag.startswith("color_"):
                        self.text_editor.tag_delete(tag)
    
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
            
            # Chuyển đổi nội dung để hiển thị
            display_content = self.convert_to_display(content_part)
            
            return {
                'id': item_id,
                'raw_content': content_part,
                'display_content': display_content
            }
        except:
            return None
    
    def convert_to_display(self, raw_content):
        """Chuyển đổi nội dung raw thành nội dung hiển thị với màu sắc"""
        # Chuyển \r thành xuống dòng thật
        content = raw_content.replace('\\r', '\n')
        return content
    
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
    
    def convert_to_raw(self, display_content):
        """Chuyển nội dung hiển thị về dạng raw (giữ nguyên mã màu nếu có)"""
        # Tạm thời chỉ chuyển xuống dòng thành \r
        content = display_content.replace('\n', '\\r')
        return content
    
    def detect_encoding(self, file_path):
        """Tự động phát hiện encoding của file"""
        encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'utf-16le', 'utf-16be', 'gbk', 'gb2312', 'big5', 'cp1252', 'latin1', 'ascii']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        # Nếu không phát hiện được, thử với errors='ignore'
        return 'utf-8'
    
    def open_file(self):
        """Mở file txt"""
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
            self.file_label.config(text=f"File: {os.path.basename(file_path)} (Encoding: {detected_encoding})")
            self.refresh_tree()
            
            other_lines_count = len(self.other_lines)
            messagebox.showinfo("Thành công", f"Đã tải {len(self.data)} items từ file\nEncoding: {detected_encoding}\nBảo toàn {other_lines_count} dòng khác (comment, metadata)")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file: {str(e)}\n\nVui lòng kiểm tra:\n1. File có đúng định dạng không\n2. File có bị hỏng không\n3. Quyền truy cập file")
    
    def refresh_tree(self):
        """Làm mới danh sách items"""
        # Xóa tất cả items hiện tại
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm items mới
        for i, item in enumerate(self.data):
            preview = item['display_content'][:50].replace('\n', ' ')
            if len(item['display_content']) > 50:
                preview += "..."
            
            self.tree.insert("", "end", values=(item['id'], preview), tags=(str(i),))
    
    def on_item_select(self, event):
        """Xử lý khi chọn một item"""
        selection = self.tree.selection()
        if not selection:
            return
            
        # Lấy index của item được chọn
        item = self.tree.item(selection[0])
        index = int(item['tags'][0])
        
        # Hiển thị nội dung trong text editor
        self.current_editing_index = index
        selected_item = self.data[index]
        
        self.current_id_label.config(text=selected_item['id'])
        
        # Xóa nội dung cũ và hiển thị nội dung mới
        self.text_editor.delete('1.0', tk.END)
        self.text_editor.insert('1.0', selected_item['display_content'])
        
        # Áp dụng màu sắc nếu được bật
        if self.show_colors_var.get():
            self.apply_colors_to_text(selected_item['display_content'])
    
    def update_item(self):
        """Cập nhật nội dung item hiện tại"""
        if self.current_editing_index == -1:
            messagebox.showwarning("Cảnh báo", "Chưa chọn item nào để chỉnh sửa")
            return
        
        # Lấy nội dung từ text editor
        new_content = self.text_editor.get('1.0', tk.END).rstrip('\n')
        
        # Cập nhật dữ liệu
        self.data[self.current_editing_index]['display_content'] = new_content
        self.data[self.current_editing_index]['raw_content'] = self.convert_to_raw(new_content)
        
        # Làm mới tree view
        self.refresh_tree()
        
        messagebox.showinfo("Thành công", "Đã cập nhật nội dung")
    
    def cancel_changes(self):
        """Hủy thay đổi và khôi phục nội dung gốc"""
        if self.current_editing_index == -1:
            return
            
        # Khôi phục nội dung gốc
        original_content = self.data[self.current_editing_index]['display_content']
        self.text_editor.delete('1.0', tk.END)
        self.text_editor.insert('1.0', original_content)
        
        # Áp dụng màu sắc nếu được bật
        if self.show_colors_var.get():
            self.apply_colors_to_text(original_content)
    
    def save_file(self):
        """Lưu file với định dạng gốc và bảo toàn các dòng khác"""
        if not self.file_path:
            messagebox.showwarning("Cảnh báo", "Chưa mở file nào")
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
            
            messagebox.showinfo("Thành công", f"Đã lưu file thành công\nEncoding: {detected_encoding}\nBảo toàn tất cả dòng gốc")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")
    
    def search_item(self):
        """Tìm kiếm item theo ID hoặc nội dung"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm kiếm")
        search_window.geometry("400x150")
        search_window.transient(self.root)
        search_window.grab_set()
        
        # Center the window
        search_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        frame = ttk.Frame(search_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Tìm kiếm theo ID hoặc nội dung:").pack(pady=(0, 10))
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(frame, textvariable=search_var, width=40)
        search_entry.pack(pady=(0, 20))
        search_entry.focus()
        
        def do_search():
            query = search_var.get().strip().lower()
            if not query:
                return
            
            # Tìm kiếm
            for i, item in enumerate(self.data):
                if (query in item['id'].lower() or 
                    query in item['display_content'].lower()):
                    
                    # Chọn item trong tree
                    children = self.tree.get_children()
                    if i < len(children):
                        self.tree.selection_set(children[i])
                        self.tree.see(children[i])
                        self.on_item_select(None)
                        search_window.destroy()
                        return
            
            messagebox.showinfo("Kết quả", "Không tìm thấy item nào phù hợp")
        
        button_frame = ttk.Frame(frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="Tìm", command=do_search).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Hủy", command=search_window.destroy).pack(side=tk.LEFT)
        
        # Bind Enter key
        search_entry.bind('<Return>', lambda e: do_search())

    def add_new_item(self):
        """Thêm item mới"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm Item Mới")
        add_window.geometry("600x500")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Center the window
        add_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        main_frame = ttk.Frame(add_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ID input
        ttk.Label(main_frame, text="ID:").pack(anchor=tk.W)
        id_var = tk.StringVar()
        id_entry = ttk.Entry(main_frame, textvariable=id_var, width=20)
        id_entry.pack(fill=tk.X, pady=(0, 10))
        id_entry.focus()
        
        # Content input
        ttk.Label(main_frame, text="Nội dung:").pack(anchor=tk.W)
        content_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15)
        content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
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
            self.text_editor.delete('1.0', tk.END)
            self.refresh_tree()
            messagebox.showinfo("Thành công", "Đã xóa item")
    
    def show_color_picker(self):
        """Hiển thị bảng chọn màu"""
        color_window = tk.Toplevel(self.root)
        color_window.title("Chọn Màu")
        color_window.geometry("400x300")
        color_window.transient(self.root)
        color_window.grab_set()
        
        # Center the window
        color_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        main_frame = ttk.Frame(color_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Chọn màu để chèn vào vị trí cursor:", font=("Arial", 10, "bold")).pack(pady=(0, 20))
        
        # Bảng màu
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
                main_frame,
                text=name,
                bg=f"#{hex_code}",
                fg="white" if hex_code in ["000000", "0000ff", "8b4513"] else "black",
                width=12,
                command=lambda code=hex_code: self.insert_color_code(color_window, code)
            )
            color_button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Cấu hình grid
        for i in range(4):
            main_frame.grid_columnconfigure(i, weight=1)
        
        # Custom color input
        custom_frame = ttk.Frame(main_frame)
        custom_frame.grid(row=len(colors)//4 + 1, column=0, columnspan=4, pady=20, sticky="ew")
        
        ttk.Label(custom_frame, text="Hoặc nhập mã hex (6 ký tự):").pack(side=tk.LEFT)
        custom_var = tk.StringVar()
        custom_entry = ttk.Entry(custom_frame, textvariable=custom_var, width=10)
        custom_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        def insert_custom():
            hex_code = custom_var.get().strip()
            if len(hex_code) == 6 and all(c in '0123456789abcdefABCDEF' for c in hex_code):
                self.insert_color_code(color_window, hex_code.lower())
            else:
                messagebox.showwarning("Lỗi", "Mã hex phải có 6 ký tự (0-9, a-f)")
        
        ttk.Button(custom_frame, text="Chèn", command=insert_custom).pack(side=tk.LEFT)
        custom_entry.bind('<Return>', lambda e: insert_custom())
    
    def insert_color_code(self, window, hex_code):
        """Chèn mã màu vào vị trí cursor"""
        color_code = f"^{hex_code}"
        
        # Chèn vào vị trí cursor trong text editor
        cursor_pos = self.text_editor.index(tk.INSERT)
        self.text_editor.insert(cursor_pos, color_code)
        
        # Áp dụng màu sắc nếu được bật
        if self.show_colors_var.get():
            content = self.text_editor.get('1.0', tk.END).rstrip('\n')
            self.apply_colors_to_text(content)
        
        # Focus về text editor
        self.text_editor.focus_set()
        
        window.destroy()
        messagebox.showinfo("Thành công", f"Đã chèn mã màu: {color_code}")

def main():
    root = tk.Tk()
    app = TextEditorTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
