# xử lý ảnh CT

Ứng dụng Streamlit mô phỏng chuỗi xử lý ảnh trong chẩn đoán hình ảnh: nâng cao chất lượng, tạo sinogram và tái tạo cắt lớp tương tự máy CT. Phiên bản mới sở hữu giao diện Liquid Glass tối giản với thanh điều khiển cố định, giúp thao tác nhanh hơn khi xử lý hàng loạt.

## ✨ Tính năng chính

- **Tiền xử lý & khử nhiễu ảnh** bằng cân bằng histogram thích nghi và lọc NL-Means.
- **Tạo sinogram** thông qua phép chiếu Radon với thông tin góc đầy đủ.
- **Tái tạo ảnh CT (Filtered Back Projection)** từ sinogram vừa xử lý hoặc sinogram tải lên từ hệ thống ngoài.
- **Hỗ trợ đa nguồn dữ liệu**: ảnh PNG/JPG, file DICOM, webcam và sinogram (.png/.npy).
- **Tùy chọn hiển thị linh hoạt**: bật Popover "Cài đặt hiển thị" để chuyển giữa hai tab riêng hoặc xem song song ngay trên một màn hình.

## 🗂️ Cấu trúc dự án

```
├── app/
│   ├── assets/                # (dự phòng) nơi lưu trữ nội dung tĩnh
│   ├── services/              # Xử lý dữ liệu & nghiệp vụ hình ảnh
│   │   ├── data_loader.py
│   │   ├── image_processing.py
│   │   └── pipeline.py
│   └── ui/                    # Thành phần giao diện
│       ├── components/
│       │   ├── controls.py
│       │   ├── header.py
│       │   ├── progress.py
│       │   └── results.py
│       ├── __init__.py
│       └── styles.py
├── main.py                    # Điểm vào Streamlit
├── requirements.txt
└── README.md
```

## 🚀 Cách chạy

1. Tạo và kích hoạt môi trường ảo (khuyến nghị).
2. Cài đặt phụ thuộc:

```powershell
pip install -r requirements.txt
```

3. Khởi chạy ứng dụng:

```powershell
streamlit run main.py
```

## 💡 Gợi ý sử dụng

- Bật **"Hiển thị thanh tiến trình"** để theo dõi từng bước khử nhiễu, tạo sinogram và tái tạo (thanh trạng thái hiển thị ở tab "Kết quả").
- Với file DICOM lớn, hãy xử lý theo từng lô nhỏ để tiết kiệm bộ nhớ GPU/CPU.
- Tab "Tái tạo từ sinogram" hỗ trợ chọn kích thước đầu ra; thử nhiều giá trị để tối ưu mức chi tiết mong muốn.

## 🧭 Gợi ý nghiên cứu trải nghiệm người dùng

**10 câu hỏi khảo sát người dùng:**

1. Khi mở ứng dụng, anh/chị muốn nhìn thấy thông tin hoặc hành động nào đầu tiên để tự tin bắt đầu xử lý?
2. Điều gì khiến anh/chị bối rối nhất khi chuyển giữa Pipeline Studio và Sinogram Lab?
3. Anh/chị thường đánh giá chất lượng ảnh đã xử lý bằng tiêu chí nào và cần thêm số liệu gì trên màn hình kết quả?
4. Tần suất anh/chị thay đổi bảng màu hoặc chế độ sáng/tối trong một buổi làm việc là bao nhiêu và vì lý do gì?
5. Anh/chị mong muốn nhận thông báo dạng nào khi xử lý thất bại để có thể khắc phục nhanh chóng?
6. Trong quy trình hiện tại, bước tải dữ liệu nào (ảnh thường, DICOM, sinogram) tốn nhiều thời gian nhất và vì sao?
7. Anh/chị có cần so sánh nhiều hơn hai ảnh cùng lúc không và nếu có, mong muốn bố cục hiển thị ra sao?
8. Tùy chọn nào trong phần cài đặt giao diện khiến anh/chị ít sử dụng nhất và vì sao?
9. Anh/chị có cần lưu cấu hình xử lý để áp dụng lại cho các ca tương tự không? Nếu có, mong muốn thao tác lưu ở đâu?
10. Một buổi làm việc lý tưởng với công cụ nên kéo dài bao lâu và những thao tác nào cần được tự động hóa thêm?

**Các tình huống luồng sử dụng cần kiểm tra:**

- Kỹ sư nhận nhanh một lô ảnh chuẩn 2D, bật chế độ auto-process và cần xem ngay chênh lệch trước/sau.
- Bác sĩ đọc lại sinogram từ máy CT khác, đổi sang Sinogram Lab, điều chỉnh kích thước tái tạo phù hợp báo cáo hội chẩn.
- Kỹ thuật viên phải trình chiếu cho sinh viên, bật chế độ song song, chọn palette sáng và Dark Mode luân phiên để phù hợp phòng học.
- Nhân viên QA cần kiểm tra thất bại: xử lý file lỗi để xem thông báo, sau đó đổi nguồn dữ liệu khác tiếp tục quy trình.
- Nhà nghiên cứu dựng pipeline riêng, cần ghi chú nguồn dữ liệu và xuất các thông số tái tạo để đưa vào báo cáo trải nghiệm.

## 📄 Giấy phép

Dự án phục vụ mục đích học tập và nghiên cứu. Vui lòng kiểm tra lại toàn quyền khi sử dụng trong môi trường sản xuất.
"# MYCODE" 
