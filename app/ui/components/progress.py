from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Callable, Iterator, Optional

import streamlit as st

ProgressFn = Optional[Callable[[float, str], None]]


def _noop_progress(_: float, __: str) -> None:
    return


@contextmanager
def progress_handler(
    enabled: bool,
    success_message: str = "Hoàn tất xử lý!",
    *,
    holder: Optional[Any] = None,
) -> Iterator[ProgressFn]:
    if not enabled:
        yield None
        return

    target = holder or st
    progress_bar = target.progress(0.0)
    status_text = target.empty()

    def _update(value: float, text: str) -> None:
        progress_bar.progress(min(max(float(value), 0.0), 1.0))
        status_text.write(text)

    try:
        yield _update
    finally:
        progress_bar.empty()
        status_text.empty()
    target.success(success_message)
