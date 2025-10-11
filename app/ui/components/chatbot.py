from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

from app.services.qa_bot import answer_question
from app.services.groq_client import chat_with_groq, groq_available
from app.services.research import (
    extract_keywords,
    search_google,
    summarize_results,
    get_default_bio_whitelist,
)


CHAT_STATE_KEY = "qa_messages"


def _init_chat_state() -> None:
    if CHAT_STATE_KEY not in st.session_state:
        st.session_state[CHAT_STATE_KEY] = []  # list[dict{role, content}]


def _render_message(role: str, content: str) -> None:
    with st.chat_message(role):
        st.write(content)


def render_chatbot() -> None:
    _init_chat_state()

    st.markdown(
        """
        <div class='glass-section'>
            <h3><i class='ti ti-robot'></i> Chatbot Kiến Thức (giới hạn chủ đề)</h3>
            <p style='margin:0; color: var(--text-muted); font-size: 0.95rem;'>
                Chatbot chỉ trả lời trong phạm vi chủ đề đã được biên soạn. Gõ "chủ đề" để xem danh sách.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Web research settings (optional fallback)
    with st.expander("Nghiên cứu Web (beta)"):
        enable_research = st.toggle(
            "Bật chế độ nghiên cứu khi câu hỏi ngoài phạm vi",
            value=False,
            key="qa_web_toggle",
        )
        top_k = st.slider("Số kết quả web", 1, 5, 3, key="qa_web_topk")
        use_domain_filter = st.toggle(
            "Bộ lọc domain y-sinh tin cậy (PubMed, Nature, ScienceDirect, …)",
            value=True,
            key="qa_web_domain_filter",
        )
        strict_only = st.toggle(
            "Chỉ lấy domain trong whitelist (nghiêm ngặt)",
            value=True,
            key="qa_web_strict",
        )
        default_wl = ", ".join(get_default_bio_whitelist())
        wl_text = st.text_area(
            "Whitelist domains (phân tách bằng dấu phẩy)",
            value=default_wl,
            height=72,
            key="qa_web_wl",
        )
        use_oss_kw = st.toggle("Dùng mô hình OSS cho trích từ khóa (YAKE)", value=False, key="qa_web_kw_oss")
        use_oss_sum = st.toggle("Dùng mô hình OSS cho tóm tắt (transformers)", value=False, key="qa_web_sum_oss")
        st.caption("Cần cài đặt: 'googlesearch-python' (tìm kiếm), 'yake' (từ khóa), 'transformers' (tóm tắt).")

    # Groq (reasoning) options
    with st.expander("Groq Reasoning (beta)"):
        enable_groq = st.toggle(
            "Dùng Groq cho câu hỏi ngoài phạm vi",
            value=False,
            key="qa_groq_toggle",
        )
        groq_model = st.selectbox(
            "Model",
            options=["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3-32b"],
            index=0,
            key="qa_groq_model",
        )
        include_reasoning = st.toggle("Kèm nội dung reasoning (nếu hỗ trợ)", value=False, key="qa_groq_inc_reason")
        # effort: for GPT-OSS use low/medium/high; for Qwen use none/default
        if groq_model.startswith("openai/gpt-oss"):
            effort = st.select_slider("Mức độ reasoning", options=["low", "medium", "high"], value="low", key="qa_groq_eff")
            reasoning_effort = effort
            reasoning_format = None
        else:
            effort = st.select_slider("Mức độ reasoning", options=["none", "default"], value="default", key="qa_groq_eff")
            reasoning_effort = effort
            reasoning_format = st.selectbox("Định dạng reasoning", options=["parsed", "raw", "hidden"], index=0, key="qa_groq_fmt")

    # 1) Read input
    prompt = st.chat_input("Nhập câu hỏi (ví dụ: 'FBP là gì?', 'nguồn dữ liệu đầu vào')")

    # 2) Update conversation state first (so we can render immediately)
    history: List[Dict[str, str]] = st.session_state[CHAT_STATE_KEY]
    if prompt:
        history.append({"role": "user", "content": prompt})

        handled = False
        # In-scope curated answer
        reply = answer_question(prompt)
        if reply:
            history.append({"role": "assistant", "content": reply})
            handled = True

        # Web research attempt (optional)
        summary: str | None = None
        kws: list[str] | None = None
        if not handled and enable_research:
            kws = extract_keywords(prompt, prefer_oss=use_oss_kw)
            if kws:
                query = " ".join(kws)
                whitelist = None
                if use_domain_filter:
                    wl = [w.strip() for w in wl_text.split(",") if w.strip()]
                    whitelist = wl if wl else get_default_bio_whitelist()
                results = search_google(
                    query,
                    num_results=top_k,
                    domain_whitelist=whitelist,
                    strict_only=strict_only,
                    use_cache=True,
                )
                summary = summarize_results(prompt, results, prefer_oss=use_oss_sum)
                if summary:
                    history.append({"role": "assistant", "content": f"Từ khóa: {', '.join(kws)}\n\n{summary}"})
                    handled = True

        # Groq fallback if still unhandled
        if not handled and enable_groq:
            with st.spinner("Đang suy nghĩ với Groq…"):
                content, reasoning, err = chat_with_groq(
                    prompt,
                    model=groq_model,
                    include_reasoning=include_reasoning,
                    reasoning_effort=reasoning_effort,
                    reasoning_format=reasoning_format,
                )
            if err:
                history.append({"role": "assistant", "content": f"Không thể gọi Groq: {err}"})
            elif content:
                if include_reasoning and reasoning:
                    history.append({"role": "assistant", "content": f"{content}\n\n[Reasoning]\n{reasoning}"})
                else:
                    history.append({"role": "assistant", "content": content})
            handled = True

        # If neither research nor Groq produced an answer, keep silent by design
        # else: remain silent for out-of-scope

    # 3) Render full conversation (user then assistant immediately)
    for msg in history:
        _render_message(msg.get("role", "assistant"), msg.get("content", ""))
