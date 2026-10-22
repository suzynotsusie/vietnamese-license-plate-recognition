"""Đường dẫn dữ liệu của project.

Project (mã nguồn, notebook) và dữ liệu nằm ở hai ổ khác nhau:
  D:\\vietnamese-license-plate-recognition\\alpr-project   <- project
  E:\\vietnamese-license-plate-recognition\\VNLP           <- dữ liệu gốc (không chép sang D)

Thứ tự ưu tiên khi tìm đường dẫn:
  1. Biến môi trường VNLP_ROOT, DATASETS_DIR, EXTERNAL_DIR
  2. Tệp config.json ở thư mục gốc project (mỗi máy tự tạo, không đưa lên Git)
  3. Tệp config.example.json (mặc định của nhóm)
"""
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KEYS = ("vnlp_root", "datasets_dir", "external_dir")


def load_paths(verbose: bool = True) -> dict:
    cfg = {}
    for name in ("config.example.json", "config.json"):  # config.json ghi đè bản mẫu
        f = PROJECT_ROOT / name
        if f.exists():
            cfg.update(json.loads(f.read_text(encoding="utf-8")))
    for k in KEYS:
        if os.environ.get(k.upper()):
            cfg[k] = os.environ[k.upper()]
    paths = {}
    for k in KEYS:
        p = Path(cfg[k])
        paths[k] = p if p.is_absolute() else (PROJECT_ROOT / p).resolve()  # đường dẫn tương đối tính từ project
    paths["project_root"] = PROJECT_ROOT
    if verbose:
        for k, v in paths.items():
            print(f"{k:13s}: {v}  {'(OK)' if v.exists() else '(CHƯA CÓ)'}")
    if not paths["vnlp_root"].exists():
        print("\nKhông tìm thấy dữ liệu VNLP. Tạo config.json (chép từ config.example.json) và sửa vnlp_root.")
    return paths
