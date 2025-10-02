from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


@dataclass
class ControlState:
    mode: str
    source: str
    images: List[UploadedFile]
    dicoms: List[UploadedFile]
    camera_capture: Optional[UploadedFile]
    sinograms: List[UploadedFile]
    sinogram_target: int
    show_progress: bool
    auto_process: bool
    process_requested: bool
    reconstruct_requested: bool


SOURCE_OPTIONS = {
    "Ảnh chuẩn 2D": "png",
    "Chuỗi DICOM": "dicom",
    "Camera trực tiếp": "webcam",
}

MODE_META = {
    "pipeline": {
        "name": "Pipeline Studio",
        "description": "Xử lý đầy đủ: khử nhiễu, tạo sinogram, tái tạo CT.",
        "icon": "ti-aperture",
    },
    "reconstruct": {
        "name": "Sinogram Lab",
        "description": "Đón sinogram có sẵn và dựng lát cắt tức thì.",
        "icon": "ti-wave-sine",
    },
}


def _render_mode_panel() -> str:
    mode_switch_col, mode_cards_col = st.columns([0.45, 1.25])

    with mode_switch_col:
        mode_toggle = st.toggle(
            "Bật Sinogram Lab",
            value=st.session_state.get("mode_switch", False),
            key="mode_switch",
        )

    current_mode = "reconstruct" if mode_toggle else "pipeline"

    cards_html = []
    for key, meta in MODE_META.items():
        state_class = " active" if current_mode == key else ""
        cards_html.append(
            f"""<article class='mode-card{state_class}'>
<i class='ti {meta['icon']}'></i>
<div>
<h4>{meta['name']}</h4>
<p>{meta['description']}</p>
</div>
</article>"""
        )

    with mode_cards_col:
        st.markdown("<div class='mode-card-stack'>" + "".join(cards_html) + "</div>", unsafe_allow_html=True)

    return current_mode


def render_controls() -> ControlState:
    mode = _render_mode_panel()

    st.divider()

    show_progress = st.toggle("Hiển thị thanh tiến trình", value=True, key="toggle_progress")

    images: List[UploadedFile] = []
    dicoms: List[UploadedFile] = []
    camera_capture: Optional[UploadedFile] = None
    sinograms: List[UploadedFile] = []
    sinogram_target = 256
    auto_process = False
    process_requested = False
    reconstruct_requested = False

    if mode == "pipeline":
        st.markdown("<div class='section-heading'><i class='ti ti-database'></i><span>Kho dữ liệu đầu vào</span></div>", unsafe_allow_html=True)
        
        # Render source selector as 3 buttons
        source_cols = st.columns(3)
        source_key = st.session_state.get("selected_source", "png")
        
        for idx, (source_label, source_value) in enumerate(SOURCE_OPTIONS.items()):
            with source_cols[idx]:
                is_active = source_value == source_key
                button_type = "primary" if is_active else "secondary"
                if st.button(
                    source_label,
                    key=f"source_btn_{source_value}",
                    use_container_width=True,
                    type=button_type,
                ):
                    source_key = source_value
                    st.session_state["selected_source"] = source_value

        col_auto, col_note = st.columns([1, 1.2])
        with col_auto:
            auto_process = st.toggle("Tự động xử lý sau khi tải", value=False, key="toggle_auto")
        with col_note:
            st.markdown(
                "<span class='hint-text'>Chế độ tự động hữu ích khi xử lý nhiều ảnh nhỏ.</span>",
                unsafe_allow_html=True,
            )

        st.divider()

        if source_key == "png":
            st.markdown("<div class='section-subtitle'><i class='ti ti-folders'></i><span>Tải ảnh chuẩn</span></div>", unsafe_allow_html=True)
            images = st.file_uploader(
                "Chọn ảnh PNG/JPG",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                label_visibility="collapsed",
            ) or []
        elif source_key == "dicom":
            st.markdown("<div class='section-subtitle'><i class='ti ti-file-dicom'></i><span>Tải file DICOM</span></div>", unsafe_allow_html=True)
            dicoms = st.file_uploader(
                "Chọn file DICOM (.dcm)",
                type=["dcm"],
                accept_multiple_files=True,
                label_visibility="collapsed",
            ) or []
        else:
            st.markdown("<div class='section-subtitle'><i class='ti ti-camera-bolt'></i><span>Chụp trực tiếp</span></div>", unsafe_allow_html=True)
            camera_capture = st.camera_input("Nhấn để chụp", label_visibility="collapsed")

        if source_key == "png":
            process_requested = auto_process and len(images) > 0
            if not auto_process:
                process_requested = st.button("Bắt đầu xử lý ảnh", use_container_width=True)
        elif source_key == "dicom":
            process_requested = auto_process and len(dicoms) > 0
            if not auto_process:
                process_requested = st.button("Bắt đầu xử lý DICOM", use_container_width=True)
        else:
            process_requested = auto_process and camera_capture is not None
            if not auto_process:
                process_requested = st.button("Xử lý ảnh webcam", use_container_width=True)
    else:
        source_key = "sinogram"
        st.markdown("<div class='section-heading'><i class='ti ti-wave-sine'></i><span>Phòng tái tạo sinogram</span></div>", unsafe_allow_html=True)
        sinograms = st.file_uploader(
            "Chọn sinogram (PNG/JPG/TIFF hoặc .npy)",
            type=["png", "jpg", "jpeg", "tif", "tiff", "npy"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="sinogram_uploader",
        ) or []

        sinogram_target = st.slider(
            "Kích thước ảnh tái tạo",
            min_value=128,
            max_value=512,
            value=256,
            step=32,
        )

        reconstruct_requested = st.button("Tái tạo sinogram", use_container_width=True)

    st.markdown(
        """
        <div class='control-tips glass-section'>
            <h4><i class='ti ti-bulb'></i> Mẹo thao tác nhanh</h4>
            <ul>
                <li>Dùng batch nhỏ để dễ dàng so sánh trước/sau theo từng lô.</li>
                <li>Ghi chú góc chụp khi tải sinogram để đối chiếu với kết quả tái tạo.</li>
                <li>Tối ưu kích thước tái tạo theo mục tiêu: 256 cho duyệt nhanh, 512 cho báo cáo.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return ControlState(
        mode=mode,
        source=source_key,
        images=list(images),
        dicoms=list(dicoms),
        camera_capture=camera_capture,
        sinograms=list(sinograms),
        sinogram_target=sinogram_target,
        show_progress=show_progress,
        auto_process=auto_process,
        process_requested=process_requested,
        reconstruct_requested=reconstruct_requested,
    )
