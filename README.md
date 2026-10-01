# 3D Terrarium

Bể cá / tiểu cảnh 3D cá nhân chạy trong trình duyệt (Three.js), dùng làm hình nền động trên Mac.

## Chạy
Bấm đúp **`Mở Bể Cá.command`**. File này bật máy chủ nhỏ `aq_server.py` (chỉ trên máy, cổng 8791) rồi mở Safari.
Cần Python 3 và có mạng ở lần đầu (Three.js tải từ CDN).

## Xem trực tuyến (GitHub Pages)
https://mrgiangleai.github.io/3D-terrarium/ — mở link là dùng được **toàn bộ**, không cần chạy file nào. Dữ liệu bể và danh mục mô hình lưu trong trình duyệt của từng người. Trên link, **Quản lý mô hình** hoạt động như sau: bỏ chọn = gỡ khỏi thư viện; thêm mô hình Poly Haven = tải thẳng từ polyhaven.com khi dùng; nhập file `.glb` từ máy = lưu trong trình duyệt. Chỉ muốn **xóa/tải file thật về máy** thì mới cần `Mở Bể Cá.command`.

## Dùng trên điện thoại
Mở cùng link trên điện thoại: giao diện tự chuyển thành **ngăn kéo ở dưới** (chạm thanh trên cùng để thu nhỏ / vừa / cao), nút 👁 góc trên phải để ẩn hiện. **Chụm hai ngón** để zoom, **kéo hai ngón** để dịch, **chạm hai lần** vào khoảng trống để về lại; chạm chọn món rồi chạm vào bể để đặt, bấm **Xong** để thoát chế độ đặt / cọ. Máy yếu sẽ tự hạ độ nét; muốn nhẹ hơn nữa chọn chất lượng **Thấp**. Trên iPhone: Safari → Chia sẻ → **Thêm vào MH chính** để mở toàn màn hình như một app.

## Tính năng
- **Kiểu bể** (tab Bể): bể cá chữ nhật, hộp terrarium có nắp và khay gỗ vằn, bể kính cắt góc kiểu kim cương (vát đáy + nắp, sỏi đen, bệ đen); chỉnh rộng/cao/sâu/cắt góc/vát, đế (gỗ vằn, gỗ sáng, nâu đỏ, đá, bệ đen), khung (silicone hay kim loại mảnh), nắp kính.
- **Nền tường trong bể**: tường rêu 3D nổi gò (rêu "lông" nhiều lớp, đậm nhạt loang), đá phiến, vỏ bần, đen; tường phòng bê tông.
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
