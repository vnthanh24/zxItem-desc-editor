# Tính năng Xóa Nhiều Item

## Tổng quan
Đã thêm tính năng cho phép xóa một hoặc nhiều item cùng lúc trong Advanced Text Editor Tool.

## Các tính năng mới

### 1. Nút "Xóa nhiều Item"
- **Vị trí**: Thanh toolbar chính
- **Biểu tượng**: 🗑️ Xóa nhiều Item
- **Chức năng**: Xóa tất cả các item đã được chọn trong danh sách

### 2. Chọn nhiều item
- **Ctrl + Click**: Chọn/bỏ chọn từng item riêng lẻ
- **Shift + Click**: Chọn vùng item từ item đầu tiên đến item được click
- **Ctrl + A**: Chọn tất cả item
- **Escape**: Bỏ chọn tất cả

### 3. Context Menu (Chuột phải)
Khi click chuột phải vào danh sách item, hiển thị menu với các tùy chọn:
- **🗑️ Xóa item đã chọn**: Xóa tất cả item đã được chọn
- **✅ Chọn tất cả**: Chọn tất cả item trong danh sách
- **❌ Bỏ chọn tất cả**: Bỏ chọn tất cả item

### 4. Phím tắt
- **Delete**: Xóa các item đã chọn
- **Ctrl + D**: Xóa các item đã chọn (phím tắt thay thế)
- **Ctrl + A**: Chọn tất cả item (khi focus ở danh sách)
- **Escape**: Bỏ chọn tất cả (khi focus ở danh sách)

### 5. Hiển thị thông tin
- **Số lượng item đã chọn**: Khi chọn nhiều hơn 1 item, thanh status sẽ hiển thị "Đã chọn X items"
- **Hướng dẫn sử dụng**: Label hướng dẫn phía dưới ô lọc với các mẹo sử dụng nhanh

## Cách sử dụng

### Xóa một item:
1. Click chọn item trong danh sách
2. Nhấn nút "🗑️ Xóa Item" hoặc phím Delete
3. Xác nhận trong dialog

### Xóa nhiều item:
1. **Chọn nhiều item bằng một trong các cách:**
   - Ctrl + Click vào từng item muốn chọn
   - Shift + Click để chọn vùng item
   - Ctrl + A để chọn tất cả
2. **Xóa bằng một trong các cách:**
   - Nhấn nút "🗑️ Xóa nhiều Item"
   - Nhấn phím Delete hoặc Ctrl + D
   - Click chuột phải và chọn "🗑️ Xóa item đã chọn"
3. Xác nhận trong dialog hiển thị danh sách các item sẽ bị xóa

### Chọn nhanh:
- **Ctrl + A**: Chọn tất cả item
- **Escape**: Bỏ chọn tất cả
- **Chuột phải → Chọn tất cả**: Chọn tất cả qua menu
- **Chuột phải → Bỏ chọn tất cả**: Bỏ chọn tất cả qua menu

## Dialog xác nhận
- **Xóa 1 item**: "Bạn có chắc muốn xóa item ID: [ID]?"
- **Xóa nhiều item**: "Bạn có chắc muốn xóa [N] items? ID: [danh sách ID]"

## Thông báo trạng thái
Sau khi xóa thành công, thanh status sẽ hiển thị:
- "Đã xóa item" (màu cam) - khi xóa 1 item
- "Đã xóa [N] items" (màu cam) - khi xóa nhiều item

## Lưu ý quan trọng
- Thao tác xóa không thể hoàn tác
- Khi xóa item đang chỉnh sửa, text editor sẽ được làm sạch
- File sẽ được đánh dấu là đã thay đổi (modified) sau khi xóa
- Cần lưu file để thay đổi có hiệu lực vĩnh viễn

## Mẹo sử dụng
1. Sử dụng ô "Lọc" để thu gọn danh sách trước khi chọn nhiều item
2. Kiểm tra số lượng item đã chọn trên thanh status trước khi xóa
3. Sử dụng phím tắt để thao tác nhanh hơn
4. Click chuột phải để truy cập nhanh các chức năng chọn/xóa