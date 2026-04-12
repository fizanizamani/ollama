# import streamlit as st
# import ollama 
# client= ollama.Client()
# st.title("Real-time Responsive Model")
# for i in range(1,6):
#     User_input=st.text_input(f"ENTER YOUR QUESTION {i}")
#     if User_input:
#       col1=st.columns(1)
#     with col1:
#         st.subheader("llama 3.2")
#         response1=client.generate(
#             model="llama3.2:3b";
#             prompt=User_input
#      )
#         st.write(response1[response1])


import streamlit as st
import ollama

client = ollama.Client()
st.title("Real-Time Chat with my homie")

# Initialize chat history
messages = st.session_state.get("messages", [])

# Clear chat button
if st.button("Clear Chat"):
    messages = []
st.session_state["messages"] = messages

# Display chat history
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")
if user_input:
    # Save user message
    messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Get bot response
    response = client.chat(model="qwen3.5:cloud", messages=messages)
    bot_reply = response["message"]["content"]

    # Save and display bot response
    messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.write(bot_reply)