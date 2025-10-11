import streamlit as st


def render_header() -> None:
    st.markdown(
        """
        <section class='hero-card glass-section'>
            <span class='hero-badge'><i class='ti ti-atom-2'></i>Radiology Studio</span>
            <h1>Xử lý ảnh CT</h1>
            <p>
                Trải nghiệm xử lý ảnh cắt lớp: tiền xử lý, dựng sinogram và tái tạo lát cắt
                với bố cục linh hoạt cùng bảng màu tùy chỉnh.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

