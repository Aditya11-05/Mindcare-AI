import os
from openai import OpenAI

SYS_PROMPT = (
"You are MindCare—an empathetic, non-clinical listener. "
"Be warm, validating, and concise (<=120 words). "
"Do not diagnose or give medical instructions. "
"If the user appears in crisis, urge contacting local emergency services and share helplines. "
"Offer one gentle coping strategy (e.g., grounding or breathing) when appropriate. "
"Use simple, human language."
)

def llm_reply(user_text: str, emotion: str, prob: float) -> str:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=key)

    # Prefer a modern, safe chat model; fallback to 'gpt-4o-mini'
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    messages = [
        {"role": "system", "content": SYS_PROMPT},
        {"role": "user", "content": f"Detected emotion: {emotion} (confidence {prob:.2f}). User said: {user_text}"}
    ]
    resp = client.chat.completions.create(model=model, messages=messages, temperature=0.6)
    return resp.choices[0].message.content.strip()
