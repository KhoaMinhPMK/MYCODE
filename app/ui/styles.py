import streamlit as st

from app.ui.theme import apply_theme_tokens, ensure_theme_state


IOS_GLASS_STYLES = """
    <style>
    @import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.47.0/tabler-icons.min.css');

    :root {
        --glass-bg: rgba(255, 255, 255, 0.22);
        --glass-border: rgba(255, 255, 255, 0.35);
        --glass-shadow: rgba(15, 23, 42, 0.12);
        --accent-primary: #6E7FF3;
        --accent-secondary: #9FAAFC;
        --text-primary: #0F172A;
        --text-muted: rgba(15, 23, 42, 0.55);
        --app-gradient-1: rgba(110, 127, 243, 0.28);
        --app-gradient-2: rgba(159, 170, 252, 0.24);
        --app-bg-solid: #F6F7FB;
        --surface-tint: rgba(110, 127, 243, 0.08);
        --status-idle-border: rgba(110, 127, 243, 0.22);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 12% 18%, var(--app-gradient-1), transparent 45%),
            radial-gradient(circle at 78% 6%, var(--app-gradient-2), transparent 40%),
            var(--app-bg-solid);
        font-family: "SF Pro Display", "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
        color: var(--text-primary);
    }

    [data-testid="stAppViewContainer"] .main {
        padding: 2.5rem 3.5rem 3rem;
    }

    body.splash-active {
        overflow: hidden;
    }

    /* CSS-only splash screen with auto-dismiss */
    .splash-screen-css {
        position: fixed;
        inset: 0;
        background: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: splashFadeOut 0.4s ease 2.2s forwards;
    }

    @keyframes splashFadeOut {
        to {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
    }

    .splash-progress-bar-css {
        width: 0;
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(135deg, #6E7FF3, #9FA9FC);
        animation: splashProgress 2s ease-out forwards;
    }

    @keyframes splashProgress {
        0% { width: 0%; }
        100% { width: 100%; }
    }

    .splash-screen {
        position: fixed;
        inset: 0;
        background: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        transition: opacity 0.45s ease, visibility 0.45s ease;
    }

    .splash-screen.is-hidden {
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
    }

    .splash-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.2rem;
        padding: 2.4rem 3rem;
        border-radius: 32px;
        box-shadow: 0 32px 56px rgba(15, 23, 42, 0.16);
        background: #ffffff;
        border: 1px solid rgba(15, 23, 42, 0.05);
    }

    .splash-logo {
        font-size: 3.4rem;
        font-weight: 700;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        color: #111827;
        font-family: "Inter", "SF Pro Display", "Segoe UI", sans-serif;
    }

    .splash-progress-wrap {
        position: relative;
        width: 260px;
        height: 6px;
        border-radius: 999px;
        background: rgba(17, 24, 39, 0.08);
        overflow: hidden;
    }

    .splash-progress-bar {
        width: 0;
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(135deg, #6E7FF3, #9FA9FC);
        transition: width 0.12s ease-out;
    }
    
    .splash-bar-animate {
        animation: none;
    }

    .splash-progress-text {
        font-size: 0.92rem;
        font-weight: 600;
        color: rgba(17, 24, 39, 0.72);
        letter-spacing: 0.12em;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        letter-spacing: -0.02em;
    }

    .glass-section {
        border-radius: 24px;
        background: var(--glass-bg);
        backdrop-filter: blur(24px) saturate(150%);
        border: 1px solid var(--glass-border);
        box-shadow: 0 20px 42px var(--glass-shadow);
        padding: 1.75rem 2rem;
        margin-bottom: 1.5rem;
    }

    [data-testid="stVerticalBlock"] > div:has(.glass-section) {
        padding: 0 !important;
    }

    .hero-card {
        margin-bottom: 2rem;
    }

    .hero-card h1 {
        font-size: 2.4rem;
        margin-bottom: 0.75rem;
    }

    .hero-card p {
        font-size: 1.05rem;
        color: var(--text-muted);
        margin-bottom: 1.4rem;
        line-height: 1.55rem;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.45rem 1.1rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.6);
        border: 1px solid rgba(255,255,255,0.8);
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 1rem;
    }

    .hero-badge .ti {
        font-size: 1rem;
        color: var(--accent-primary);
    }

    .hero-highlights {
        display: grid;
        gap: 0.65rem;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }

    .hero-highlights div {
        border-radius: 16px;
        padding: 0.65rem 0.9rem;
        background: rgba(255,255,255,0.55);
        border: 1px solid rgba(255,255,255,0.4);
        font-size: 0.92rem;
        color: var(--text-muted);
        backdrop-filter: blur(18px);
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .hero-highlights .ti {
        font-size: 1.1rem;
        color: var(--accent-primary);
    }

    .control-panel {
        padding: 1.5rem 1.75rem;
    }

    .settings-bar {
        display: flex;
        justify-content: flex-end;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }

    .settings-bar [data-testid="stPopoverTrigger"] > button {
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.5);
        background: rgba(255,255,255,0.72);
        color: var(--text-muted);
        font-weight: 600;
        padding: 0.6rem 1.35rem;
        backdrop-filter: blur(14px);
        transition: transform 0.25s ease, box-shadow 0.25s ease, color 0.25s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
    }

    .settings-bar [data-testid="stPopoverTrigger"] > button .ti {
        font-size: 1rem;
    }

    .settings-bar [data-testid="stPopoverTrigger"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.12);
        color: var(--accent-primary);
    }

    .settings-popover {
        padding: 0.2rem 0.4rem 0.8rem;
    }

    .settings-section-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: var(--text-primary);
    }

    .settings-section-title .ti {
        font-size: 1.1rem;
        color: var(--accent-primary);
    }

    .settings-popover [data-baseweb="radio"] > div {
        gap: 0.5rem;
    }

    .settings-popover [data-baseweb="radio"] label {
        border-radius: 14px;
        padding: 0.65rem 1rem;
        background: rgba(255,255,255,0.65);
        border: 1px solid rgba(255,255,255,0.55);
        font-weight: 600;
        color: var(--text-muted);
        transition: all 0.25s ease;
    }

    .settings-popover [data-baseweb="radio"] div[role="radio"][aria-checked="true"] label {
        border-color: rgba(0, 0, 0, 0.06);
        background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(255,255,255,0.72));
        color: var(--accent-primary);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
    }

    .settings-popover .stToggle label {
        font-weight: 600;
        color: var(--text-primary);
    }

    .settings-preview-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.5rem;
        margin: 0.5rem 0 0.75rem;
    }

    .settings-preview-grid.compact {
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    }

    .settings-preview-card {
        border-radius: 14px;
        padding: 0.65rem 0.8rem;
        background: rgba(255,255,255,0.55);
        border: 1px solid rgba(255,255,255,0.4);
        display: flex;
        align-items: center;
        gap: 0.55rem;
        color: var(--text-muted);
        font-weight: 600;
        transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease;
    }

    .settings-preview-card.active {
        color: var(--accent-primary);
        border-color: var(--accent-primary);
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
        background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(255,255,255,0.68));
    }

    .settings-preview-card .ti {
        font-size: 1.1rem;
        color: var(--accent-primary);
    }

    .mode-selector {
        margin-bottom: 0.4rem;
    }

    .mode-card-stack {
        display: grid;
        gap: 0.6rem;
    }

    .mode-card {
        border-radius: 18px;
        padding: 0.75rem 1rem;
        background: rgba(255,255,255,0.55);
        border: 1px solid rgba(255,255,255,0.4);
        display: flex;
        gap: 0.75rem;
        align-items: center;
        transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease;
    }

    .mode-card.active {
        background: var(--surface-tint);
        border-color: var(--accent-primary);
        box-shadow: 0 18px 36px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }

    .mode-card i {
        font-size: 1.4rem;
        color: var(--accent-primary);
    }

    .mode-card h4 {
        margin: 0;
        font-size: 1.05rem;
        color: var(--text-primary);
    }

    .mode-card p {
        margin: 0.2rem 0 0;
        font-size: 0.88rem;
        color: var(--text-muted);
    }

    .section-heading,
    .section-subtitle {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1.05rem;
        margin-bottom: 0.8rem;
    }

    .section-subtitle {
        font-size: 1rem;
        margin-top: 0.6rem;
        margin-bottom: 0.75rem;
    }

    .section-heading .ti,
    .section-subtitle .ti {
        font-size: 1.1rem;
        color: var(--accent-primary);
    }

    .section-heading span,
    .section-subtitle span {
        line-height: 1;
    }

    .source-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.85rem;
        margin-bottom: 1.1rem;
    }

    .source-card {
        border-radius: 18px;
        padding: 1rem 1.1rem;
        background: rgba(255,255,255,0.55);
        border: 1px solid rgba(255,255,255,0.4);
        display: flex;
        gap: 0.9rem;
        align-items: flex-start;
        transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease;
    }

    .source-card.active {
        border-color: var(--accent-primary);
        background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(255,255,255,0.65));
        box-shadow: 0 18px 36px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }

    .source-card i {
        font-size: 1.3rem;
        color: var(--accent-primary);
        line-height: 1.6rem;
    }

    .source-card h5 {
        margin: 0;
        font-size: 1rem;
        color: var(--text-primary);
    }

    .source-card p {
        margin: 0.35rem 0 0;
        font-size: 0.85rem;
        color: var(--text-muted);
        line-height: 1.35rem;
    }

    .control-panel [data-testid="stRadio"] > div {
        display: inline-flex;
        gap: 0.6rem;
        background: rgba(255,255,255,0.55);
        border-radius: 18px;
        padding: 0.35rem;
    }

    .control-panel [data-testid="stRadio"] label {
        flex: 1;
        border-radius: 14px;
        padding: 0.55rem 1rem;
        font-weight: 600;
        color: var(--text-muted);
        text-align: center;
    }

    .control-panel [data-testid="stRadio"] div[role="radio"][aria-checked="true"] label {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white;
        box-shadow: 0 10px 22px rgba(0, 0, 0, 0.15);
    }

    .hint-text {
        display: inline-block;
        font-size: 0.85rem;
        color: var(--text-muted);
    }

    .control-tips {
        padding: 1.4rem 1.6rem;
    }

    .control-tips h4 {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.85rem;
        color: var(--text-primary);
    }

    .control-tips h4 .ti {
        color: var(--accent-primary);
    }

    .control-tips ul {
        padding-left: 1.2rem;
        color: var(--text-muted);
    }

    .stButton>button {
        width: 100%;
        padding: 0.85rem 1.05rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.4);
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white;
        font-weight: 600;
        letter-spacing: 0.01em;
        backdrop-filter: blur(20px);
        transition: transform 0.28s ease, box-shadow 0.28s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 36px rgba(0, 0, 0, 0.18);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.45);
        border-radius: 16px;
        padding: 0.6rem 1.3rem;
        border: 1px solid rgba(255,255,255,0.35);
        color: var(--text-muted);
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: var(--surface-tint) !important;
        color: var(--accent-primary) !important;
        border-color: var(--status-idle-border) !important;
    }

    .status-card {
        border-radius: 20px;
        padding: 1rem 1.4rem;
        background: rgba(255,255,255,0.6);
        border: 1px solid rgba(255,255,255,0.5);
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        backdrop-filter: blur(16px);
        margin-bottom: 1.2rem;
    }

    .status-card.idle {
        background: var(--surface-tint);
        border: 1px dashed var(--status-idle-border);
    }

    .status-title {
        font-weight: 600;
        letter-spacing: 0.01em;
    }

    .status-sub {
        font-size: 0.9rem;
        color: var(--text-muted);
    }

    .result-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        background: var(--surface-tint);
        color: var(--accent-primary);
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .result-badge .ti {
        font-size: 0.95rem;
    }

    .image-container {
        position: relative;
        display: inline-block;
        width: 100%;
    }

    .download-overlay-btn {
        position: absolute;
        top: 0.75rem;
        right: 0.75rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 12px;
        padding: 0.5rem 0.65rem;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
        z-index: 10;
    }

    .download-overlay-btn:hover {
        background: rgba(255, 255, 255, 1);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.25);
    }

    .download-overlay-btn i {
        color: var(--accent-primary);
        font-size: 1.1rem;
    }

    div[data-testid="stFileUploader"] section {
        padding: 1.1rem;
        border-radius: 18px;
        border: 1px dashed var(--status-idle-border);
        background: var(--surface-tint);
        backdrop-filter: blur(16px);
    }

    [data-testid="stProgress"] div[data-testid="stProgressBarFill"] {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    }

    [data-testid="stMetricValue"] {
        font-size: 1.25rem;
    }

    .toast-banner {
        position: fixed;
        right: 2.5rem;
        bottom: 2.5rem;
        border-radius: 18px;
        padding: 1rem 1.2rem;
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(255,255,255,0.6);
        box-shadow: 0 24px 48px rgba(0,0,0,0.14);
        display: flex;
        gap: 0.75rem;
        align-items: center;
        z-index: 9000;
        color: var(--text-primary);
        transition: transform 0.4s ease, opacity 0.4s ease;
    }

    .toast-banner i {
        font-size: 1.35rem;
        color: var(--accent-primary);
    }

    .toast-banner.hide {
        opacity: 0;
        transform: translateY(25px);
    }

    .toast-banner.success {
        border-color: rgba(76, 175, 80, 0.35);
    }

    .toast-banner .toast-copy {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
    }

    .toast-banner .toast-copy strong {
        font-size: 0.95rem;
        font-weight: 700;
    }

    .toast-banner .toast-copy span {
        font-size: 0.85rem;
        color: var(--text-muted);
    }

    /* Music Player Styles */
    #music-player-container {
        display: none;
    }

    [data-testid="stPopover"] button[data-baseweb="popover-trigger"] {
        transition: all 0.2s ease;
    }

    [data-testid="stPopover"] button[data-baseweb="popover-trigger"]:hover {
        transform: scale(1.05);
    }

    /* Welcome Popup Styles */
    .welcome-overlay-bg {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(12px);
        z-index: 1;
        animation: fadeIn 0.4s ease;
    }

    .welcome-dialog {
        position: relative;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(24px);
        border-radius: 32px;
        padding: 3rem 2.5rem 2rem 2.5rem;
        text-align: center;
        box-shadow: 0 32px 64px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.9);
        animation: slideUp 0.5s ease;
        z-index: 10000;
        margin-bottom: 1.5rem;
    }

    .welcome-dialog h2 {
        margin: 0 0 1rem 0;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .welcome-dialog p {
        margin: 0;
        font-size: 1.1rem;
        line-height: 1.6;
        color: var(--text-secondary);
    }
    </style>
"""


def apply_global_styles() -> None:
    ensure_theme_state()
    st.markdown(IOS_GLASS_STYLES, unsafe_allow_html=True)
    apply_theme_tokens()
