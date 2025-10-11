from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING, Any, Tuple

import cv2
import numpy as np
import pydicom

if TYPE_CHECKING:  # pragma: no cover
    from streamlit.runtime.uploaded_file_manager import UploadedFile
else:  # pragma: no cover
    UploadedFile = Any  # type: ignore


def _read_bytes(file: UploadedFile) -> bytes:
    if hasattr(file, "getvalue"):
        return file.getvalue()
    return file.read()


def load_standard_image(file: UploadedFile) -> Tuple[np.ndarray, np.ndarray]:
    data = np.frombuffer(_read_bytes(file), dtype=np.uint8)
    bgr = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("Không thể đọc ảnh chuẩn.")
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb, gray


def load_dicom_image(file: UploadedFile) -> np.ndarray:
    dataset = pydicom.dcmread(BytesIO(_read_bytes(file)))
    array = dataset.pixel_array.astype(np.float32)
    normalized = cv2.normalize(array, None, 0, 255, cv2.NORM_MINMAX)
    return normalized.astype(np.uint8)


def load_sinogram_image(file: UploadedFile) -> np.ndarray:
    name = getattr(file, "name", "").lower()
    raw_bytes = _read_bytes(file)

    if name.endswith(".npy"):
        buffer = BytesIO(raw_bytes)
        array = np.load(buffer)
        if array.ndim == 3:
            array = cv2.cvtColor(array.astype(np.float32), cv2.COLOR_BGR2GRAY)
        normalized = cv2.normalize(array.astype(np.float32), None, 0, 255, cv2.NORM_MINMAX)
        return normalized.astype(np.uint8)

    data = np.frombuffer(raw_bytes, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Không thể đọc sinogram theo định dạng đã chọn.")
    return image.astype(np.uint8)

