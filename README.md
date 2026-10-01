# 3D Terrarium

Bể cá / tiểu cảnh 3D cá nhân chạy trong trình duyệt (Three.js), dùng làm hình nền động trên Mac.

## Chạy
Bấm đúp **`Mở Bể Cá.command`**. File này bật máy chủ nhỏ `aq_server.py` (chỉ trên máy, cổng 8791) rồi mở Safari.
Cần Python 3 và có mạng ở lần đầu (Three.js tải từ CDN).

## Xem trực tuyến (GitHub Pages)
https://mrgiangleai.github.io/3D-terrarium/ — chạy được toàn bộ bể, nhưng không có máy chủ quản lý nên **Quản lý mô hình** (xóa file, tải thêm) chỉ dùng được khi chạy bằng `Mở Bể Cá.command`. Dữ liệu bể lưu trong trình duyệt của từng người.

## Tính năng
- **Kiểu bể** (tab Bể): bể cá chữ nhật, hộp terrarium có nắp và đế gỗ, bể kính cắt góc kiểu kim cương; chỉnh rộng/cao/sâu/cắt góc, đế (gỗ sáng, nâu đỏ, đá), khung (silicone hay kim loại mảnh), nắp kính.
- **Nền tường trong bể**: tường rêu 3D, đá phiến, vỏ bần, đen; tường phòng bê tông.
- **Bể mẫu bày sẵn như ảnh tham khảo** và cảnh khởi đầu mặc định; góc nhìn toàn cảnh, cuộn chuột để zoom theo con trỏ, Shift + kéo để dịch, bấm đúp để về lại.
- Đèn: LED, rọi, ánh trăng, **đèn cổ ngỗng**, **LED màu phía sau**; chỉnh độ cao, màu, độ sáng.
- Tự setup từ Thư viện: nền, đá, lũa, cây, trang trí, cá, rùa, cua.
- Vật lý thật (Rapier): xếp chồng, xoay 3 chiều, đổi cỡ.
- Cọ tô rêu lên bề mặt vật; cọ chỉnh địa hình (nâng/hạ/gồ ghề/làm phẳng).
- Mực nước chỉnh tới 3% để làm bể bán cạn; mặt nước phản chiếu, độ trong chỉnh được.
- Cá bơi đàn 3D, cho ăn; rùa và cua có hoạt ảnh.
- **Quản lý mô hình**: chọn giữ/xóa, tải thêm từ Poly Haven, link Sketchfab, nhập file `.glb` từ `models/inbox/`.

## Phím tắt
`H` ẩn giao diện · `F` cho ăn · `B` cọ rêu · `T` cọ địa hình · `Q/E` xoay · `W/A/S/D` nghiêng · `R` dựng thẳng · `[` `]` đổi cỡ cọ · `Esc` thoát chế độ.

## Mô hình 3D và giấy phép
- `models/*` (đá, lũa, cây, bình…): [Poly Haven](https://polyhaven.com), CC0.
- `models/fish/BarramundiFish.glb`: Khronos glTF Sample Assets, CC0.
- Cá, rùa, cua còn lại dựng bằng code. Mô hình tải từ Sketchfab (nếu có) giữ giấy phép riêng của tác giả, đặt trong `models/inbox/` và không đưa lên git.
