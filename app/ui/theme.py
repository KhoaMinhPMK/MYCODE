from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import streamlit as st


THEME_PALETTE_KEY = "ui_theme_palette"
THEME_DARK_KEY = "ui_theme_dark"


@dataclass(frozen=True)
class ThemeTokens:
    accent_primary: str
    accent_secondary: str
    text_primary: str
    text_muted: str
    glass_background: str
    glass_border: str
    glass_shadow: str
    app_gradient_1: str
    app_gradient_2: str
    app_background: str
    surface_tint: str
    status_idle_border: str


@dataclass(frozen=True)
class ThemePalette:
    name: str
    label: str
    icon: str
    light: ThemeTokens
    dark: ThemeTokens


PALETTES: Dict[str, ThemePalette] = {
    "aurora": ThemePalette(
        name="aurora",
        label="Aurora Indigo",
        icon="ti-planet",
        light=ThemeTokens(
            accent_primary="#6E7FF3",
            accent_secondary="#9FA9FC",
            text_primary="#10172A",
            text_muted="rgba(16, 23, 42, 0.58)",
            glass_background="rgba(255, 255, 255, 0.22)",
            glass_border="rgba(255, 255, 255, 0.36)",
            glass_shadow="rgba(15, 23, 42, 0.12)",
            app_gradient_1="rgba(110, 127, 243, 0.28)",
            app_gradient_2="rgba(159, 170, 252, 0.24)",
            app_background="#f6f7fb",
            surface_tint="rgba(110, 127, 243, 0.08)",
            status_idle_border="rgba(110, 127, 243, 0.22)",
        ),
        dark=ThemeTokens(
            accent_primary="#A8B3FF",
            accent_secondary="#C4CBFF",
            text_primary="rgba(230, 235, 245, 0.92)",
            text_muted="rgba(200, 210, 230, 0.65)",
            glass_background="rgba(30, 35, 50, 0.60)",
            glass_border="rgba(160, 175, 210, 0.25)",
            glass_shadow="rgba(10, 15, 30, 0.25)",
            app_gradient_1="rgba(140, 155, 245, 0.14)",
            app_gradient_2="rgba(110, 127, 243, 0.10)",
            app_background="#1a1f2e",
            surface_tint="rgba(159, 169, 252, 0.10)",
            status_idle_border="rgba(159, 169, 252, 0.22)",
        ),
    ),
    "solaris": ThemePalette(
        name="solaris",
        label="Solaris Ember",
        icon="ti-sun-high",
        light=ThemeTokens(
            accent_primary="#FF7B54",
            accent_secondary="#FFB26B",
            text_primary="#251605",
            text_muted="rgba(37, 22, 5, 0.6)",
            glass_background="rgba(255, 255, 255, 0.24)",
            glass_border="rgba(255, 201, 170, 0.5)",
            glass_shadow="rgba(243, 148, 93, 0.15)",
            app_gradient_1="rgba(255, 179, 123, 0.28)",
            app_gradient_2="rgba(255, 123, 84, 0.22)",
            app_background="#FFF6EF",
            surface_tint="rgba(255, 123, 84, 0.1)",
            status_idle_border="rgba(255, 123, 84, 0.28)",
        ),
        dark=ThemeTokens(
            accent_primary="#FFB896",
            accent_secondary="#FFCFB3",
            text_primary="rgba(240, 230, 220, 0.92)",
            text_muted="rgba(220, 205, 190, 0.65)",
            glass_background="rgba(40, 28, 22, 0.58)",
            glass_border="rgba(220, 170, 140, 0.24)",
            glass_shadow="rgba(20, 10, 5, 0.25)",
            app_gradient_1="rgba(255, 150, 110, 0.12)",
            app_gradient_2="rgba(220, 120, 80, 0.08)",
            app_background="#221812",
            surface_tint="rgba(255, 164, 110, 0.08)",
            status_idle_border="rgba(255, 164, 110, 0.24)",
        ),
    ),
    "viridian": ThemePalette(
        name="viridian",
        label="Viridian Bloom",
        icon="ti-leaf",
        light=ThemeTokens(
            accent_primary="#32A071",
            accent_secondary="#9DD9A3",
            text_primary="#062919",
            text_muted="rgba(6, 41, 25, 0.55)",
            glass_background="rgba(255, 255, 255, 0.24)",
            glass_border="rgba(173, 225, 198, 0.5)",
            glass_shadow="rgba(18, 90, 60, 0.2)",
            app_gradient_1="rgba(50, 160, 113, 0.3)",
            app_gradient_2="rgba(157, 217, 163, 0.24)",
            app_background="#F3FBF7",
            surface_tint="rgba(50, 160, 113, 0.1)",
            status_idle_border="rgba(50, 160, 113, 0.26)",
        ),
        dark=ThemeTokens(
            accent_primary="#88D9B8",
            accent_secondary="#A8EBCD",
            text_primary="rgba(230, 245, 240, 0.92)",
            text_muted="rgba(200, 230, 220, 0.65)",
            glass_background="rgba(18, 35, 28, 0.58)",
            glass_border="rgba(140, 210, 180, 0.24)",
            glass_shadow="rgba(8, 20, 15, 0.25)",
            app_gradient_1="rgba(90, 200, 150, 0.12)",
            app_gradient_2="rgba(60, 160, 110, 0.08)",
            app_background="#141f1a",
            surface_tint="rgba(80, 192, 136, 0.08)",
            status_idle_border="rgba(102, 214, 162, 0.24)",
        ),
    ),
    "celeste": ThemePalette(
        name="celeste",
        label="Celeste Haze",
        icon="ti-moon-stars",
        light=ThemeTokens(
            accent_primary="#8B75F5",
            accent_secondary="#C7A8FF",
            text_primary="#160F30",
            text_muted="rgba(22, 15, 48, 0.58)",
            glass_background="rgba(255, 255, 255, 0.26)",
            glass_border="rgba(214, 206, 255, 0.5)",
            glass_shadow="rgba(63, 46, 138, 0.18)",
            app_gradient_1="rgba(139, 117, 245, 0.3)",
            app_gradient_2="rgba(199, 168, 255, 0.25)",
            app_background="#F8F6FF",
            surface_tint="rgba(139, 117, 245, 0.1)",
            status_idle_border="rgba(139, 117, 245, 0.26)",
        ),
        dark=ThemeTokens(
            accent_primary="#C5B3FF",
            accent_secondary="#DDD1FF",
            text_primary="rgba(240, 235, 250, 0.93)",
            text_muted="rgba(215, 205, 235, 0.66)",
            glass_background="rgba(28, 22, 45, 0.60)",
            glass_border="rgba(180, 165, 235, 0.26)",
            glass_shadow="rgba(12, 8, 20, 0.28)",
            app_gradient_1="rgba(150, 130, 240, 0.14)",
            app_gradient_2="rgba(110, 85, 200, 0.10)",
            app_background="#18121f",
            surface_tint="rgba(155, 132, 252, 0.10)",
            status_idle_border="rgba(180, 160, 255, 0.26)",
        ),
    ),
}


def ensure_theme_state() -> None:
    if THEME_PALETTE_KEY not in st.session_state:
        st.session_state[THEME_PALETTE_KEY] = "celeste"  # Màu tím làm mặc định
    if THEME_DARK_KEY not in st.session_state:
        st.session_state[THEME_DARK_KEY] = False


def get_active_palette() -> ThemePalette:
    ensure_theme_state()
    palette_id: str = st.session_state[THEME_PALETTE_KEY]
    return PALETTES.get(palette_id, PALETTES["celeste"])


def get_active_tokens() -> ThemeTokens:
    palette = get_active_palette()
    dark_mode = bool(st.session_state.get(THEME_DARK_KEY, False))
    return palette.dark if dark_mode else palette.light


def apply_theme_tokens() -> None:
    tokens = get_active_tokens()
    css = f"""
    <style>
    :root {{
        --accent-primary: {tokens.accent_primary};
        --accent-secondary: {tokens.accent_secondary};
        --text-primary: {tokens.text_primary};
        --text-muted: {tokens.text_muted};
        --glass-bg: {tokens.glass_background};
        --glass-border: {tokens.glass_border};
        --glass-shadow: {tokens.glass_shadow};
        --app-gradient-1: {tokens.app_gradient_1};
        --app-gradient-2: {tokens.app_gradient_2};
        --app-bg-solid: {tokens.app_background};
        --surface-tint: {tokens.surface_tint};
        --status-idle-border: {tokens.status_idle_border};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def set_palette(palette_id: str) -> None:
    ensure_theme_state()
    if palette_id in PALETTES:
        st.session_state[THEME_PALETTE_KEY] = palette_id


def set_dark_mode(enabled: bool) -> None:
    ensure_theme_state()
    st.session_state[THEME_DARK_KEY] = enabled


def active_palette_name() -> str:
    ensure_theme_state()
    return st.session_state[THEME_PALETTE_KEY]


def dark_mode_enabled() -> bool:
    ensure_theme_state()
    return bool(st.session_state[THEME_DARK_KEY])


def palette_options() -> Dict[str, ThemePalette]:
    return PALETTES