import streamlit as st

from app.ui.components.splash import render_splash
from app.ui.layout import render_app
from app.ui.styles import apply_global_styles


def main() -> None:
    st.set_page_config(
        page_title="xử lý ảnh CT",
        page_icon="🩻",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    apply_global_styles()
    render_splash()
    render_app()


if __name__ == "__main__":
    main()