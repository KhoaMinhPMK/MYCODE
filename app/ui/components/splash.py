from __future__ import annotations

import time

import streamlit as st


SPLASH_STATE_KEY = "ui_splash_dismissed"


def render_splash() -> None:
    # Temporarily disabled for testing - splash will show every reload
    # if st.session_state.get(SPLASH_STATE_KEY):
    #     return

    st.markdown(
        """
        <div class='splash-screen-css'>
            <div class='splash-card'>
                <div class='splash-logo'>CT</div>
                <div class='splash-progress-wrap'>
                    <div class='splash-progress-bar-css'></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state[SPLASH_STATE_KEY] = True
