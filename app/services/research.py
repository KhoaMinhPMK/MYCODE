from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import re
import time


@dataclass(frozen=True)
class SearchResult:
    title: str
    link: str
    snippet: str = ""


_STOPWORDS = {
    "là", "làm", "và", "hoặc", "của", "các", "cái", "những", "một", "này",
    "đó", "cho", "khi", "với", "trong", "đến", "từ", "cần", "nên", "được",
    "thì", "gì", "nào", "bao", "như", "về", "đang", "theo", "hỏi", "đầu",
}

_DOMAIN_TERMS = [
    "fbp", "filtered back projection", "backprojection", "radon", "iradon",
    "sinogram", "ct", "ct reconstruction", "reconstruction",
]


def _extract_keywords_yake(text: str, max_keywords: int) -> Optional[List[str]]:
    try:
        import yake  # type: ignore
    except Exception:
        return None
    try:
        kw_extractor = yake.KeywordExtractor(lan="vi", n=1, top=max_keywords)
        keywords = kw_extractor.extract_keywords(text)
        sorted_keys = [k for k, _ in sorted(keywords, key=lambda x: x[1])]
        seen = set()
        result: List[str] = []
        for k in sorted_keys:
            kl = k.lower()
            if kl not in seen:
                seen.add(kl)
                result.append(kl)
        return result[:max_keywords]
    except Exception:
        return None


def extract_keywords(text: str, max_keywords: int = 6, *, prefer_oss: bool = False) -> List[str]:
    if not text:
        return []
    t = text.lower()
    kept: List[str] = [term for term in _DOMAIN_TERMS if term in t]

    if prefer_oss:
        oss = _extract_keywords_yake(text, max_keywords)
        if oss:
            merged: List[str] = []
            seen = set()
            for tok in kept + oss:
                if tok not in seen:
                    seen.add(tok)
                    merged.append(tok)
            return merged[:max_keywords]

    tokens = re.findall(r"[a-zA-ZÀ-ỹ0-9\-]+", t)
    tokens = [tok for tok in tokens if tok not in _STOPWORDS and len(tok) > 2]
    seen = set()
    uniq: List[str] = []
    for tok in tokens:
        if tok not in seen:
            seen.add(tok)
            uniq.append(tok)
    merged = kept + [u for u in uniq if u not in kept]
    return merged[:max_keywords]


def get_default_bio_whitelist() -> List[str]:
    return [
        "pubmed.ncbi.nlm.nih.gov",
        "www.ncbi.nlm.nih.gov",
        "nih.gov",
        "nature.com",
        "www.nature.com",
        "sciencedirect.com",
        "www.sciencedirect.com",
        "springer.com",
        "link.springer.com",
        "ieeexplore.ieee.org",
    ]


_CACHE: Dict[Tuple[str, int, Tuple[str, ...], bool], Tuple[float, List[SearchResult]]] = {}
_CACHE_TTL_SECONDS = 3600.0


def _filter_by_domain(results: List[SearchResult], whitelist: Sequence[str], strict_only: bool) -> List[SearchResult]:
    wl = set(whitelist)
    whitelisted = [r for r in results if any(host in r.link for host in wl)]
    if strict_only:
        return whitelisted
    others = [r for r in results if r not in whitelisted]
    return whitelisted + others


def search_google(
    query: str,
    num_results: int = 3,
    *,
    domain_whitelist: Optional[Sequence[str]] = None,
    strict_only: bool = True,
    use_cache: bool = True,
) -> List[SearchResult]:
    try:
        from googlesearch import search  # type: ignore
    except Exception:
        return []

    wl_tuple: Tuple[str, ...] = tuple(domain_whitelist) if domain_whitelist else tuple()
    cache_key = (query, num_results, wl_tuple, strict_only)
    now = time.time()
    if use_cache and cache_key in _CACHE:
        ts, cached = _CACHE[cache_key]
        if now - ts < _CACHE_TTL_SECONDS:
            return list(cached)

    try:
        links = list(search(query, num_results=num_results, advanced=False, lang="vi"))
    except Exception:
        return []

    raw: List[SearchResult] = []
    for url in links[: num_results * 2]:
        title = re.sub(r"https?://(www\.)?", "", url).split("/")[0]
        raw.append(SearchResult(title=title, link=url))

    filtered = _filter_by_domain(raw, domain_whitelist, strict_only) if domain_whitelist else raw
    results = filtered[:num_results]

    if use_cache:
        _CACHE[cache_key] = (now, list(results))
    return results


def _summarize_with_transformers(text: str) -> Optional[str]:
    try:
        from transformers import pipeline  # type: ignore
    except Exception:
        return None
    try:
        summarizer = pipeline("summarization")
        out = summarizer(text, max_length=120, min_length=40, do_sample=False)
        if out and isinstance(out, list) and isinstance(out[0], dict) and "summary_text" in out[0]:
            return out[0]["summary_text"]
        return None
    except Exception:
        return None


def summarize_results(query: str, results: List[SearchResult], *, prefer_oss: bool = False) -> Optional[str]:
    if not results:
        return None
    base_text = "; ".join([r.title for r in results])

    if prefer_oss:
        model_sum = _summarize_with_transformers(base_text)
        if model_sum:
            citations = "\n".join([f"- {r.title}: {r.link}" for r in results])
            return model_sum + "\n\nNguồn:\n" + citations

    bullets = []
    for r in results:
        bullets.append(f"- {r.title}: {r.link}")
    summary = (
        "Tổng hợp nhanh từ kết quả web (beta, không bảo đảm độ chính xác):\n" + "\n".join(bullets)
    )
    return summary

