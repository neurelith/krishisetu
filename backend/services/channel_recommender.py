"""
channel_recommender.py
----------------------
Rule-based channel and timing recommender for WhatsApp campaign targeting.

Recommendations are driven by the engagement segment, farmer demographics,
device type, and seasonal context – all features already computed by the
EngagementPredictor pipeline.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Static knowledge bases
# ---------------------------------------------------------------------------

# Preferred channels by device type
_DEVICE_CHANNEL_MAP: Dict[str, List[str]] = {
    "smartphone":  ["whatsapp", "push_notification", "sms"],
    "android":     ["whatsapp", "push_notification", "sms"],
    "feature_phone": ["sms", "voice_call"],
    "keypad_phone": ["sms", "voice_call"],
    "basic_phone": ["sms", "voice_call"],
    "ios":         ["whatsapp", "push_notification", "sms"],
    "unknown":     ["sms", "whatsapp"],
}

# Best send time windows (IST) by engagement segment
_SEGMENT_SEND_WINDOWS: Dict[str, Dict[str, Any]] = {
    "Very High": {
        "primary_window":   "07:00–09:00",
        "secondary_window": "19:00–21:00",
        "days":             ["Monday", "Wednesday", "Friday"],
        "rationale":        "High-intent farmers respond best early morning before field work.",
    },
    "High": {
        "primary_window":   "08:00–10:00",
        "secondary_window": "18:00–20:00",
        "days":             ["Tuesday", "Thursday", "Saturday"],
        "rationale":        "Moderate-intent farmers check phones mid-morning.",
    },
    "Medium": {
        "primary_window":   "10:00–12:00",
        "secondary_window": "16:00–18:00",
        "days":             ["Monday", "Wednesday", "Friday"],
        "rationale":        "Nurture segment; midday reach when farm tasks ease.",
    },
    "Low": {
        "primary_window":   "12:00–14:00",
        "secondary_window": None,
        "days":             ["Wednesday"],
        "rationale":        "Low-frequency touch; avoid over-messaging.",
    },
}

# Message frequency caps
_FREQUENCY_CAPS: Dict[str, int] = {
    "Very High": 3,   # messages per month
    "High":      2,
    "Medium":    1,
    "Low":       1,
}

# Seasonal channel emphasis
_SEASON_PHASE_CHANNELS: Dict[str, List[str]] = {
    "pre_season":    ["voice_call", "sms"],          # planning phase – more personal
    "early_season":  ["whatsapp", "sms"],
    "mid_season":    ["whatsapp", "push_notification"],
    "late_season":   ["whatsapp", "sms"],             # urgency – products needed now
    "post_season":   ["sms"],                          # harvest done – light touch
    "post_harvest":  ["sms"],
    "unknown":       ["sms", "whatsapp"],
}


class ChannelRecommender:
    """
    Recommends the best communication channel(s) and send timing for a
    farmer based on their engagement segment and profile.

    Usage
    -----
    >>> rec = ChannelRecommender()
    >>> channels = rec.recommend(
    ...     segment="High",
    ...     device_type="smartphone",
    ...     season_phase="mid_season",
    ...     language="Hindi",
    ...     hist_open_rate=0.4,
    ... )
    """

    def recommend(
        self,
        segment:         str,
        device_type:     Optional[str] = None,
        season_phase:    Optional[str] = None,
        language:        Optional[str] = None,
        hist_open_rate:  float = 0.0,
        hist_click_rate: float = 0.0,
        message_count_history: int = 0,
        literacy_level: Optional[str] = None,
        connectivity: Optional[str] = None,
        high_value_farmer: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Return channel and timing recommendations.

        Parameters
        ----------
        segment         : Engagement segment string (Low / Medium / High / Very High)
        device_type     : Farmer's device type (smartphone / feature_phone / …)
        season_phase    : Current season phase from preprocessing
        language        : Farmer's preferred language
        hist_open_rate  : Historical message open rate (0–1)
        hist_click_rate : Historical click rate (0–1)
        message_count_history : Number of messages sent to this farmer before

        Returns
        -------
        dict with keys:
            primary_channel, alternative_channels, send_window,
            frequency_per_month, personalisation_tips, priority_score
        """
        segment = segment or "Low"

        # ── Primary channel selection ──────────────────────────────────
        device_key  = (device_type or "unknown").lower()
        device_channels = _DEVICE_CHANNEL_MAP.get(device_key, ["sms", "whatsapp"])
        season_channels = _SEASON_PHASE_CHANNELS.get(season_phase or "unknown", ["sms"])

        # Intersect device preference with season preference; fall back to device list
        primary_candidates = [c for c in device_channels if c in season_channels]
        if not primary_candidates:
            primary_candidates = device_channels

        reasons: List[str] = []
        if device_key in ("feature_phone", "basic_phone", "keypad_phone"):
            primary_candidates = ["sms", "voice_call"]
            reasons.append("Feature/keypad phone detected, so low-bandwidth SMS or voice is safest.")
        if (literacy_level or "").lower() in ("low", "limited", "illiterate"):
            primary_candidates = ["voice_call", "sms"]
            reasons.append("Low literacy profile, so voice-first advisory improves comprehension.")
        if (connectivity or "").lower() in ("weak", "low", "offline", "2g"):
            primary_candidates = ["sms"] + [c for c in primary_candidates if c != "sms"]
            reasons.append("Weak connectivity, so SMS is the fallback channel.")
        if device_key in ("smartphone", "android", "ios") and segment in ("High", "Very High"):
            primary_candidates = ["whatsapp"] + [c for c in primary_candidates if c != "whatsapp"]
            reasons.append("Smartphone plus high predicted receptivity supports WhatsApp rich content.")
        if high_value_farmer:
            primary_candidates = ["whatsapp", "voice_call", "sms"]
            reasons.append("High-value farmer, so combine WhatsApp with voice follow-up.")

        primary_channel     = primary_candidates[0]
        alternative_channels = [c for c in device_channels if c != primary_channel][:2]
        if high_value_farmer:
            alternative_channels = [c for c in ["voice_call", "sms", "whatsapp"] if c != primary_channel][:2]

        # ── Timing window ─────────────────────────────────────────────
        timing = _SEGMENT_SEND_WINDOWS.get(
            segment, _SEGMENT_SEND_WINDOWS["Low"]
        )

        # ── Frequency cap ─────────────────────────────────────────────
        freq_cap = _FREQUENCY_CAPS.get(segment, 1)

        # Reduce frequency for farmers who've already received many messages
        if message_count_history > 10 and hist_click_rate < 0.02:
            freq_cap = max(1, freq_cap - 1)

        # ── Priority score (0–100) ────────────────────────────────────
        seg_score = {"Very High": 90, "High": 70, "Medium": 45, "Low": 20}.get(segment, 20)
        history_boost = min(20, int(hist_open_rate * 30 + hist_click_rate * 50))
        priority_score = min(100, seg_score + history_boost)

        # ── Personalisation tips ──────────────────────────────────────
        tips = self._build_tips(
            segment, language, hist_open_rate, hist_click_rate, season_phase
        )

        return {
            "primary_channel":      primary_channel,
            "alternative_channels": alternative_channels,
            "send_window": {
                "primary":   timing["primary_window"],
                "secondary": timing["secondary_window"],
                "best_days": timing["days"],
                "rationale": timing["rationale"],
            },
            "frequency_per_month": freq_cap,
            "personalisation_tips": tips,
            "priority_score":        priority_score,
            "rationale": reasons or ["Selected from device, season and engagement rules."],
        }

    # ------------------------------------------------------------------

    def _build_tips(
        self,
        segment:        str,
        language:       Optional[str],
        open_rate:      float,
        click_rate:     float,
        season_phase:   Optional[str],
    ) -> List[str]:
        tips: List[str] = []

        if language and language.lower() not in ("english", "unknown"):
            tips.append(f"Send message in {language} for better comprehension.")

        if open_rate < 0.1:
            tips.append("Use curiosity-driven subject lines to improve open rate.")
        elif open_rate > 0.5:
            tips.append("Farmer is highly engaged – include exclusive offers.")

        if click_rate < 0.02 and segment in ("High", "Very High"):
            tips.append("Add a clear single CTA (call-to-action) link to boost clicks.")

        if season_phase == "late_season":
            tips.append("Highlight harvest-related products; urgency messaging works well.")
        elif season_phase == "pre_season":
            tips.append("Focus on crop-planning content and seed recommendations.")
        elif season_phase == "early_season":
            tips.append("Emphasize crop protection and fertiliser timing tips.")

        if segment == "Low":
            tips.append("Consider re-engagement content (surveys, quizzes) to revive interest.")

        if not tips:
            tips.append("Use standard campaign messaging with farmer's name for personalisation.")

        return tips
