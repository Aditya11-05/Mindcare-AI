import os
from typing import Optional, List, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from sqlalchemy import func
from .db import SessionLocal, init_db, Message
from .safety_guard import is_crisis
from .respond_templates import generate_reply_templates
from .respond_llm import llm_reply

# ---------- FastAPI setup ----------
app = FastAPI(title="MindCare AI — Complete")

origins = ["*"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ---------- Models ----------
MODEL_NAME = os.getenv("EMOTION_MODEL", "bhadresh-savani/distilbert-base-uncased-emotion")
clf = pipeline("text-classification", model=MODEL_NAME, return_all_scores=True)

EMO_MAP = {
    "joy": "joy",
    "sadness": "sadness",
    "anger": "anger",
    "fear": "anxiety",
    "love": "love",
    "surprise": "surprise",
    "neutral": "neutral",
}

USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"

def top_emotion(scores):
    best = max(scores, key=lambda x: x["score"])
    label = best["label"].lower()
    mapped = EMO_MAP.get(label, label)
    return mapped, float(best["score"])

class ChatIn(BaseModel):
    text: str

class ChatOut(BaseModel):
    emotion: str
    confidence: float
    reply: str

# ---------- Init DB ----------
init_db()

# ---------- Routes ----------
@app.post("/chat", response_model=ChatOut)
def chat(inp: ChatIn):
    text = (inp.text or "").strip()
    if not text:
        return ChatOut(emotion="neutral", confidence=0.0, reply="I’m here. Share whatever’s on your mind.")

    # Emotion
    scores = clf(text)[0]
    emotion, conf = top_emotion(scores)

    # Safety first: hard-stop template if crisis is detected
    if is_crisis(text, emotion, conf):
        reply = generate_reply_templates(text, emotion, conf)
    else:
        # LLM path if enabled; fallback to templates on error
        if USE_LLM:
            try:
                reply = llm_reply(text, emotion, conf)
            except Exception:
                reply = generate_reply_templates(text, emotion, conf)
        else:
            reply = generate_reply_templates(text, emotion, conf)

    # Log both user and ai
    with SessionLocal() as s:
        s.add_all([
            Message(role="user", text=text, emotion=emotion, confidence=conf),
            Message(role="ai", text=reply, emotion=emotion, confidence=conf)
        ])
        s.commit()

    return ChatOut(emotion=emotion, confidence=conf, reply=reply)

@app.get("/history")
def history(limit: int = 100):
    with SessionLocal() as s:
        rows = s.query(Message).order_by(Message.id.desc()).limit(limit).all()
        return [{
            "id": m.id, "ts": m.ts.isoformat(), "role": m.role, "text": m.text,
            "emotion": m.emotion, "confidence": m.confidence
        } for m in reversed(rows)]

@app.get("/stats")
def stats():
    # counts per emotion
    with SessionLocal() as s:
        rows = s.query(Message.emotion, func.count(Message.id)).filter(Message.role=="user").group_by(Message.emotion).all()
        counts = {k or "unknown": int(v) for k, v in rows}
    return {"emotion_counts": counts}

@app.post("/delete_all")
def delete_all():
    with SessionLocal() as s:
        s.query(Message).delete()
        s.commit()
    return {"ok": True, "message": "All messages deleted."}
