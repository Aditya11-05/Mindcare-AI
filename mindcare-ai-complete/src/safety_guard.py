RISK_TERMS = [
    "suicide","kill myself","end it","self harm","cutting",
    "no reason to live","hang myself","overdose","hurt myself","die","ending my life"
]

def is_crisis(text: str, emotion: str, prob: float) -> bool:
    t = (text or "").lower()
    phrase_hit = any(term in t for term in RISK_TERMS)
    emo_risk = (emotion in {"sadness","fear","anxiety","shame"}) and (prob >= 0.55)
    return phrase_hit or emo_risk
