import streamlit as st


def render_header() -> None:
    st.markdown(
        """
        <section class='hero-card glass-section'>
            <span class='hero-badge'><i class='ti ti-atom-2'></i>Radiology Studio</span>
            <h1>xử lý ảnh CT</h1>
            <p>
                Trải nghiệm điều phối ảnh cắt lớp theo phong cách studio: xử lý chuẩn hoá, dựng sinogram
                và tái tạo lát cắt với bố cục linh hoạt cùng bảng màu tuỳ chỉnh.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )
