"""
smoke_test.py  — offline end-to-end test (no server needed)
Run from the backend/ directory:  python smoke_test.py
"""
import sys
from pathlib import Path

# ── MUST be first: add backend/ root so all packages resolve correctly ────
_BACKEND = Path(__file__).resolve().parent
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from services.predictor           import EngagementPredictor
from services.channel_recommender import ChannelRecommender
from services.content_generator   import ContentGenerator
from utils.preprocessing          import parse_crop_calendar, calculate_time_features

SAMPLE_FARMER = {
    "grower_id":    "GR_SMOKE_001",
    "state":        "Rajasthan",
    "district":     "Jaipur",
    "language":     "Hindi",
    "device_type":  "smartphone",
    "gender":       "Male",
    "grower_age":   42.0,
    "grower_farm_size": 4.5,
    "grower_crop_calendar": (
        '{"crop":"wheat",'
        '"sowing":{"start":"2025-11-01","end":"2025-11-15"},'
        '"harvest":{"start":"2026-04-01","end":"2026-04-15"}}'
    ),
    "product_scan":             True,
    "offline_campaign_attended": False,
    "campaign_crop":    "wheat",
    "campaign_product": "AMISTAR TOP",
    "message_sent_date": "2026-02-15",
    "hist_open_rate":         0.0,
    "hist_click_rate":        0.0,
    "message_count_history":  0,
    "days_since_last_message": 999.0,
    "message_frequency":      0.0,
}

FARMER_NAME = "Rajesh Kumar"


def main():
    sep = "=" * 60
    print(f"\n{sep}\n  Syngenta ML Services - Smoke Test\n{sep}")

    # 1. Predictor
    print("\n[1/3] Loading EngagementPredictor...")
    predictor = EngagementPredictor()

    print("[1/3] Running prediction...")
    pred = predictor.predict(SAMPLE_FARMER)
    print(f"  Probability : {pred['engagement_probability']:.4f}")
    print(f"  Segment     : {pred['segment']}")
    print(f"  Confidence  : {pred['confidence']}")
    print(f"  Features    : {pred['features_used']}")

    # 2. Channel recommender
    print("\n[2/3] ChannelRecommender...")
    recommender = ChannelRecommender()
    channel = recommender.recommend(
        segment               = pred["segment"],
        device_type           = SAMPLE_FARMER["device_type"],
        language              = SAMPLE_FARMER["language"],
        hist_open_rate        = SAMPLE_FARMER["hist_open_rate"],
        hist_click_rate       = SAMPLE_FARMER["hist_click_rate"],
        message_count_history = SAMPLE_FARMER["message_count_history"],
    )
    print(f"  Primary channel  : {channel['primary_channel']}")
    print(f"  Best send window : {channel['send_window']['primary']}")
    print(f"  Messages/month   : {channel['frequency_per_month']}")
    print(f"  Priority score   : {channel['priority_score']}")

    # 3. Content generator
    print("\n[3/3] ContentGenerator...")
    _, sow, _, harv, _, _ = parse_crop_calendar(SAMPLE_FARMER["grower_crop_calendar"])
    tf = calculate_time_features(sow, harv, SAMPLE_FARMER["message_sent_date"])

    generator = ContentGenerator()
    content = generator.generate(
        farmer_name        = FARMER_NAME,
        segment            = pred["segment"],
        growth_stage       = tf["estimated_growth_stage"],
        crop               = "wheat",
        campaign_product   = SAMPLE_FARMER["campaign_product"],
        district           = SAMPLE_FARMER["district"],
        days_until_harvest = tf["days_until_harvest"] if str(tf["days_until_harvest"]) != "nan" else None,
        language           = SAMPLE_FARMER["language"],
    )
    print(f"  Growth stage    : {tf['estimated_growth_stage']}")
    print(f"  Days to harvest : {tf['days_until_harvest']}")
    print(f"\n  Primary message :")
    print(f"    {content['primary_message']}")
    print(f"\n  Subject line  : {content['subject_line']}")
    print(f"  CTA           : {content['cta_text']}")

    print(f"\n{sep}\n  ALL SMOKE TESTS PASSED\n{sep}\n")


if __name__ == "__main__":
    main()
