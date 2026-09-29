"""Metadata-filtered agronomy retrieval with crop/pest/state weighted ranking."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


KNOWLEDGE_PATH = Path(__file__).resolve().parent.parent / "data" / "agronomy_knowledge.jsonl"
CROP_ALIASES = {
    "paddy": "rice",
    "dhan": "rice",
    "varii": "rice",
    "kapas": "cotton",
    "kapus": "cotton",
}


class RagService:
    """Retrieves only credible crop-aware documents, then ranks by relevance."""

    def __init__(self) -> None:
        self.docs = _load_docs()
        self.vector_store = None
        self._init_vector_store()

    def retrieve(self, farmer: Any, k: int = 4) -> Dict[str, Any]:
        if hasattr(farmer, "crop"):
            # FarmContext object
            query_meta = {
                "crop": _canonical_crop(getattr(farmer.crop, "name", "rice")),
                "state": _norm(getattr(farmer.location, "state", "West Bengal")),
                "district": _norm(getattr(farmer.location, "district", "Nadia")),
                "season": _norm(getattr(farmer.crop, "season", "Kharif")),
                "pest": _norm(getattr(farmer.diagnosis, "condition_detected", "sheath blight") if getattr(farmer, "diagnosis", None) else "sheath blight"),
                "weather": _norm(getattr(farmer.weather, "microclimate_risk", "humidity")),
            }
        elif isinstance(farmer, dict):
            query_meta = _query_metadata(farmer)
        else:
            query_meta = {"crop": "rice", "state": "west bengal", "district": "nadia", "season": "kharif", "pest": "sheath blight", "weather": "humidity"}

        candidates = self._metadata_filter(query_meta)
        ranked = self._weighted_rank(candidates, query_meta)

        # Semantic similarity is used only as a tie-breaker among already credible candidates.
        if self.vector_store is not None and len(ranked) > 1:
            ranked = self._semantic_tiebreak(ranked, query_meta)

        sources = [
            {
                "id": doc["id"],
                "crop": doc.get("crop"),
                "region": doc.get("region"),
                "season": doc.get("season"),
                "topic": doc.get("topic"),
                "score": round(score, 3),
                "text": doc["text"],
            }
            for score, doc in ranked[:k]
        ]
        if not sources:
            sources = [_fallback_source(query_meta)]

        return {
            "query": " ".join(str(v) for v in query_meta.values() if v),
            "advisory_summary": " ".join(source["text"] for source in sources[:2])[:1200],
            "sources": sources,
            "mode": "metadata-filtered-weighted-rag",
            "filters": query_meta,
        }

    def _metadata_filter(self, meta: Dict[str, str]) -> List[Dict[str, Any]]:
        crop = meta["crop"]
        state = meta["state"]
        pest = meta["pest"]

        filtered = []
        for doc in self.docs:
            doc_crop = _norm(doc.get("crop"))
            doc_region = _norm(doc.get("region"))
            doc_topic = _norm(doc.get("topic"))

            # Crop mismatch is a hard filter unless the document is explicitly generic.
            if crop and doc_crop not in {crop, "all"}:
                continue
            # If there is a pest-specific doc for this crop, avoid unrelated pest docs.
            if pest and doc_topic and not _contains_any(doc_topic, pest) and doc_crop != "all":
                if not _broad_topic(doc_topic):
                    continue
            # State match is preferred but not mandatory when crop/pest are strong.
            if state and doc_region not in {state, "india", "all"} and doc_crop == "all":
                continue
            filtered.append(doc)
        return filtered

    def _weighted_rank(self, docs: List[Dict[str, Any]], meta: Dict[str, str]) -> List[Tuple[float, Dict[str, Any]]]:
        ranked = []
        for doc in docs:
            score = 0.0
            doc_crop = _norm(doc.get("crop"))
            doc_region = _norm(doc.get("region"))
            doc_season = _norm(doc.get("season"))
            doc_topic = _norm(doc.get("topic"))
            haystack = _norm(" ".join(str(v) for v in doc.values()))

            if meta["crop"] and doc_crop == meta["crop"]:
                score += 100
            elif doc_crop == "all":
                score += 15
            if meta["pest"] and (_contains_any(doc_topic, meta["pest"]) or _contains_any(haystack, meta["pest"])):
                score += 70
                if meta["pest"] in doc_topic or meta["pest"] in haystack:
                    score += 25
            if meta["state"] and doc_region == meta["state"]:
                score += 35
            elif doc_region in {"india", "all"}:
                score += 8
            if meta["season"] and doc_season in {meta["season"], "all"}:
                score += 20
            if meta["district"] and meta["district"] in haystack:
                score += 10
            ranked.append((score, doc))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return ranked

    def _semantic_tiebreak(self, ranked: List[Tuple[float, Dict[str, Any]]], meta: Dict[str, str]) -> List[Tuple[float, Dict[str, Any]]]:
        # Kept intentionally conservative: weighted metadata score remains dominant.
        try:
            query = " ".join(str(v) for v in meta.values() if v)
            matches = self.vector_store.similarity_search_with_score(query, k=len(ranked))
            semantic = {m.metadata.get("id"): 1 / (1 + float(score)) for m, score in matches}
            return sorted(
                [(score + semantic.get(doc["id"], 0), doc) for score, doc in ranked],
                key=lambda item: item[0],
                reverse=True,
            )
        except Exception:
            return ranked

    def _init_vector_store(self) -> None:
        try:
            from langchain_community.vectorstores import FAISS
            from langchain_core.documents import Document
            from langchain_core.embeddings import Embeddings
        except Exception:
            return

        class HashEmbeddings(Embeddings):
            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                return [self.embed_query(text) for text in texts]

            def embed_query(self, text: str) -> List[float]:
                dims = 128
                vec = [0.0] * dims
                for token in _norm(text).split():
                    vec[hash(token) % dims] += 1.0
                norm = sum(v * v for v in vec) ** 0.5 or 1.0
                return [v / norm for v in vec]

        documents = [
            Document(page_content=doc["text"], metadata={k: v for k, v in doc.items() if k != "text"})
            for doc in self.docs
        ]
        self.vector_store = FAISS.from_documents(documents, HashEmbeddings()) if documents else None


def _load_docs() -> List[Dict[str, Any]]:
    if not KNOWLEDGE_PATH.exists():
        return []
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def _query_metadata(farmer: Dict[str, Any]) -> Dict[str, str]:
    return {
        "crop": _canonical_crop(farmer.get("main_crop") or farmer.get("campaign_crop")),
        "state": _norm(farmer.get("state")),
        "district": _norm(farmer.get("district") or farmer.get("tehsil_block")),
        "season": _norm(farmer.get("season")),
        "pest": _norm(farmer.get("pest_threat")),
        "weather": _norm(farmer.get("weather_risk")),
    }


def _fallback_source(meta: Dict[str, str]) -> Dict[str, Any]:
    crop = meta.get("crop") or "crop"
    pest = meta.get("pest") or "local pest pressure"
    return {
        "id": "safe_fallback",
        "crop": crop,
        "region": meta.get("state") or "india",
        "season": meta.get("season") or "all",
        "topic": pest,
        "score": 0,
        "text": f"For {crop}, scout the field for {pest} and consult local label-approved agronomy advice before treatment.",
    }


def _canonical_crop(value: Any) -> str:
    crop = _norm(value)
    return CROP_ALIASES.get(crop, crop)


def _norm(value: Any) -> str:
    return str(value or "").strip().lower().replace("_", " ")


def _contains_any(text: str, query: str) -> bool:
    terms = [term for term in query.split() if len(term) > 2]
    return any(term in text for term in terms)


def _broad_topic(topic: str) -> bool:
    return any(token in topic for token in ["guidance", "season", "weather", "connectivity", "risk"])
