import streamlit as st
from openai import OpenAI
import os
from mbti_prompts import MBTI_PROMPTS

# ---------------------------
# CONFIG
# ---------------------------

client = OpenAI()

AVATAR_PATH = "avatars"   # ← fixed: matches your actual folder name

MBTI_TYPES = {
    "INTJ": "The Architect",
    "INTP": "The Logician",
    "ENTJ": "The Commander",
    "ENTP": "The Debater",
    "INFJ": "The Advocate",
    "INFP": "The Mediator",
    "ENFJ": "The Protagonist",
    "ENFP": "The Campaigner",
    "ISTJ": "The Logistician",
    "ISFJ": "The Defender",
    "ESTJ": "The Supervisor",
    "ESFJ": "The Executive",
    "ISTP": "The Craftsman",
    "ISFP": "The Adventurer",
    "ESTP": "The Entrepreneur",
    "ESFP": "The Performer",
}

# Group colors for visual grouping on the home page
GROUP_COLORS = {
    "INTJ": "#4a55a2", "INTP": "#4a55a2", "ENTJ": "#4a55a2", "ENTP": "#4a55a2",
    "INFJ": "#218380", "INFP": "#218380", "ENFJ": "#218380", "ENFP": "#218380",
    "ISTJ": "#4a6da7", "ISFJ": "#4a6da7", "ESTJ": "#4a6da7", "ESFJ": "#4a6da7",
    "ISTP": "#c46e2f", "ISFP": "#c46e2f", "ESTP": "#c46e2f", "ESFP": "#c46e2f",
}

# ---------------------------
# PAGE CONFIG  (must be first st call)
# ---------------------------

st.set_page_config(
    page_title="MBTI Friend AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------
# SESSION STATE
# ---------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # list of {"role": ..., "content": ...}

# ---------------------------
# LANDING PAGE
# ---------------------------

def show_home():
    st.title("🧠 MBTI Friend AI")
    st.write("Pick a personality type and start chatting with your AI friend.")
    st.divider()

    cols = st.columns(4)

    for i, (mbti, desc) in enumerate(MBTI_TYPES.items()):
        avatar_path = os.path.join(AVATAR_PATH, f"{mbti}.png")
        color = GROUP_COLORS[mbti]

        with cols[i % 4]:
            # Card-style container
            with st.container(border=True):
                img_col, text_col = st.columns([1, 2])

                with img_col:
                    if os.path.exists(avatar_path):
                        st.image(avatar_path, use_container_width=True)
                    else:
                        # Fallback colored circle with initials if image missing
                        st.markdown(
                            f"""<div style="background:{color};border-radius:50%;
                            width:64px;height:64px;display:flex;align-items:center;
                            justify-content:center;font-size:18px;font-weight:bold;
                            color:white;">{mbti[:2]}</div>""",
                            unsafe_allow_html=True
                        )

                with text_col:
                    st.markdown(
                        f"<span style='font-size:20px;font-weight:700;color:{color}'>{mbti}</span>",
                        unsafe_allow_html=True
                    )
                    st.caption(desc)

                if st.button(f"Chat as {mbti}", key=f"btn_{mbti}", use_container_width=True):
                    st.session_state.selected_mbti = mbti
                    st.session_state.page = "chat"
                    st.session_state.chat_history = []
                    st.rerun()

# ---------------------------
# CHAT PAGE
# ---------------------------

def show_chat():
    mbti = st.session_state.selected_mbti
    desc = MBTI_TYPES[mbti]
    avatar_path = os.path.join(AVATAR_PATH, f"{mbti}.png")
    color = GROUP_COLORS[mbti]

    # Pull the rich system prompt from mbti_prompts.py
    system_prompt = MBTI_PROMPTS[mbti]["prompt"]

    # ── Top bar ──────────────────────────────────────────
    top_left, top_right = st.columns([5, 2])

    with top_left:
        av_col, title_col = st.columns([1, 6])
        with av_col:
            if os.path.exists(avatar_path):
                st.image(avatar_path, width=72)
        with title_col:
            st.markdown(
                f"<h2 style='margin:0;color:{color}'>{mbti} <span style='font-weight:400;font-size:18px;color:#888'>— {desc}</span></h2>",
                unsafe_allow_html=True
            )

    with top_right:
        new_mbti = st.selectbox(
            "Switch personality",
            list(MBTI_TYPES.keys()),
            index=list(MBTI_TYPES.keys()).index(mbti)
        )
        if new_mbti != mbti:
            st.session_state.selected_mbti = new_mbti
            st.session_state.chat_history = []
            st.rerun()

        if st.button("← Back to home", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.chat_history = []
            st.rerun()

    st.divider()

    # ── Chat history display ──────────────────────────────
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ── User input ────────────────────────────────────────
    prompt = st.chat_input(f"Say something to your {mbti} friend...")

    if prompt:
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        # Build full message list: system + full history
        messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200,
            temperature=1.1,
        )

        reply = response.choices[0].message.content

        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.write(reply)

# ---------------------------
# ROUTER
# ---------------------------

if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "chat":
    show_chat()