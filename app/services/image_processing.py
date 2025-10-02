from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

import cv2
import numpy as np
from skimage import exposure, restoration
from skimage.transform import iradon, radon

ProgressCallback = Optional[Callable[[float, str], None]]


@dataclass
class SinogramResult:
    """Gói dữ liệu sinogram để sử dụng cho hiển thị và tái tạo."""

    raw: np.ndarray
    theta: np.ndarray
    display: np.ndarray
    original_shape: tuple[int, int]

    @property
    def image(self) -> np.ndarray:
        """Ảnh sinogram đã chuẩn hóa để hiển thị."""
        return self.display


def preprocess_and_denoise(img_gray: np.ndarray, progress_callback: ProgressCallback = None) -> np.ndarray:
    """Tiền xử lý và khử nhiễu ảnh grayscale (uint8)."""

    if progress_callback:
        progress_callback(0.1, "Đang chuẩn bị ảnh...")

    img = img_gray.astype(np.float32) / 255.0

    if progress_callback:
        progress_callback(0.3, "Đang cân bằng histogram...")

    eq = exposure.equalize_adapthist(img, clip_limit=0.02)

    if progress_callback:
        progress_callback(0.5, "Đang khử nhiễu ảnh...")

    denoised = restoration.denoise_nl_means(
        eq,
        patch_size=3,
        patch_distance=4,
        h=0.05,
        channel_axis=None,
    )

    if progress_callback:
        progress_callback(0.8, "Hoàn tất xử lý...")

    return (denoised * 255).astype(np.uint8)


def create_sinogram(img_gray: np.ndarray, progress_callback: ProgressCallback = None) -> SinogramResult:
    """Tạo sinogram từ ảnh grayscale đã xử lý."""

    if progress_callback:
        progress_callback(0.85, "Đang tạo sinogram...")

    max_size = 256
    h, w = img_gray.shape
    scale = min(max_size / h, max_size / w, 1.0)
    resized = img_gray if scale == 1.0 else cv2.resize(
        img_gray,
        (int(w * scale), int(h * scale)),
        interpolation=cv2.INTER_AREA,
    )

    img = resized.astype(np.float32) / 255.0
    theta = np.linspace(0.0, 180.0, max(img.shape), endpoint=False)
    sino_raw = radon(img, theta=theta, circle=False)

    # Chuẩn hóa để hiển thị
    sino_display = sino_raw - np.min(sino_raw)
    if np.max(sino_display) > 0:
        sino_display = sino_display / np.max(sino_display)
    sino_display = (sino_display * 255).astype(np.uint8)

    if progress_callback:
        progress_callback(0.95, "Hoàn thành sinogram")

    return SinogramResult(
        raw=sino_raw,
        theta=theta,
        display=sino_display,
        original_shape=resized.shape,
    )


def sinogram_from_image_array(
    sinogram_img: np.ndarray,
    *,
    target_shape: Optional[Tuple[int, int]] = None,
) -> SinogramResult:
    sinogram_float = sinogram_img.astype(np.float32)
    if sinogram_float.max() > 1.0:
        sinogram_float /= 255.0

    angles = np.linspace(0.0, 180.0, sinogram_float.shape[1], endpoint=False)
    if target_shape is None:
        side = int(sinogram_float.shape[0])
        target_shape = (side, side)

    display = sinogram_img.astype(np.uint8)

    return SinogramResult(
        raw=sinogram_float,
        theta=angles,
        display=display,
        original_shape=target_shape,
    )


def reconstruct_image(sinogram: SinogramResult, progress_callback: ProgressCallback = None) -> np.ndarray:
    """Tái tạo ảnh từ sinogram bằng phép chiếu ngược (Filtered Back Projection)."""

    if progress_callback:
        progress_callback(0.97, "Đang tái tạo ảnh CT...")

    reconstruction = iradon(
        sinogram.raw,
        theta=sinogram.theta,
        filter_name="hann",
        circle=False,
    )

    # Chuẩn hóa về thang 0-255
    reconstruction -= reconstruction.min()
    max_val = reconstruction.max()
    if max_val > 0:
        reconstruction /= max_val
    reconstruction_uint8 = (reconstruction * 255).astype(np.uint8)

    target_shape = sinogram.original_shape
    if reconstruction_uint8.shape != target_shape:
        reconstruction_uint8 = cv2.resize(
            reconstruction_uint8,
            (target_shape[1], target_shape[0]),
            interpolation=cv2.INTER_CUBIC,
        )

    if progress_callback:
        progress_callback(1.0, "Hoàn tất tái tạo")

    return reconstruction_uint8


def get_image_info(img: np.ndarray) -> dict[str, str]:
    """Lấy thông tin cơ bản của ảnh."""

    return {
        "Kích thước": f"{img.shape[1]} x {img.shape[0]} pixels",
        "Độ sâu": f"{img.dtype}",
        "Kênh màu": "Grayscale" if len(img.shape) == 2 else f"{img.shape[2]} channels",
        "Min/Max": f"{img.min()} / {img.max()}",
    }
