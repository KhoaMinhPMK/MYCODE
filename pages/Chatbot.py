import streamlit as st

from app.ui.styles import apply_global_styles
from app.ui.components.chatbot import render_chatbot


def main() -> None:
    st.set_page_config(
        page_title="Chatbot CT",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    apply_global_styles()

    st.markdown("<div class='glass-section'>", unsafe_allow_html=True)
    st.markdown("<h2><i class='ti ti-robot'></i> Chatbot Kiến Thức</h2>", unsafe_allow_html=True)
    st.caption("Chat chỉ trả lời trong phạm vi chủ đề đã biên soạn; bật nghiên cứu web/Groq để mở rộng.")

    render_chatbot()

    st.divider()
    if st.button("🏠 Quay về Trang chính", use_container_width=True):
        try:
            st.switch_page("main.py")
        except Exception:
            st.switch_page("Main")
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
