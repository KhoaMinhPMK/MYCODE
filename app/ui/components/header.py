import streamlit as st


def render_header() -> None:
    # Create columns for header with chat button
    col1, col2 = st.columns([10, 1])
    
    with col1:
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
    
    with col2:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        if st.button("💬", help="Mở Chat", use_container_width=True, key="chat_button"):
            st.session_state.current_page = "chat"
            st.rerun()
