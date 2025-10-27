import os
import requests
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="MindCare AI", page_icon="🫶", layout="centered")
st.title("🫶 MindCare AI")

API = os.getenv("API_BASE", "http://localhost:8000")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Sidebar: mood chart + admin
with st.sidebar:
    st.header("Mood Overview")
    try:
        r = requests.get(f"{API}/stats", timeout=15)
        counts = r.json().get("emotion_counts", {})
        if counts:
            labels, values = list(counts.keys()), list(counts.values())
            fig = plt.figure()
            plt.bar(labels, values)
            plt.title("User Emotion Counts")
            plt.xlabel("Emotion")
            plt.ylabel("Count")
            st.pyplot(fig)
        else:
            st.caption("No data yet.")
    except Exception as e:
        st.caption(f"Stats unavailable: {e}")

    st.markdown("---")
    if st.button("🗑️ Delete all data"):
        try:
            requests.post(f"{API}/delete_all", timeout=15)
            st.success("All messages deleted.")
            st.session_state.chat = []
        except Exception as e:
            st.error(f"Delete failed: {e}")

# --- Chat form (renamed to avoid key conflict) ---
with st.form("chat_form"):
    txt = st.text_area(
        "Share what's on your mind…",
        height=130,
        placeholder="Type here…",
        key="chat_input"  # Unique key for the text area
    )
    submitted = st.form_submit_button("Send")

# --- Handle chat submission ---
if submitted and txt.strip():
    try:
        r = requests.post(f"{API}/chat", json={"text": txt.strip()}, timeout=30)
        r.raise_for_status()
        data = r.json()

        # Append user + AI messages to session_state
        st.session_state.chat.append({"role": "user", "text": txt.strip()})
        st.session_state.chat.append({
            "role": "ai",
            "text": data.get("reply", ""),
            "emotion": data.get("emotion"),
            "conf": data.get("confidence", 0.0)
        })
    except Exception as e:
        st.error(f"Backend error: {e}")

# --- Load chat history (first run only) ---
if not st.session_state.chat:
    try:
        hist = requests.get(f"{API}/history?limit=50", timeout=15).json()
        for m in hist:
            if m["role"] == "user":
                st.session_state.chat.append({"role": "user", "text": m["text"]})
            elif m["role"] == "ai":
                st.session_state.chat.append({
                    "role": "ai",
                    "text": m["text"],
                    "emotion": m.get("emotion"),
                    "conf": m.get("confidence", 0.0)
                })
    except Exception:
        pass

# --- Render chat messages ---
for msg in st.session_state.chat[-40:]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        emo = msg.get("emotion", "")
        conf = msg.get("conf", 0.0)
        st.markdown(f"**MindCare ({emo} · {conf:.2f}):** {msg['text']}")

# --- Footer disclaimer ---
st.caption("""
**Disclaimer:** This tool does not provide medical or clinical advice.  
If you're in crisis, contact local emergency services immediately.  
India (24x7): AASRA Helpline 9820466726.
""")
