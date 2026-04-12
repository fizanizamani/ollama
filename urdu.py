# import ollama
# import streamlit as st
# client=ollama.Client()

# st.markdown("""
#     <style>
# .chat-container {
#     max-width: 700px;
#     margin: 20px auto;
#     padding: 20px;
#     background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
#     border-radius: 20px;
#     box-shadow: 0 4px 12px rgba(0,0,0,0.05);
#     box-shadow: 0 0 20px #00f2ff;
# }

# .user-msg, .bot-msg {
#     padding: 12px 16px;
#     border-radius: 15px;
#     margin: 10px 0;
#     max-width: 80%;
#     line-height: 1.5;
#     white-space: pre-wrap; /* preserves spacing & line breaks */
#     font-family: "Segoe UI", sans-serif;
# }

# .user-msg {
#     background-color: #DCF8C6; /* light green */
#     margin-left: auto;
#     text-align: left;
# }

# .bot-msg {
#     background-color: #F1F0F0; /* light gray */
#     margin-right: auto;
#     text-align: left;
# }
# </style>
# """, unsafe_allow_html=True)

# # 👇 COLUMN LAYOUT
# left, center, right = st.columns([1,2,1])

# with center:

#     st.title("HOMIE")

#     system_prompt = {
#         "role": "system",
#         "content": """
#         Tum ek funny, savage, aur entertaining besti krne wale AI chatbot ho.
#         Hamesha Roman Urdu mein jawab do.
#         Tone humorous, savage, witty aur casual honi chahiye.
#         User ko roast ko roast krte ho, disrespectful ya offensive nahi hona.
#         Helpful bhi rehna hai aur clear jawab dena hai.
#         Short aur engaging replies do aur slang word use kro.
#         jitna hosake usko roast krk uski insult karo aur mazak urao.
#         """
#     }

#     messages=st.session_state.get("messages",[])
#     if st.button("Clear Chat"):
#         messages=[]
#     st.session_state["messages"]=messages

#     if len(messages) == 0:
#           st.info("Oye! Kuch pooch na... ya bas timepass karne aaye ho?")
       
#     for msg in messages:
#             with st.chat_message(msg["role"]):
#                 st.write(msg["content"])
        
#     user_input=st.chat_input("Puch le bhai jo puchna hai")
#     if user_input:
#             messages.append({"role":"user","content":user_input})
#             with st.chat_message("user"):
#                 st.write(user_input)

#             full_messages = [system_prompt] + messages

            
#             with st.spinner("ruk ja bhai soch raha hun... thoda sabr kar"):
#              response = client.chat(
#                model="qwen3.5:cloud",
#                messages=full_messages
#             )

#             botreply = response["message"]["content"]
                
#             messages.append({"role":"assistant","content":botreply})
#             with st.chat_message("assistant"):
#              st.write(botreply)

import ollama
import streamlit as st

client = ollama.Client()

st.set_page_config(page_title="HOMIE AI", layout="centered")

# 🔥 ADVANCED UI CSS
st.markdown("""
<style>

/* 🌌 FULL PAGE BACKGROUND FIX */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: radial-gradient(circle at top left, #1f1c2c, #302b63, #0f0c29);
    color: white !important;
    height: 100%;
}

/* Ensure full height coverage */
body {
    margin: 0;
    padding: 0;
}

/* Center content */
.block-container {
    max-width: 800px;
    margin: auto;
}

/* 🔥 FORCE ALL TEXT WHITE */
* {
    color: white !important;
}

/* Chat message styling */
[data-testid="stChatMessage"] {
    padding: 12px 16px;
    border-radius: 18px;
    margin-bottom: 12px;
    max-width: 75%;
    line-height: 1.5;
    font-family: "Segoe UI", sans-serif;
    backdrop-filter: blur(10px);
}

/* 🧑 User message */
[data-testid="stChatMessage"][data-testid*="user"] {
    background: linear-gradient(135deg, #00f2ff, #0072ff);
    margin-left: auto;
    box-shadow: 0 0 15px rgba(0,242,255,0.6);
}

[data-testid="stChatMessage"][data-testid*="assistant"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.2);
    margin-right: auto;
    box-shadow: 0 0 10px rgba(255,255,255,0.1);
}

h1 {
    text-align: center;
    color: #00f2ff !important;
    text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
}

/* 💬 Input box */
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 12px !important;
}

/* Remove white header/footer areas */
header, footer {
    background: transparent !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #00f2ff;
    border-radius: 10px;
}

.stButton > button {
    background: rgba(255, 255, 255, 0.08) !important;
    color: white !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 HOMIE AI")

system_prompt = {
        "role": "system",
        "content": """
        Tum ek funny, savage, aur entertaining besti krne wale AI chatbot ho.
        Hamesha Roman Urdu mein jawab do.
        Tone humorous, savage, witty aur casual honi chahiye.
        User ko roast ko roast krte ho, disrespectful ya offensive nahi hona.
        Helpful bhi rehna hai aur clear jawab dena hai.
        Short aur engaging replies do aur slang word use kro.
        jitna hosake usko roast krk uski insult karo aur mazak urao.
        """
    }
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑 Clear Chat"):
    st.session_state.messages = []

messages = st.session_state.messages

if len(messages) == 0:
    st.info("Oye! Kuch pooch na... ya bas timepass karne aaye ho? ")

for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Puch le bhai jo puchna hai...")

if user_input:
    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    full_messages = [system_prompt] + messages

    with st.spinner("ruk ja bhai soch raha hun... thoda sabr kar"):
        response = client.chat(
            model="qwen3.5:cloud",
            messages=full_messages
        )

    botreply = response["message"]["content"]

    messages.append({"role": "assistant", "content": botreply})

    with st.chat_message("assistant"):
        st.write(botreply)