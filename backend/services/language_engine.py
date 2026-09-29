"""Language-pure agronomy phrasing for farmer-facing campaign content."""

from __future__ import annotations

from typing import Dict, Optional


LANGUAGE_PACKS: Dict[str, Dict[str, object]] = {
    "Hindi": {
        "terms": {
            "crop": "फसल",
            "field": "खेत",
            "scouting": "फसल की नियमित निगरानी",
            "fungal disease": "फफूंद रोग",
            "pink bollworm": "गुलाबी सुंडी",
            "bollworm": "सुंडी",
            "rust": "रतुआ रोग",
            "dealer": "नजदीकी कृषि विक्रेता",
            "agronomist": "कृषि सलाहकार",
        },
        "opening": "नमस्ते {name} जी।",
        "risk": "{district} क्षेत्र में {crop} में {pest} का खतरा दिख रहा है।",
        "scout": "फसल की नियमित निगरानी जरूरी है।",
        "weather": "{weather} के कारण सावधानी रखें।",
        "cta": "आज खेत देखें और नजदीकी कृषि विक्रेता से सलाह लें।",
        "sms_cta": "आज खेत देखें।",
        "voice_close": "सही समय पर सलाह लेने से फसल बचाने में मदद मिलती है।",
    },
    "Telugu": {
        "terms": {
            "crop": "పంట",
            "field": "పొలం",
            "scouting": "పంటను తరచుగా పరిశీలించడం",
            "fungal disease": "శిలీంధ్ర వ్యాధి",
            "pink bollworm": "పింక్ బాల్‌వార్మ్",
            "bollworm": "కాయ పురుగు",
            "rust": "రస్ట్ వ్యాధి",
            "dealer": "సమీప వ్యవసాయ విక్రేత",
            "agronomist": "వ్యవసాయ సలహాదారు",
        },
        "opening": "నమస్కారం {name} గారు.",
        "risk": "{district} ప్రాంతంలో {crop} పంటకు {pest} ప్రమాదం కనిపిస్తోంది.",
        "scout": "పంటను తరచుగా పరిశీలించడం ముఖ్యం.",
        "weather": "{weather} కారణంగా జాగ్రత్త అవసరం.",
        "cta": "ఈరోజు పొలాన్ని పరిశీలించి సమీప వ్యవసాయ విక్రేతను సంప్రదించండి.",
        "sms_cta": "ఈరోజు పొలం చూడండి.",
        "voice_close": "సరైన సమయంలో చర్య తీసుకుంటే పంట నష్టం తగ్గుతుంది.",
    },
    "Tamil": {
        "terms": {
            "crop": "பயிர்",
            "field": "வயல்",
            "scouting": "பயிரை அடிக்கடி பார்வையிடுதல்",
            "fungal disease": "பூஞ்சை நோய்",
            "pink bollworm": "இளஞ்சிவப்பு காய் புழு",
            "bollworm": "காய் புழு",
            "rust": "ரஸ்ட் நோய்",
            "dealer": "அருகிலுள்ள வேளாண் விற்பனையாளர்",
            "agronomist": "வேளாண் ஆலோசகர்",
        },
        "opening": "வணக்கம் {name} அவர்களே.",
        "risk": "{district} பகுதியில் {crop} பயிரில் {pest} அபாயம் உள்ளது.",
        "scout": "பயிரை அடிக்கடி பார்வையிடுவது முக்கியம்.",
        "weather": "{weather} காரணமாக கவனம் தேவை.",
        "cta": "இன்று வயலைப் பார்த்து அருகிலுள்ள வேளாண் விற்பனையாளரிடம் ஆலோசனை பெறுங்கள்.",
        "sms_cta": "இன்று வயலைப் பாருங்கள்.",
        "voice_close": "சரியான நேரத்தில் செயல் எடுத்தால் பயிர் சேதம் குறையும்.",
    },
    "Marathi": {
        "terms": {
            "crop": "पीक",
            "field": "शेत",
            "scouting": "पिकाची नियमित पाहणी",
            "fungal disease": "बुरशीजन्य रोग",
            "pink bollworm": "गुलाबी बोंड अळी",
            "bollworm": "बोंड अळी",
            "rust": "तांबेरा रोग",
            "dealer": "जवळचा कृषी विक्रेता",
            "agronomist": "कृषी सल्लागार",
        },
        "opening": "नमस्कार {name} जी.",
        "risk": "{district} भागात {crop} पिकात {pest} चा धोका दिसत आहे.",
        "scout": "पिकाची नियमित पाहणी गरजेची आहे.",
        "weather": "{weather} मुळे काळजी घ्या.",
        "cta": "आज शेत पाहा आणि जवळच्या कृषी विक्रेत्याचा सल्ला घ्या.",
        "sms_cta": "आज शेत पाहा.",
        "voice_close": "वेळीच उपाय केल्यास पिकाचे नुकसान कमी होते.",
    },
    "English": {
        "terms": {
            "crop": "crop",
            "field": "field",
            "scouting": "regular crop scouting",
            "fungal disease": "fungal disease",
            "pink bollworm": "pink bollworm",
            "bollworm": "bollworm",
            "rust": "rust disease",
            "dealer": "nearby agri dealer",
            "agronomist": "agronomist",
        },
        "opening": "Hello {name}.",
        "risk": "In {district}, {crop} has {pest} risk.",
        "scout": "Regular crop scouting is important.",
        "weather": "{weather} needs extra caution.",
        "cta": "Scout the field today and speak to a nearby agri dealer.",
        "sms_cta": "Scout today.",
        "voice_close": "Timely action can reduce crop loss.",
    },
}

CROP_NAMES = {
    "Hindi": {"rice": "धान", "cotton": "कपास", "wheat": "गेहूं", "maize": "मक्का", "soybean": "सोयाबीन"},
    "Telugu": {"rice": "వరి", "cotton": "పత్తి", "wheat": "గోధుమ", "maize": "మొక్కజొన్న", "soybean": "సోయాబీన్"},
    "Tamil": {"rice": "நெல்", "cotton": "பருத்தி", "wheat": "கோதுமை", "maize": "மக்காச்சோளம்", "soybean": "சோயாபீன்"},
    "Marathi": {"rice": "भात", "cotton": "कापूस", "wheat": "गहू", "maize": "मका", "soybean": "सोयाबीन"},
    "English": {"rice": "rice", "cotton": "cotton", "wheat": "wheat", "maize": "maize", "soybean": "soybean"},
}


class LanguageEngine:
    """Builds language-pure SMS, WhatsApp and voice text."""

    def build_messages(
        self,
        language: str,
        name: str,
        crop: Optional[str],
        pest: Optional[str],
        district: Optional[str],
        weather: Optional[str],
        product: Optional[str],
        sms_safe: bool,
    ) -> Dict[str, str]:
        lang = language if language in LANGUAGE_PACKS else "Hindi"
        pack = LANGUAGE_PACKS[lang]
        crop_name = self.localize_crop(lang, crop)
        pest_name = self.localize_term(lang, pest or "pest")
        district_name = district or self.localize_term(lang, "field")

        risk = str(pack["risk"]).format(district=district_name, crop=crop_name, pest=pest_name)
        weather_line = str(pack["weather"]).format(weather=weather) if weather else ""
        cta = str(pack["cta"])
        sms_cta = str(pack["sms_cta"])

        sms = f"{crop_name}: {pest_name} खतरा. {sms_cta}" if lang == "Hindi" else None
        if lang == "Telugu":
            sms = f"{crop_name}: {pest_name} ప్రమాదం. {sms_cta}"
        elif lang == "Tamil":
            sms = f"{crop_name}: {pest_name} அபாயம். {sms_cta}"
        elif lang == "Marathi":
            sms = f"{crop_name}: {pest_name} धोका. {sms_cta}"
        elif lang == "English":
            sms = f"{crop_name}: {pest_name} risk. {sms_cta}"

        whatsapp_lines = [
            str(pack["opening"]).format(name=name),
            risk,
            str(pack["scout"]),
        ]
        if weather_line:
            whatsapp_lines.append(weather_line)
        whatsapp_lines.append(cta)
        if product and lang == "English":
            whatsapp_lines.append(f"Ask about {product} only if symptoms are visible.")
        whatsapp = "\n".join(whatsapp_lines)

        voice = " ".join([
            str(pack["opening"]).format(name=name),
            risk,
            str(pack["scout"]),
            weather_line,
            cta,
            str(pack["voice_close"]),
        ]).replace("  ", " ").strip()

        return {
            "sms": compress_sms(sms or whatsapp, 140 if sms_safe else 160),
            "whatsapp": whatsapp,
            "voice_script": voice,
            "cta_text": sms_cta,
        }

    def localize_term(self, language: str, term: Optional[str]) -> str:
        lang = language if language in LANGUAGE_PACKS else "Hindi"
        value = str(term or "").strip().lower()
        terms = LANGUAGE_PACKS[lang]["terms"]
        for key, localized in terms.items():
            if key in value:
                return str(localized)
        return str(term or terms["crop"])

    def localize_crop(self, language: str, crop: Optional[str]) -> str:
        lang = language if language in CROP_NAMES else "Hindi"
        key = str(crop or "").strip().lower()
        return CROP_NAMES[lang].get(key, crop or str(LANGUAGE_PACKS[lang]["terms"]["crop"]))


def compress_sms(text: str, limit: int = 160) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    hard_stop = text[:limit]
    if " " in hard_stop:
        hard_stop = hard_stop.rsplit(" ", 1)[0]
    return hard_stop.rstrip(".,;:") + "."
