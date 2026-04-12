import streamlit as st
import ollama

client = ollama.Client()

st.title("Model Comparison Engine")

user_input = st.text_input("Enter your question:")

if user_input:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("LLaMA 3.2")
        response1 = client.generate(
            model="llama3.2:3b",
            prompt=user_input
        )
        st.write(response1['response'])

    with col2:
        st.subheader("Qwen 3.5")
        response2 = client.generate(
            model="qwen3.5:cloud",
            prompt=user_input
        )
        st.write(response2['response'])