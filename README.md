# Text Editor Tool - Công cụ chỉnh sửa file mô tả item

## Mô tả
Tool GUI để chỉnh sửa file .txt chứa thông tin các item game với định dạng:
```
[ID]    "[mã_màu][nội_dung]"
```

Tool sẽ chuyển đổi:
- Mã màu (^xxxxxx) → Ẩn đi khi hiển thị
- \r → Xuống dòng thật trong editor
- Hiển thị nội dung dễ đọc, dễ chỉnh sửa

## Yêu cầu hệ thống
- Python 3.6 trở lên
- Tkinter (thường có sẵn với Python)

## Cài đặt Python
1. Tải Python từ: https://www.python.org/downloads/
2. Khi cài đặt, nhớ tick "Add Python to PATH"
3. Hoặc cài từ Microsoft Store
4. Chạy `install_requirements.bat` để cài thư viện cần thiết (tùy chọn)

## Xử lý lỗi Encoding
Tool tự động phát hiện encoding của file. Nếu gặp lỗi:
```
'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

Tool sẽ:
1. Tự động thử các encoding phổ biến: UTF-8, UTF-16, GB2312, Big5, Latin1, v.v.
2. Sử dụng thư viện `chardet` để phát hiện encoding (nếu có cài)
3. Hiển thị encoding đã phát hiện trong thông báo
4. Lưu file với cùng encoding gốc

Để cài đặt thư viện phát hiện encoding tốt hơn:
```bash
pip install chardet
```
Hoặc chạy file `install_requirements.bat`

## Cách sử dụng

### Phương pháp 1: Chạy trực tiếp
```bash
python text_editor_tool.py
```

### Phương pháp 2: Sử dụng file batch
Double-click vào `run_tool.bat`

## Tính năng

### 1. Mở file
- Click "Mở File" để chọn file .txt
- Tool sẽ phân tích và hiển thị danh sách items
- Tự động phát hiện encoding (UTF-8, UTF-16, ANSI, v.v.)

### 2. Xem và chỉnh sửa với màu sắc thực tế 🎨
- Danh sách items hiển thị ở bên trái với ID và preview
- Click vào item để xem nội dung đầy đủ ở bên phải
- **MỚI:** Hiển thị văn bản với màu sắc thực tế theo mã hex
  - `^ff0000` → Văn bản màu đỏ thực tế
  - `^00ff00` → Văn bản màu xanh lá thực tế
  - `^0090ff` → Văn bản màu xanh dương nhạt thực tế
- Checkbox để bật/tắt hiển thị màu sắc
- Nội dung hiển thị sẽ chuyển `\r` thành xuống dòng đúng định dạng

### 3. Chỉnh sửa nội dung
- Chỉnh sửa nội dung trong khung text editor với màu sắc trực quan
- Click "Cập nhật" để lưu thay đổi
- Click "Hủy thay đổi" để khôi phục nội dung gốc
- Mã màu được giữ nguyên khi lưu file

### 4. Tìm kiếm
- Click "Tìm kiếm" để tìm theo ID hoặc nội dung
- Nhập từ khóa và nhấn Enter hoặc click "Tìm"

### 5. Lưu file
- Click "Lưu File" để lưu tất cả thay đổi
- File sẽ được lưu với định dạng gốc (có mã màu và \r)

## Định dạng file input
```
70718	"^6cfb4bThiên cơ vô thường, thanh lục khuy mệnh.\r^ffcb4aNhấp chuột phải, có thể tiến hành thao tác như giám định,\r trang bị, phân giải đối với trang bị."
70719	"^ff0000Kiếm khí bát phương.\r^00ff00Tăng sát thương cho tất cả đòn tấn công."
```

## Định dạng hiển thị trong editor (MỚI! 🎨)
```
🎨 Với màu sắc thực tế:
Thiên cơ vô thường, thanh lục khuy mệnh.        (màu xanh lá #6cfb4b)
Nhấp chuột phải, có thể tiến hành thao tác...   (màu cam #ffcb4a)
trang bị, phân giải đối với trang bị.
```

## Tùy chọn hiển thị
- ☑️ **Hiển thị màu sắc**: Bật/tắt màu sắc thực tế theo mã hex
- ☑️ **Hiển thị mã màu** (phiên bản nâng cao): Hiển thị/ẩn mã ^xxxxxx

## File mẫu
`sample_data.txt` - File mẫu để test tool

## Lưu ý
- Tool giữ nguyên định dạng gốc khi lưu file
- Mã màu được ẩn khi hiển thị nhưng vẫn được bảo toàn
- Hỗ trợ tìm kiếm không phân biệt hoa thường
- Backup file gốc trước khi chỉnh sửa để đảm bảo an toàn
