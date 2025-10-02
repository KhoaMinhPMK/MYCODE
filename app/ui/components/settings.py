from __future__ import annotations

from typing import List, Tuple

import streamlit as st

from app.ui.theme import (
    active_palette_name,
    apply_theme_tokens,
    dark_mode_enabled,
    palette_options,
    set_dark_mode,
    set_palette,
)


DISPLAY_MODE_KEY = "ui_display_mode"

_MODE_ORDER: Tuple[str, ...] = ("tabbed", "split")

DISPLAY_METADATA = {
    "tabbed": {
        "label": "Tab điều phối",
        "description": "Điều khiển và kết quả ở hai tab riêng biệt",
        "icon": "ti-layout-dashboard",
    },
    "split": {
        "label": "Song song",
        "description": "Xem điều khiển và kết quả cùng lúc",
        "icon": "ti-columns",
    },
}


def ensure_display_mode() -> str:
    if DISPLAY_MODE_KEY not in st.session_state:
        st.session_state[DISPLAY_MODE_KEY] = "tabbed"
    return st.session_state[DISPLAY_MODE_KEY]


def _mode_selector(current_mode: str) -> str:
    options: List[str] = list(_MODE_ORDER)
    return st.radio(
        "Bố cục làm việc",
        options=options,
        index=options.index(current_mode),
        horizontal=True,
        key="layout_mode_selector",
        format_func=lambda value: DISPLAY_METADATA[value]["label"],
    )


def _palette_selector(active_palette: str) -> str:
    palette_map = palette_options()
    palette_ids: List[str] = list(palette_map.keys())
    return st.radio(
        "Bảng màu",
        options=palette_ids,
        index=palette_ids.index(active_palette),
        key="palette_selector",
        format_func=lambda value: palette_map[value].label,
    )


def render_display_settings() -> str:
    current_mode = ensure_display_mode()
    palette_key = active_palette_name()
    is_dark_mode = dark_mode_enabled()

    st.markdown("<div class='settings-bar'>", unsafe_allow_html=True)
    spacer, trigger = st.columns([1, 0.2])
    with trigger:
        settings_popover = st.popover("Tuỳ chỉnh giao diện", use_container_width=True)
        with settings_popover:
            st.markdown("<div class='settings-popover'>", unsafe_allow_html=True)
            st.markdown("<h4 class='settings-section-title'><i class='ti ti-adjustments'></i> Bố cục làm việc</h4>", unsafe_allow_html=True)
            
            # Render clickable layout mode buttons
            layout_cols = st.columns(2)
            updated_mode = current_mode
            for idx, mode_value in enumerate(_MODE_ORDER):
                meta = DISPLAY_METADATA[mode_value]
                with layout_cols[idx]:
                    is_active = mode_value == current_mode
                    button_type = "primary" if is_active else "secondary"
                    if st.button(
                        f"{meta['label']}",
                        key=f"layout_btn_{mode_value}",
                        use_container_width=True,
                        type=button_type,
                    ):
                        updated_mode = mode_value
            
            st.caption(DISPLAY_METADATA[updated_mode]["description"])

            st.divider()
            st.markdown("<h4 class='settings-section-title'><i class='ti ti-color-swatch'></i> Chủ đề</h4>", unsafe_allow_html=True)
            
            # Render clickable palette cards
            palette_map = palette_options()
            palette_cols = st.columns(4)
            
            selected_palette = palette_key
            for idx, (palette_id, palette) in enumerate(palette_map.items()):
                with palette_cols[idx]:
                    is_active = palette_id == palette_key
                    button_type = "primary" if is_active else "secondary"
                    # Create button with icon
                    button_label = f"{palette.label}"
                    if st.button(
                        button_label,
                        key=f"palette_btn_{palette_id}",
                        use_container_width=True,
                        type=button_type,
                    ):
                        selected_palette = palette_id
            
            st.caption("Thay đổi sắc độ để phù hợp môi trường trình chiếu hoặc sở thích cá nhân")

            st.divider()
            dark_enabled = st.toggle("Kích hoạt Dark Mode", value=is_dark_mode, key="dark_mode_toggle")
            st.caption("Giảm chói khi làm việc trong phòng tối hoặc buổi đêm")
            
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if updated_mode != current_mode:
        st.session_state[DISPLAY_MODE_KEY] = updated_mode

    if selected_palette != palette_key:
        set_palette(selected_palette)

    if dark_enabled != is_dark_mode:
        set_dark_mode(dark_enabled)

    apply_theme_tokens()
    return st.session_state[DISPLAY_MODE_KEY]
