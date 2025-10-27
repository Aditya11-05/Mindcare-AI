from .safety_guard import is_crisis

HELPLINE = (
    "If you're in immediate danger, contact local emergency services now. "
    "India (24x7): AASRA Helpline 9820466726. "
    "If you can, reach a trusted friend/family right away."
)

TEMPLATES = {
    "joy": "That's wonderful to hear. Would you like to share what sparked this feeling?",
    "sadness": "I’m really sorry you’re going through this. Do you want to talk about what’s weighing on you?",
    "anger": "Your feelings are valid. Want to vent about what triggered it? I’m listening.",
    "fear": "That sounds overwhelming. Let’s try a quick grounding: name 3 things you see, 2 you hear, 1 you feel.",
    "anxiety": "It makes sense to feel this way. Try slow breathing: inhale 4, hold 4, exhale 6—repeat 4x.",
    "love": "That's heartwarming. What made you feel so connected or cared for?",
    "surprise": "Whoa—that sounds unexpected! How are you feeling about it now?",
    "neutral": "I’m here to listen. Tell me more."
}

FALLBACK = "I’m here with you. Would you like to share a bit more about what you’re feeling right now?"

def generate_reply_templates(user_text: str, emotion: str, prob: float) -> str:
    if is_crisis(user_text, emotion, prob):
        return ("I’m really glad you told me. Your safety matters most. " + HELPLINE)
    return TEMPLATES.get(emotion, FALLBACK)
