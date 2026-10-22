"""Chuẩn hóa và kiểm tra định dạng biển số Việt Nam.

Chuỗi biển được lưu ở dạng "gọn": chữ in hoa, không dấu gạch, không dấu chấm.
Ví dụ: 30A-123.45 -> 30A12345, 29-G1 410.81 -> 29G141081.
"""
import re

# Các mẫu định dạng (áp dụng trên chuỗi gọn)
PATTERNS = {
    # Ô tô: 2 số mã tỉnh + 1-2 chữ seri + 4-5 số thứ tự. VD 30A12345, 51LD12345, 36N1078
    "car": re.compile(r"^\d{2}[A-Z]{1,2}\d{4,5}$"),
    # Xe máy mới: 2 số + chữ + chữ/số + 4-5 số. VD 29G141081, 30K82182, 29AA12345
    "moto": re.compile(r"^\d{2}[A-Z][A-Z0-9]\d{4,5}$"),
    # Xe máy điện (MĐ, ghi là MD): 29MD122383
    "moto_md": re.compile(r"^\d{2}MD\d\d{4,5}$"),
    # Xe máy kiểu cũ: mã tỉnh + 3 số + seri ở cuối. VD 31960H4 (31 / 960-H4), 29947RY
    "moto_old": re.compile(r"^\d{2}\d{3}[A-Z][A-Z0-9]$"),
    # Biển tổ chức/cá nhân nước ngoài: 29-636-NN-479, 41-291-NG-01
    "foreign": re.compile(r"^\d{2}\d{3}(NG|NN|QT|CV)\d{2,3}$"),
}

# Chữ cái thực tế xuất hiện trên biển VN (không dùng I, O, Q, W)
VALID_LETTERS = set("ABCDEFGHKLMNPRSTUVXYZ")
VALID_CHARS = VALID_LETTERS | set("0123456789")


def normalize(raw: str) -> str:
    """Bỏ ký tự phân cách, đổi sang chữ in hoa, Đ -> D."""
    s = raw.upper().replace("Đ", "D")
    return re.sub(r"[^A-Z0-9]", "", s)


def plate_format(s: str):
    """Trả về tên định dạng khớp đầu tiên, hoặc None."""
    if any(c not in VALID_CHARS for c in s):
        return None
    for name, rx in PATTERNS.items():
        if rx.match(s):
            return name
    return None


def province(s: str) -> str:
    return s[:2] if len(s) >= 2 and s[:2].isdigit() else ""


def display(s: str, fmt: str = None) -> str:
    """Định dạng hiển thị: 30A12345 -> 30A-123.45 ; 29G141081 -> 29-G1 410.81."""
    fmt = fmt or plate_format(s)
    if fmt == "car":
        m = re.match(r"^(\d{2}[A-Z]{1,2})(\d+)$", s)
        head, num = m.groups()
        return f"{head}-{num[:3]}.{num[3:]}" if len(num) == 5 else f"{head}-{num}"
    if fmt in ("moto", "moto_md"):
        head, num = s[:4], s[4:]
        if fmt == "moto_md":
            head, num = s[:5], s[5:]
        return f"{head[:2]}-{head[2:]} {num[:3]}.{num[3:]}" if len(num) == 5 else f"{head[:2]}-{head[2:]} {num}"
    if fmt == "moto_old":
        return f"{s[:2]} {s[2:5]}-{s[5:]}"
    if fmt == "foreign":
        return f"{s[:2]}-{s[2:5]}-{s[5:7]}-{s[7:]}"
    return s


# Định dạng hợp lệ theo loại phương tiện
VEHICLE_FORMATS = {
    "car": ("car", "foreign"),
    "moto": ("moto", "moto_md", "moto_old", "foreign", "car"),
}


def is_valid(s: str, vehicle: str) -> bool:
    fmt = plate_format_for(s, vehicle)
    return fmt is not None


def plate_format_for(s: str, vehicle: str):
    if any(c not in VALID_CHARS for c in s):
        return None
    for name in VEHICLE_FORMATS[vehicle]:
        if PATTERNS[name].match(s):
            return name
    return None
