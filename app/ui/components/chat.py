import streamlit as st


def render_chat_page() -> None:
    """Render the chat interface page."""
    st.markdown(
        """
        <section class='hero-card glass-section'>
            <span class='hero-badge'><i class='ti ti-message-chatbot'></i>Chat Assistant</span>
            <h1>Trợ lý AI</h1>
            <p>
                Trò chuyện với trợ lý AI để được hỗ trợ về xử lý ảnh CT và các tính năng khác.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Chat container with custom styling
    st.markdown(
        """
        <div class='glass-section' style='padding: 2rem; border-radius: 24px; margin-bottom: 1rem;'>
        """,
        unsafe_allow_html=True,
    )
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Nhập tin nhắn của bạn..."):
        # Add user message to chat history
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response (placeholder)
        response = f"Bạn đã nói: '{prompt}'. Đây là một trợ lý demo. Tính năng chat AI sẽ được tích hợp sau."
        
        # Add assistant response to chat history
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Rerun to update the display
        st.rerun()
    
    # Back button
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔙 Quay lại trang chính", use_container_width=True, type="primary"):
            st.session_state.current_page = "main"
            st.rerun()
