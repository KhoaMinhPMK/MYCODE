from __future__ import annotations

from io import BytesIO
from typing import Iterable

import numpy as np
import streamlit as st
from PIL import Image

from app.services.pipeline import ProcessedImage, ReconstructionResult


def _image_to_bytes(img_array: np.ndarray, format: str = "PNG") -> bytes:
    """Convert numpy array to image bytes for download."""
    if img_array.dtype != np.uint8:
        img_normalized = (
            (img_array - img_array.min()) / (img_array.max() - img_array.min()) * 255
        ).astype(np.uint8)
    else:
        img_normalized = img_array

    if len(img_normalized.shape) == 2:
        pil_img = Image.fromarray(img_normalized, mode="L")
    else:
        pil_img = Image.fromarray(img_normalized, mode="RGB")

    buf = BytesIO()
    pil_img.save(buf, format=format)
    return buf.getvalue()


def _render_image_with_download(
    img_array: np.ndarray,
    caption: str,
    filename: str,
    key_suffix: str,
) -> None:
    """Render image with overlay download button."""
    import base64

    img_bytes = _image_to_bytes(img_array)
    b64 = base64.b64encode(img_bytes).decode()

    container_id = f"img-container-{key_suffix}"

    st.markdown(
        f"""
        <div class='image-container' id='{container_id}'>
            <a href="data:image/png;base64,{b64}" download="{filename}" class='download-overlay-btn' title='Tải xuống'>
                <i class='ti ti-download'></i>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image(img_array, caption=caption, use_container_width=True, clamp=True)


def _render_image_metrics(info: dict[str, str]) -> None:
    cols = st.columns(len(info))
    for (key, value), col in zip(info.items(), cols):
        with col:
            st.metric(key, value)


def _render_result_card(result: ProcessedImage, index: int, total: int) -> None:
    st.markdown(
        f"""
        <div class='glass-section'>
            <div style='display:flex; justify-content: space-between; align-items:center; margin-bottom: 0.5rem;'>
                <div class='result-badge'><i class='ti ti-stack-2'></i>Ảnh {index}/{total}</div>
                <h3 style='margin:0;'>{result.name}</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        _render_image_metrics(result.info)

    primary_cols = st.columns(2, gap="medium")
    with primary_cols[0]:
        _render_image_with_download(
            result.original_display,
            "Ảnh gốc",
            f"{result.name}_original.png",
            f"orig_{index}"
        )
        _render_image_with_download(
            result.denoised,
            "Sau khử nhiễu",
            f"{result.name}_denoised.png",
            f"denoised_{index}"
        )

    with primary_cols[1]:
        _render_image_with_download(
            result.sinogram.image,
            "Sinogram tạo mới",
            f"{result.name}_sinogram.png",
            f"sino_{index}"
        )
        _render_image_with_download(
            result.reconstruction,
            "Lát cắt tái tạo",
            f"{result.name}_reconstruction.png",
            f"recon_{index}"
        )

    with st.expander("Đối chiếu nhanh", expanded=False):
        compare_cols = st.columns(2)
        with compare_cols[0]:
            st.image(result.original_display, caption="Trước xử lý", use_container_width=True, clamp=True)
        with compare_cols[1]:
            st.image(result.denoised, caption="Sau xử lý", use_container_width=True, clamp=True)


def render_results(results: Iterable[ProcessedImage]) -> None:
    results = list(results)
    if not results:
        st.markdown(
            """
            <div class='glass-section'>
                <h3>Chưa có dữ liệu</h3>
                <p>Tải ảnh hoặc chụp ảnh để bắt đầu quy trình xử lý.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    total = len(results)
    for idx, result in enumerate(results, start=1):
        _render_result_card(result, idx, total)
        if idx < total:
            st.divider()


def render_reconstruction_results(results: Iterable[ReconstructionResult]) -> None:
    results = list(results)
    if not results:
        st.markdown(
            """
            <div class='glass-section'>
                <h3>Chưa có sinogram</h3>
                <p>Tải sinogram ở bảng điều khiển bên trái để tái tạo ảnh CT.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    total = len(results)
    for idx, result in enumerate(results, start=1):
        st.markdown(
            f"""
            <div class='glass-section'>
                <div style='display:flex; justify-content: space-between; align-items:center; margin-bottom: 0.5rem;'>
                    <div class='result-badge'><i class='ti ti-wave-sine'></i>Sinogram {idx}/{total}</div>
                    <h3 style='margin:0;'>{result.name}</h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        recon_cols = st.columns([1, 1], gap="medium")
        with recon_cols[0]:
            _render_image_with_download(
                result.sinogram.image,
                "Sinogram tải lên",
                f"{result.name}_sinogram_input.png",
                f"sino_in_{idx}"
            )
        with recon_cols[1]:
            _render_image_with_download(
                result.reconstruction,
                "Kết quả tái tạo",
                f"{result.name}_reconstructed.png",
                f"recon_out_{idx}"
            )

        with st.expander("Thông số tái tạo", expanded=False):
            _render_image_metrics(result.info)

        if idx < total:
            st.divider()

