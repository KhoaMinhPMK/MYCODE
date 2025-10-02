from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from .image_processing import (
    SinogramResult,
    create_sinogram,
    get_image_info,
    preprocess_and_denoise,
    reconstruct_image,
    sinogram_from_image_array,
)


@dataclass
class ProcessedImage:
    name: str
    original_rgb: Optional[np.ndarray]
    original_gray: np.ndarray
    denoised: np.ndarray
    sinogram: SinogramResult
    reconstruction: np.ndarray
    info: dict[str, str]

    @property
    def original_display(self) -> np.ndarray:
        if self.original_rgb is not None:
            return self.original_rgb
        return np.stack([self.original_gray] * 3, axis=-1)


@dataclass
class ReconstructionResult:
    name: str
    sinogram: SinogramResult
    reconstruction: np.ndarray
    info: dict[str, str]


def process_gray_image(
    gray: np.ndarray,
    *,
    name: str,
    rgb: Optional[np.ndarray] = None,
    progress_callback=None,
) -> ProcessedImage:
    denoised = preprocess_and_denoise(gray, progress_callback)
    sinogram = create_sinogram(denoised, progress_callback)
    reconstruction = reconstruct_image(sinogram, progress_callback)
    info = get_image_info(gray)

    return ProcessedImage(
        name=name,
        original_rgb=rgb,
        original_gray=gray,
        denoised=denoised,
        sinogram=sinogram,
        reconstruction=reconstruction,
        info=info,
    )


def process_sinogram_array(
    sinogram_img: np.ndarray,
    *,
    name: str,
    target_size: int,
    progress_callback=None,
) -> ReconstructionResult:
    shape = (int(target_size), int(target_size))
    sinogram = sinogram_from_image_array(sinogram_img, target_shape=shape)
    reconstruction = reconstruct_image(sinogram, progress_callback)
    info = get_image_info(reconstruction)

    return ReconstructionResult(
        name=name,
        sinogram=sinogram,
        reconstruction=reconstruction,
        info=info,
    )
