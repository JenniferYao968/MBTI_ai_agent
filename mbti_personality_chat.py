import streamlit as st
import random
import os

# -----------------------------
# MBTI PERSONALITY DEFINITIONS
# -----------------------------

MBTI_DATA = {

"INTJ": {
    "label": "INTJ – The Strategist",
    "avatar": "mbti_avatars_png/intj.png",
    "responses": [
        "Let's approach this logically. What is the most efficient solution?",
        "Consider the long-term consequences before making a decision.",
        "Breaking the problem into smaller components will help solve it faster.",
        "Your challenge can likely be optimized with a better strategy."
    ]
},

"ENTP": {
    "label": "ENTP – The Debater",
    "avatar": "mbti_avatars_png/entp.png",
    "responses": [
        "Interesting question. What if we flipped the perspective?",
        "I love problems like this. Let's brainstorm wild possibilities.",
        "Maybe the best solution is one nobody has considered yet.",
        "Why not experiment and see what happens?"
    ]
},

"ENFP": {
    "label": "ENFP – The Enthusiast",
    "avatar": "mbti_avatars_png/enfp.png",
    "responses": [
        "That sounds exciting! I believe you'll find something amazing.",
        "Don't stress too much — life is an adventure!",
        "Maybe follow what energizes you the most.",
        "Every challenge is an opportunity for growth!"
    ]
},

"INFJ": {
    "label": "INFJ – The Counselor",
    "avatar": "mbti_avatars_png/infj.png",
    "responses": [
        "How does this situation align with your deeper values?",
        "Sometimes reflection reveals the best answer.",
        "Your intuition might already know the direction.",
        "Consider what choice will bring long-term fulfillment."
    ]
},

"ISTJ": {
    "label": "ISTJ – The Inspector",
    "avatar": "mbti_avatars_png/istj.png",
    "responses": [
        "Let's evaluate the facts carefully.",
        "Consistency and discipline will solve this problem.",
        "Focus on proven methods rather than risky ideas.",
        "A structured plan will help you succeed."
    ]
},

"ISFJ": {
    "label": "ISFJ – The Protector",
    "avatar": "mbti_avatars_png/isfj.png",
    "responses": [
        "Make sure your decision supports the people around you.",
        "Sometimes the most caring action is the best choice.",
        "Stability and support systems are important here.",
        "Think about how this affects your community."
    ]
},

"ESTJ": {
    "label": "ESTJ – The Executive",
    "avatar": "mbti_avatars_png/estj.png",
    "responses": [
        "Let's organize a clear plan and execute it.",
        "Efficiency matters — focus on practical results.",
        "A structured decision process will solve this.",
        "Leadership means taking decisive action."
    ]
},

"ESFJ": {
    "label": "ESFJ – The Consul",
    "avatar": "mbti_avatars_png/esfj.png",
    "responses": [
        "How will this affect the people around you?",
        "Support and harmony are important in this situation.",
        "Talking to trusted friends may help clarify things.",
        "Community perspectives might provide guidance."
    ]
},

"INTP": {
    "label": "INTP – The Thinker",
    "avatar": "mbti_avatars_png/intp.png",
    "responses": [
        "That's an interesting puzzle.",
        "Let's analyze the underlying principles.",
        "Maybe the answer lies in rethinking the assumptions.",
        "What theoretical explanation might explain this?"
    ]
},

"INFP": {
    "label": "INFP – The Idealist",
    "avatar": "mbti_avatars_png/infp.png",
    "responses": [
        "What choice feels most authentic to who you are?",
        "Follow what resonates with your inner values.",
        "Meaning and purpose are important in this decision.",
        "Trust your personal ideals."
    ]
},

"ENTJ": {
    "label": "ENTJ – The Commander",
    "avatar": "mbti_avatars_png/entj.png",
    "responses": [
        "Focus on the goal and move decisively.",
        "What strategy will maximize results?",
        "Leadership requires bold decisions.",
        "Think about scaling the outcome."
    ]
},

"ENFJ": {
    "label": "ENFJ – The Protagonist",
    "avatar": "mbti_avatars_png/enfj.png",
    "responses": [
        "How can you inspire others through this decision?",
        "Your actions can positively influence people.",
        "Think about the collective impact.",
        "Encouraging collaboration may help here."
    ]
},

"ISTP": {
    "label": "ISTP – The Craftsman",
    "avatar": "mbti_avatars_png/istp.png",
    "responses": [
        "Let's solve this step by step.",
        "Practical experimentation may help.",
        "Try testing different approaches.",
        "Hands-on experience might reveal the answer."
    ]
},

"ISFP": {
    "label": "ISFP – The Artist",
    "avatar": "mbti_avatars_png/isfp.png",
    "responses": [
        "Choose the path that feels genuine to you.",
        "Life is about expressing your true self.",
        "Maybe approach the situation creatively.",
        "Follow what brings personal harmony."
    ]
},

"ESTP": {
    "label": "ESTP – The Entrepreneur",
    "avatar": "mbti_avatars_png/estp.png",
    "responses": [
        "Why not take action and see what happens?",
        "Opportunities often appear when you move quickly.",
        "Experimentation could reveal new paths.",
        "Sometimes bold moves pay off."
    ]
},

"ESFP": {
    "label": "ESFP – The Entertainer",
    "avatar": "mbti_avatars_png/esfp.png",
    "responses": [
        "Life is meant to be enjoyed!",
        "Focus on what makes you happy right now.",
        "Maybe turn the challenge into something fun.",
        "Enjoy the moment and explore possibilities."
    ]
}

}

# -----------------------------
# STREAMLIT UI
# -----------------------------

st.set_page_config(page_title="MBTI AI Personality Demo")

st.title("MBTI Personality Chat Demo")
st.write("Choose an MBTI personality and see how they respond.")

# Select personality
selected_mbti = st.selectbox(
    "Choose a personality",
    list(MBTI_DATA.keys()),
    format_func=lambda x: MBTI_DATA[x]["label"]
)

mbti = MBTI_DATA[selected_mbti]

# Display avatar
if os.path.exists(mbti["avatar"]):
    st.image(mbti["avatar"], width=150)

# User input
user_input = st.text_input("Say something to your MBTI friend:")

# Generate response
if user_input:

    response = random.choice(mbti["responses"])

    st.markdown("### Response")
    st.write(response)