# MindCare AI — Complete (Ready to Use)

An emotion-aware, safety-first mental-health companion with:
- ✅ Emotion detection (Hugging Face pipeline by default)
- ✅ **Safety guard** for crisis phrases (shows helplines)
- ✅ **Empathetic replies** (templates) **or LLM-powered** replies (optional)
- ✅ **SQLite logging** of chats + **mood chart**
- ✅ **Docker** + **Docker Compose**
- ✅ Data privacy: local DB + delete-all endpoint/button

> **Disclaimer:** Not medical/clinical advice. If you're in crisis, contact local emergency services immediately.

---

## Quick Start (Local)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

1. **Run backend**:
```bash
uvicorn src.api:app --reload --port 8000
```
2. **Run UI** (new terminal):
```bash
streamlit run app/ui_streamlit.py
```
Open: http://localhost:8501

### Optional: LLM Replies
Set env and restart backend:
```bash
export USE_LLM=true
export OPENAI_API_KEY=sk-...     # or set in your shell/OS env
```
Templates remain the fallback if LLM fails or is off.

---

## Run with Docker

```bash
docker build -t mindcare-ai .
docker run -p 8000:8000 -p 8501:8501   -e USE_LLM=false   -e EMOTION_MODEL=bhadresh-savani/distilbert-base-uncased-emotion   mindcare-ai
```
Or with compose:
```bash
docker compose up --build
```

---

## API

- `POST /chat` → { emotion, confidence, reply }
- `GET /history?limit=100` → recent messages
- `GET /stats` → emotion counts over time
- `POST /delete_all` → clears the local DB (irreversible)

---

## Safety Notes
- This is a wellbeing companion—**not** therapy.
- Crisis text triggers helpline info and a nudge to contact trusted people.
- You control all data locally. Delete anytime from the UI sidebar.

---
