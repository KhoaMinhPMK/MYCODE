import streamlit as st

from app.ui.components.splash import render_splash
from app.ui.layout import render_app
from app.ui.styles import apply_global_styles


def main() -> None:
    st.set_page_config(
        page_title="Xử lý ảnh CT",
        page_icon="🩻",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    apply_global_styles()
    render_splash()
    render_app()

    # Footer: link to Chatbot page (use switch_page for compatibility)
    st.divider()
    if st.button("🤖 Mở trang Chatbot", use_container_width=True):
        try:
            st.switch_page("pages/Chatbot.py")
        except Exception:
            # Fallback by page name in some Streamlit versions
            st.switch_page("Chatbot")


if __name__ == "__main__":
    main()
