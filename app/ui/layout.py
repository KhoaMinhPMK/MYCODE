from __future__ import annotations

import time
from typing import Any, Dict, List

import numpy as np
import streamlit as st

from app.services.data_loader import (
    load_dicom_image,
    load_sinogram_image,
    load_standard_image,
)
from app.services.pipeline import (
    ProcessedImage,
    ReconstructionResult,
    process_gray_image,
    process_sinogram_array,
)

from .components.controls import ControlState, render_controls
from .components.header import render_header
from .components.progress import progress_handler
from .components.results import render_reconstruction_results, render_results
from .components.settings import ensure_display_mode, render_display_settings


SESSION_KEY = "workspace_results"
PIPELINE_COUNT_KEY = "ui_pipeline_count"
RECON_COUNT_KEY = "ui_recon_count"
HISTORY_KEY = "workspace_history"


def _init_session_state() -> None:
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = {
            "pipeline": [],
            "reconstruction": [],
        }
    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = {
            "pipeline": [],
            "reconstruction": [],
        }
    if PIPELINE_COUNT_KEY not in st.session_state:
        st.session_state[PIPELINE_COUNT_KEY] = 0
    if RECON_COUNT_KEY not in st.session_state:
        st.session_state[RECON_COUNT_KEY] = 0
    ensure_display_mode()


def _status_slot(status_area: Any, title: str, subtitle: str) -> Any:
    status_area.empty()
    wrapper = status_area.container()
    wrapper.markdown(
        f"""
        <div class='status-card'>
            <span class='status-title'>{title}</span>
            <span class='status-sub'>{subtitle}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return wrapper.container()


def _process_standard_images(state: ControlState, status_area: Any) -> List[ProcessedImage]:
    processed: List[ProcessedImage] = []
    files = state.images
    total = len(files)
    if total == 0:
        return processed

    for index, uploaded_file in enumerate(files, start=1):
        with st.container():
            slot = _status_slot(
                status_area,
                "Đang xử lý ảnh",  # title
                f"{uploaded_file.name} · {index}/{total}",
            )
            try:
                rgb, gray = load_standard_image(uploaded_file)
                with progress_handler(
                    state.show_progress,
                    "Ảnh đã xử lý",
                    holder=slot,
                ) as progress:
                    result = process_gray_image(
                        gray,
                        name=uploaded_file.name,
                        rgb=rgb,
                        progress_callback=progress,
                    )
                processed.append(result)
            except Exception as exc:  # pragma: no cover - UI feedback only
                status_area.error(f"Không thể xử lý {uploaded_file.name}: {exc}")
    return processed


def _process_dicoms(state: ControlState, status_area: Any) -> List[ProcessedImage]:
    processed: List[ProcessedImage] = []
    files = state.dicoms
    total = len(files)
    if total == 0:
        return processed

    for index, uploaded_file in enumerate(files, start=1):
        with st.container():
            slot = _status_slot(
                status_area,
                "Đang xử lý DICOM",
                f"{uploaded_file.name} · {index}/{total}",
            )
            try:
                gray = load_dicom_image(uploaded_file)
                rgb = np.stack([gray] * 3, axis=-1)
                with progress_handler(
                    state.show_progress,
                    "DICOM đã xử lý",
                    holder=slot,
                ) as progress:
                    result = process_gray_image(
                        gray,
                        name=uploaded_file.name,
                        rgb=rgb,
                        progress_callback=progress,
                    )
                processed.append(result)
            except Exception as exc:  # pragma: no cover - UI feedback only
                status_area.error(f"Không thể xử lý {uploaded_file.name}: {exc}")
    return processed


def _process_webcam(state: ControlState, status_area: Any) -> List[ProcessedImage]:
    processed: List[ProcessedImage] = []
    uploaded_file = state.camera_capture
    if uploaded_file is None:
        return processed

    slot = _status_slot(status_area, "Đang xử lý Webcam", "Ảnh trực tiếp")
    try:
        rgb, gray = load_standard_image(uploaded_file)
        with progress_handler(
            state.show_progress,
            "Ảnh Webcam đã xử lý",
            holder=slot,
        ) as progress:
            result = process_gray_image(
                gray,
                name="Ảnh Webcam",
                rgb=rgb,
                progress_callback=progress,
            )
        processed.append(result)
    except Exception as exc:  # pragma: no cover - UI feedback only
        status_area.error(f"Không thể xử lý ảnh Webcam: {exc}")
    return processed


def _process_pipeline(state: ControlState, status_area: Any) -> List[ProcessedImage]:
    if state.source == "png":
        return _process_standard_images(state, status_area)
    if state.source == "dicom":
        return _process_dicoms(state, status_area)
    return _process_webcam(state, status_area)


def _process_sinograms(state: ControlState, status_area: Any) -> List[ReconstructionResult]:
    processed: List[ReconstructionResult] = []
    files = state.sinograms
    if len(files) == 0:
        return processed

    total = len(files)
    for index, uploaded_file in enumerate(files, start=1):
        slot = _status_slot(
            status_area,
            "Đang tái tạo sinogram",
            f"{uploaded_file.name} · {index}/{total}",
        )
        try:
            sinogram_array = load_sinogram_image(uploaded_file)
            with progress_handler(
                state.show_progress,
                "Hoàn tất tái tạo",
                holder=slot,
            ) as progress:
                result = process_sinogram_array(
                    sinogram_array,
                    name=uploaded_file.name,
                    target_size=state.sinogram_target,
                    progress_callback=progress,
                )
            processed.append(result)
        except Exception as exc:  # pragma: no cover - UI feedback only
            status_area.error(f"Không thể tái tạo {uploaded_file.name}: {exc}")
    return processed


def _push_notification(kind: str, title: str, message: str) -> None:
    icon_map = {
        "success": "ti ti-checks",
        "info": "ti ti-info-circle",
        "warning": "ti ti-alert-triangle",
    }
    toast_id = f"toast-{int(time.time() * 1000)}"
    icon_class = icon_map.get(kind, icon_map["info"])
    st.markdown(
        f"""
        <div class='toast-banner {kind}' id='{toast_id}'>
            <i class='{icon_class}'></i>
            <div class='toast-copy'>
                <strong>{title}</strong>
                <span>{message}</span>
            </div>
        </div>
        <script>
            const toastEl = document.getElementById('{toast_id}');
            if (toastEl) {{
                setTimeout(() => toastEl.classList.add('hide'), 3400);
                setTimeout(() => toastEl.remove(), 4200);
            }}
        </script>
        """,
        unsafe_allow_html=True,
    )


def render_app() -> None:
    _init_session_state()
    
    display_mode = render_display_settings()
    render_header()

    st.markdown("<div class='workspace-shell'>", unsafe_allow_html=True)

    status_area: Any
    results_area: Any

    if display_mode == "tabbed":
        control_tab, result_tab = st.tabs(["Bàn điều khiển", "Kết quả"])

        with control_tab:
            control_state = render_controls()

        with result_tab:
            status_area = st.container()
            results_area = st.container()
    else:
        col_controls, col_results = st.columns([1, 1.35], gap="large")
        with col_controls:
            control_state = render_controls()

        with col_results:
            status_area = st.container()
            results_area = st.container()

    workspace_state: Dict[str, List[Any]] = st.session_state[SESSION_KEY]
    if not workspace_state["pipeline"] and not workspace_state["reconstruction"]:
        status_area.markdown(
            """
            <div class='status-card idle'>
                <span class='status-title'>Sẵn sàng xử lý</span>
                <span class='status-sub'>Chọn nguồn dữ liệu và nhấn bắt đầu</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if control_state.mode == "pipeline" and control_state.process_requested:
        new_results = _process_pipeline(control_state, status_area)
        if new_results:
            # Add to history
            history: Dict[str, List[Any]] = st.session_state[HISTORY_KEY]
            history["pipeline"].extend(new_results)
            
            # Update current workspace
            workspace_state["pipeline"] = new_results
            current = len(new_results)
            _push_notification(
                "success",
                "Pipeline hoàn tất",
                f"{current} ảnh đã được xử lý thành công.",
            )
            st.session_state[PIPELINE_COUNT_KEY] = len(history["pipeline"])

    if control_state.mode == "reconstruct" and control_state.reconstruct_requested:
        new_results = _process_sinograms(control_state, status_area)
        if new_results:
            # Add to history
            history: Dict[str, List[Any]] = st.session_state[HISTORY_KEY]
            history["reconstruction"].extend(new_results)
            
            # Update current workspace
            workspace_state["reconstruction"] = new_results
            current = len(new_results)
            _push_notification(
                "success",
                "Tái tạo hoàn chỉnh",
                f"{current} sinogram đã dựng lại ảnh CT.",
            )
            st.session_state[RECON_COUNT_KEY] = len(history["reconstruction"])

    with results_area:
        result_tabs = st.tabs(["Kết quả mới nhất", "Tái tạo mới nhất", "Lịch sử đầy đủ"])
        
        with result_tabs[0]:
            render_results(workspace_state["pipeline"])
        
        with result_tabs[1]:
            render_reconstruction_results(workspace_state["reconstruction"])
        
        with result_tabs[2]:
            # History view
            history: Dict[str, List[Any]] = st.session_state[HISTORY_KEY]
            total_pipeline = len(history["pipeline"])
            total_recon = len(history["reconstruction"])
            
            st.markdown(
                f"""
                <div class='glass-section'>
                    <h3><i class='ti ti-history'></i> Lịch sử xử lý</h3>
                    <div style='display: flex; gap: 1.5rem; margin-top: 1rem;'>
                        <div>
                            <span style='font-size: 2rem; font-weight: 700; color: var(--accent-primary);'>{total_pipeline}</span>
                            <p style='margin: 0; color: var(--text-muted); font-size: 0.9rem;'>Ảnh pipeline</p>
                        </div>
                        <div>
                            <span style='font-size: 2rem; font-weight: 700; color: var(--accent-primary);'>{total_recon}</span>
                            <p style='margin: 0; color: var(--text-muted); font-size: 0.9rem;'>Sinogram tái tạo</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            if total_pipeline > 0 or total_recon > 0:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Xóa lịch sử Pipeline", use_container_width=True, type="secondary"):
                        st.session_state[HISTORY_KEY]["pipeline"] = []
                        st.session_state[SESSION_KEY]["pipeline"] = []
                        st.rerun()
                with col2:
                    if st.button("🗑️ Xóa lịch sử Reconstruction", use_container_width=True, type="secondary"):
                        st.session_state[HISTORY_KEY]["reconstruction"] = []
                        st.session_state[SESSION_KEY]["reconstruction"] = []
                        st.rerun()
            
            st.divider()
            
            history_tabs = st.tabs([f"Pipeline ({total_pipeline})", f"Reconstruction ({total_recon})"])
            with history_tabs[0]:
                if total_pipeline > 0:
                    render_results(history["pipeline"])
                else:
                    st.info("Chưa có lịch sử xử lý pipeline")
            
            with history_tabs[1]:
                if total_recon > 0:
                    render_reconstruction_results(history["reconstruction"])
                else:
                    st.info("Chưa có lịch sử tái tạo sinogram")

    st.markdown("</div>", unsafe_allow_html=True)
