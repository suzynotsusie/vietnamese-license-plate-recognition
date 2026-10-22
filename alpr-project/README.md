# ALPR Việt Nam: project nhận diện biển số

Project và dữ liệu nằm ở **hai ổ khác nhau**. Dữ liệu không chép sang ổ D.

```
D:\vietnamese-license-plate-recognition\        <- repo Git
├── bao_cao\                                    # báo cáo LaTeX
└── alpr-project\                               # project này
    ├── notebooks\
    │   ├── 01_phan_tich_va_lam_sach_nhan.ipynb # ĐÃ CHẠY SẴN: phân tích, sửa nhãn, chia tập
    │   ├── 02_kiem_tra_anh.ipynb               # ảnh thiếu/hỏng, ảnh trùng (cần ảnh gốc)
    │   ├── 03_tao_dataset.ipynb                # sinh dataset YOLO + ảnh biển cắt cho OCR
    │   └── 04_du_lieu_ngoai.ipynb              # video -> khung hình, nhập Roboflow, lọc trùng VNLP
    ├── src\alpr\
    │   ├── plate_format.py     # chuẩn hóa + kiểm tra định dạng biển VN
    │   └── paths.py            # đọc đường dẫn dữ liệu từ config
    ├── data\labels\
    │   ├── vnlp_manifest.csv   # nhãn ĐÃ LÀM SẠCH + tập train/val/test cho 37.297 ảnh
    │   └── label_fixes.csv     # 59 nhãn đã xem lại bằng mắt
    ├── data\external\README.md # ghi nguồn, giấy phép dữ liệu ngoài
    ├── reports\                # DATA_REPORT.md, thống kê, hình
    ├── config.example.json     # đường dẫn dữ liệu mặc định
    └── config.json             # (tự tạo nếu đường dẫn khác, không đưa lên Git)

E:\vietnamese-license-plate-recognition\        <- dữ liệu (không đưa lên Git)
├── VNLP\                       # dữ liệu gốc
├── datasets\                   # sinh ra bởi notebook 03 (vnlp_det, vnlp_ocr, external)
└── external\                   # video, bộ dữ liệu tải về (notebook 04)
```

Đọc **[reports/DATA_REPORT.md](reports/DATA_REPORT.md)** để xem kết quả phân tích và hướng giải quyết.

## Cài đặt

```powershell
cd D:\vietnamese-license-plate-recognition\alpr-project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks
```
Hoặc mở thư mục bằng VS Code và chọn kernel `.venv`.

**Đường dẫn dữ liệu:** mặc định đọc từ `config.example.json` (ổ E như trên). Máy nào để dữ liệu chỗ khác
thì chép `config.example.json` thành `config.json` rồi sửa, hoặc đặt biến môi trường `VNLP_ROOT`,
`DATASETS_DIR`, `EXTERNAL_DIR`. `datasets_dir` nên cùng ổ với `vnlp_root` để notebook 03 dùng được
hard link (không tốn thêm dung lượng).

## Thứ tự chạy

1. `01`: đã chạy sẵn. Chỉ chạy lại nếu sửa `data/labels/label_fixes.csv`.
2. `02`: chạy một lần, mất vài phút. Xem tóm tắt cuối notebook.
3. `03`: sinh `vnlp_det` (YOLO, 2 lớp) và `vnlp_ocr` trong `datasets_dir`.
4. `04`: khi có dữ liệu ngoài.

## Quy ước

- Chuỗi biển ở dạng gọn: in hoa, không dấu gạch, không dấu chấm (`30A-123.45` thành `30A12345`).
- Tọa độ trong tên tệp VNLP là **(x1, y1, x2, y2)**, không phải (x, y, w, h) như readme gốc ghi.
- Lớp detection: `0 = plate_1row`, `1 = plate_2row`.
- Train/val/test chia **theo chuỗi biển**: một biển chỉ nằm trong một tập.
