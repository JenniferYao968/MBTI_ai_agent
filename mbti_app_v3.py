import streamlit as st
from openai import OpenAI
import os
from mbti_prompts import MBTI_PROMPTS

# ---------------------------
# CONFIG
# ---------------------------

client = OpenAI()

AVATAR_PATH = "avatars"

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
    "ESTJ": "The Executive",
    "ESFJ": "The Consul",
    "ISTP": "The Craftsman",
    "ISFP": "The Adventurer",
    "ESTP": "The Entrepreneur",
    "ESFP": "The Performer",
}

GROUP_COLORS = {
    "INTJ": "#4a55a2", "INTP": "#4a55a2", "ENTJ": "#4a55a2", "ENTP": "#4a55a2",
    "INFJ": "#218380", "INFP": "#218380", "ENFJ": "#218380", "ENFP": "#218380",
    "ISTJ": "#4a6da7", "ISFJ": "#4a6da7", "ESTJ": "#4a6da7", "ESFJ": "#4a6da7",
    "ISTP": "#c46e2f", "ISFP": "#c46e2f", "ESTP": "#c46e2f", "ESFP": "#c46e2f",
}

# ---------------------------
# QUIZ DATA
# ---------------------------

QUIZ_QUESTIONS = [
    {
        "dimension": "IE",
        "question": "When something is bothering you, what do you reach for first?",
        "subtitle": "Helps us understand how you like to process things.",
        "options": {
            "🗣️  Talk it out — saying it aloud helps me figure out what I actually think.": "E",
            "🤔  Sit with it alone first — I need to untangle my thoughts before I can explain them.": "I",
        }
    },
    {
        "dimension": "NS",
        "question": "What kind of conversation actually helps when you're going through something?",
        "subtitle": "Helps us understand what kind of support feels most useful.",
        "options": {
            "🌱  Dig into the deeper why — the meaning, the patterns, what it says about me.": "N",
            "🛠️  Focus on what's happening and what I can actually do about it right now.": "S",
        }
    },
    {
        "dimension": "TF",
        "question": "When a friend gives you advice, what feels most helpful?",
        "subtitle": "Helps us match you with a friend who communicates the way you like.",
        "options": {
            "💡  Be straight with me — tell me what's true, even if it's hard to hear.": "T",
            "🤗  Make me feel understood first — I need to feel heard before I can take anything in.": "F",
        }
    },
    {
        "dimension": "JP",
        "question": "What kind of energy do you want from a conversation right now?",
        "subtitle": "Helps us find a friend who matches your current headspace.",
        "options": {
            "📋  Grounded and structured — help me think clearly and figure out next steps.": "J",
            "✨  Open and spontaneous — let's just see where the conversation goes.": "P",
        }
    },
]

def derive_mbti(answers: dict) -> str:
    return (
        answers.get("IE", "I") +
        answers.get("NS", "N") +
        answers.get("TF", "T") +
        answers.get("JP", "J")
    )

def companion_blurb(mbti: str) -> str:
    blurbs = {
        "INTJ": "a sharp, strategic thinker who'll cut through the noise and help you see the bigger picture.",
        "INTP": "a curious, open-minded explorer who'll help you turn scattered thoughts into a real framework.",
        "ENTJ": "a decisive, no-nonsense friend who'll push you to stop thinking and start moving.",
        "ENTP": "a witty sparring partner who'll challenge your assumptions and make you think differently.",
        "INFJ": "a quietly perceptive friend who'll help you dig into what's really going on beneath the surface.",
        "INFP": "a gentle, empathetic friend who'll make you feel truly understood without any judgment.",
        "ENFJ": "a warm, inspiring friend who genuinely believes in you and will help you find your way forward.",
        "ENFP": "an enthusiastic, emotionally expressive friend who brings energy and warmth to whatever you're going through.",
        "ISTJ": "a reliable, grounded friend who'll help you make a solid plan and stick to it.",
        "ISFJ": "a caring, attentive friend who notices the small things and always makes sure you're okay.",
        "ESTJ": "a practical, direct friend who'll help you get organized and take action without overthinking.",
        "ESFJ": "a warm, socially attuned friend who'll check in and make sure you feel genuinely supported.",
        "ISTP": "a calm, no-fuss friend who'll help you solve the problem without drama or overcomplication.",
        "ISFP": "a gentle, present friend who'll sit with you in the feeling without trying to rush past it.",
        "ESTP": "a bold, action-first friend who'll pull you out of your head and into the moment.",
        "ESFP": "a fun, spontaneous friend who'll remind you that life doesn't always have to feel this heavy.",
    }
    return blurbs.get(mbti, "a friend who matches the way you think and communicate.")

# ---------------------------
# PAGE CONFIG
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
    st.session_state.chat_history = []

if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False

if "quiz_step" not in st.session_state:
    st.session_state.quiz_step = 0

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None




# ---------------------------
# QUIZ PAGE
# ---------------------------

def show_quiz():

    # ── RESULT SCREEN ─────────────────────────────────────
    if st.session_state.quiz_result:
        mbti   = st.session_state.quiz_result
        color  = GROUP_COLORS[mbti]
        avatar = os.path.join(AVATAR_PATH, f"{mbti}.png")

        st.markdown("### 🎉 Your ideal companion is...")
        st.markdown(" ")

        left, right = st.columns([1, 2])
        with left:
            if os.path.exists(avatar):
                st.image(avatar, use_container_width=True)
        with right:
            st.markdown(
                f"<div style='padding-top:8px'>"
                f"<span style='font-size:34px;font-weight:800;color:{color}'>{mbti}</span><br>"
                f"<span style='font-size:15px;color:#666'>{MBTI_TYPES[mbti]}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        st.markdown(" ")
        st.markdown(
            f"<div style='background:#f5f5f5;padding:14px 18px;border-radius:10px;"
            f"border-left:4px solid {color};font-size:15px;color:#333;line-height:1.7'>"
            f"Based on what you shared, we think you'd connect best with <b>{mbti}</b> — "
            f"{companion_blurb(mbti)}"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown(" ")

        if st.button(f"✅  Start chatting with {mbti}", use_container_width=True, type="primary"):
            st.session_state.selected_mbti  = mbti
            st.session_state.page           = "chat"
            st.session_state.quiz_done      = True
            st.session_state.chat_history   = []
            st.rerun()

        if st.button("👀  Browse all 16 types myself", use_container_width=True):
            st.session_state.quiz_done = True
            st.session_state.page      = "home"
            st.rerun()

    # ── QUESTION SCREEN ───────────────────────────────────
    else:
        step  = st.session_state.quiz_step
        total = len(QUIZ_QUESTIONS)
        q     = QUIZ_QUESTIONS[step]

        st.progress(step / total, text=f"Question {step + 1} of {total}")
        st.markdown(" ")

        # Disclaimer — first question only
        if step == 0:
            st.markdown(
                "<div style='background:#eef4ff;padding:12px 16px;border-radius:8px;"
                "font-size:13px;color:#444;line-height:1.65;margin-bottom:12px'>"
                "✨ <b>Quick note:</b> This isn't a personality test — it's about <i>what you need right now</i>. "
                "We want to match you with the right kind of companion: maybe a spontaneous friend who pulls you "
                "out of your head like <b>ESTP</b>, or a deep listener who helps you explore the root of things like <b>INFJ</b>."
                "</div>",
                unsafe_allow_html=True
            )

        st.markdown(f"### {q['question']}")
        st.caption(q["subtitle"])
        st.markdown(" ")

        for label, letter in q["options"].items():
            if st.button(label, use_container_width=True, key=f"q{step}_{letter}"):
                st.session_state.quiz_answers[q["dimension"]] = letter

                if step + 1 < total:
                    st.session_state.quiz_step += 1
                else:
                    st.session_state.quiz_result = derive_mbti(st.session_state.quiz_answers)

                st.rerun()

        st.markdown(" ")

        # Skip — always visible at the bottom
        _, skip_col, _ = st.columns([1, 2, 1])
        with skip_col:
            if st.button("I already know which type I want →", use_container_width=True):
                st.session_state.quiz_done = True
                st.session_state.page      = "home"
                st.rerun()


# ---------------------------
# LANDING PAGE
# ---------------------------

def show_home():
    st.title("🧠 MBTI Friend AI")
    st.write("Pick a personality type and start chatting with your AI companion.")

    # ── Quiz banner — prominent at the top ───────────────
    st.markdown(
        """<div style='background:linear-gradient(135deg,#eef4ff 0%,#f0faf8 100%);
        border:1px solid #d0dff7;border-radius:12px;padding:18px 24px;
        display:flex;align-items:center;justify-content:space-between;
        margin:12px 0 20px 0;gap:16px'>
        <div>
            <div style='font-size:16px;font-weight:700;color:#2a2a2a;margin-bottom:4px'>
                🔍 Not sure which type to pick?
            </div>
            <div style='font-size:13px;color:#555;line-height:1.5'>
                Answer 4 quick questions and we'll match you with the right companion
                — whether you need someone to pull you into action or help you dig deep.
            </div>
        </div>
        </div>""",
        unsafe_allow_html=True
    )

    # Button sits right below the banner, left-aligned to feel attached to it
    btn_col, _ = st.columns([1, 4])
    with btn_col:
        if st.button("✨  Help me choose a type", type="primary"):
            st.session_state.quiz_done    = False
            st.session_state.quiz_step    = 0
            st.session_state.quiz_answers = {}
            st.session_state.quiz_result  = None
            st.session_state.page         = "quiz"
            st.rerun()

    st.divider()

    cols = st.columns(4)

    for i, (mbti, desc) in enumerate(MBTI_TYPES.items()):
        avatar_path = os.path.join(AVATAR_PATH, f"{mbti}.png")
        color = GROUP_COLORS[mbti]

        with cols[i % 4]:
            with st.container(border=True):
                img_col, text_col = st.columns([1, 2])

                with img_col:
                    if os.path.exists(avatar_path):
                        st.image(avatar_path, use_container_width=True)
                    else:
                        st.markdown(
                            f"<div style='background:{color};border-radius:50%;"
                            f"width:64px;height:64px;display:flex;align-items:center;"
                            f"justify-content:center;font-size:18px;font-weight:bold;"
                            f"color:white'>{mbti[:2]}</div>",
                            unsafe_allow_html=True
                        )

                with text_col:
                    st.markdown(
                        f"<span style='font-size:20px;font-weight:700;color:{color}'>{mbti}</span>",
                        unsafe_allow_html=True
                    )
                    st.caption(desc)

                if st.button(f"Chat with {mbti}", key=f"btn_{mbti}", use_container_width=True):
                    st.session_state.selected_mbti = mbti
                    st.session_state.page          = "chat"
                    st.session_state.chat_history  = []
                    st.rerun()


# ---------------------------
# CHAT PAGE
# ---------------------------

def show_chat():
    mbti          = st.session_state.selected_mbti
    desc          = MBTI_TYPES[mbti]
    avatar_path   = os.path.join(AVATAR_PATH, f"{mbti}.png")
    color         = GROUP_COLORS[mbti]
    system_prompt = MBTI_PROMPTS[mbti]["prompt"]

    # ── Top bar ───────────────────────────────────────────
    top_left, top_right = st.columns([5, 2])

    with top_left:
        av_col, title_col = st.columns([1, 6])
        with av_col:
            if os.path.exists(avatar_path):
                st.image(avatar_path, width=72)
        with title_col:
            st.markdown(
                f"<h2 style='margin:0;color:{color}'>{mbti} "
                f"<span style='font-weight:400;font-size:18px;color:#888'>— {desc}</span></h2>",
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
            st.session_state.chat_history  = []
            st.rerun()

        if st.button("← Back to home", use_container_width=True):
            st.session_state.page         = "home"
            st.session_state.chat_history = []
            st.rerun()

    st.divider()

    # ── Chat history ──────────────────────────────────────
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ── User input ────────────────────────────────────────
    prompt = st.chat_input(f"Say something to your {mbti} friend...")

    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

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

if st.session_state.page == "quiz":
    show_quiz()

elif st.session_state.page == "home":
    show_home()

elif st.session_state.page == "chat":
    show_chat()
