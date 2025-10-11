from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class QAItem:
    id: str
    answer: str
    keywords: List[str]


def _normalize(text: str) -> str:
    return (text or "").strip().lower()


def _contains_any(text: str, needles: List[str]) -> bool:
    return any(k in text for k in needles)


# Curated knowledge base (Vietnamese, UTF-8)
_KB: Dict[str, QAItem] = {
    "fbp": QAItem(
        id="fbp",
        keywords=[
            "fbp",
            "filtered back projection",
            "backprojection",
            "tái tạo fbp",
        ],
        answer=(
            "FBP (Filtered Back Projection) là phương pháp tái tạo ảnh CT cổ điển. "
            "Quy trình: (1) có sinogram là tập phép chiếu Radon theo nhiều góc; "
            "(2) lọc tần số (ví dụ Hann) để giảm mờ; (3) chiếu ngược (back-project) các phép chiếu đã lọc về không gian ảnh; "
            "(4) chuẩn hóa cường độ. Trong mã, bước (2)-(3) được thực hiện bằng skimage.transform.iradon(filter_name='hann')."
        ),
    ),
    "inputs": QAItem(
        id="inputs",
        keywords=[
            "nguồn dữ liệu",
            "đầu vào",
            "input",
            "định dạng",
            "dữ liệu đầu vào",
        ],
        answer=(
            "Nguồn dữ liệu đầu vào được hỗ trợ: (1) ảnh thường PNG/JPG (đọc bằng OpenCV, chuyển xám); "
            "(2) file DICOM (đọc bằng pydicom, dùng pixel_array rồi chuẩn hóa 0–255); (3) sinogram từ ảnh xám hoặc file .npy. "
            "Khi tạo sinogram từ ảnh, góc chiếu (theta) được lấy đều trong [0,180) với số góc bằng cạnh dài của ảnh đã resize."
        ),
    ),
    "principle": QAItem(
        id="principle",
        keywords=[
            "nguyên lý",
            "cơ chế",
            "hoạt động",
            "principle",
            "radon",
            "iradon",
            "sinogram",
        ],
        answer=(
            "Nguyên lý: ảnh xám được biến đổi Radon để tạo sinogram (ma trận cường độ theo vị trí cảm biến và góc chiếu). "
            "Từ sinogram, dùng phép chiếu ngược có lọc (iradon) để khôi phục lát cắt CT. "
            "Trong code: radon(img, theta) tạo sinogram; iradon(sino, theta, filter_name='hann', circle=False) tái tạo ảnh."
        ),
    ),
    "algorithms": QAItem(
        id="algorithms",
        keywords=[
            "thuật toán",
            "algorithm",
            "áp dụng",
            "preprocess",
            "khử nhiễu",
            "clahe",
            "nl-means",
            "hann",
            "filter",
        ],
        answer=(
            "Thuật toán áp dụng: (1) Tiền xử lý gồm CLAHE (cân bằng histogram thích nghi) và khử nhiễu NL-Means; "
            "(2) Tạo sinogram bằng Radon với theta đều từ 0–180°; (3) Tái tạo bằng FBP (iradon) với bộ lọc Hann."
        ),
    ),
    "outputs": QAItem(
        id="outputs",
        keywords=[
            "đầu ra",
            "output",
            "kết quả",
            "sản phẩm",
        ],
        answer=(
            "Đầu ra trong Pipeline Studio: (a) ảnh sau khử nhiễu, (b) sinogram để hiển thị, (c) ảnh CT tái tạo (uint8). "
            "Trong Sinogram Lab: nhận sinogram và xuất ảnh CT tái tạo (chuẩn hóa 0–255, resize về kích thước mục tiêu)."
        ),
    ),
    "basis": QAItem(
        id="basis",
        keywords=[
            "dựa trên",
            "thông tin nào",
            "metadata",
            "tham số",
            "parameters",
        ],
        answer=(
            "Thông tin sử dụng: với ảnh thường/DICOM chỉ dùng cường độ điểm ảnh (grayscale) sau chuẩn hóa; không dùng metadata bệnh nhân. "
            "Sinogram tạo với theta đều theo chiều rộng/chiều cao; tái tạo dùng filter Hann, circle=False. "
            "Tiền xử lý: CLAHE clip_limit≈0.02; NL-Means patch_size=3, patch_distance=4, h≈0.05."
        ),
    ),
    "topics": QAItem(
        id="topics",
        keywords=["chủ đề", "help", "topics"],
        answer=(
            "Chủ đề hỗ trợ: FBP, nguồn dữ liệu đầu vào, nguyên lý hoạt động, thuật toán áp dụng, đầu ra, dựa trên thông tin nào."
        ),
    ),
}


def get_supported_topics() -> List[str]:
    return [
        "FBP",
        "Nguồn dữ liệu đầu vào",
        "Nguyên lý hoạt động",
        "Thuật toán áp dụng",
        "Đầu ra",
        "Dựa trên thông tin nào",
    ]


def answer_question(query: str) -> Optional[str]:
    text = _normalize(query)
    if not text:
        return None
    for item in _KB.values():
        if _contains_any(text, item.keywords):
            return item.answer
    return None

