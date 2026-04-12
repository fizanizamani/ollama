import streamlit as st
import ollama
import json

client = ollama.Client()

st.title("Autonomous Qwen Orchestrator ")

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("Enter your task...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    planner_prompt = f"""
    You are an intelligent AI orchestrator.

    User request: {user_input}

    Your job:
    - Break task into sub-tasks
    - Decide how many models are needed
    - Choose models yourself (llama3.2:3b  , glm-5.1:cloud, gemini-3-flash-preview:cloud,qwen3-coder-next:cloud,)
    - Assign each model a task

    Respond ONLY in JSON format like:
    {{
      "tasks": [
        {{
          "model": "model_name",
          "instruction": "what this model should do"
        }},
        {{
          "model": "model_name",
          "instruction": "what this model should do"
        }}
      ]
    }}
    """

    qwen_response = client.chat(
        model="qwen3.5:cloud",
        messages=[{"role": "user", "content": planner_prompt}]
    )

    plan_text = qwen_response["message"]["content"]

    # Show raw plan
    with st.chat_message("assistant"):
        st.write(" Qwen Plan:")
        st.write(plan_text)

    try:
        plan_json = json.loads(plan_text)
        tasks = plan_json["tasks"]
    except:
        tasks = [{"model": "llama3", "instruction": user_input}]

    results = []

    for task in tasks:
        model_name = task["model"]
        instruction = task["instruction"]

        response = client.chat(
            model=model_name,
            messages=[{"role": "user", "content": instruction}]
        )

        output = response["message"]["content"]

        results.append(f"###  {model_name}\n{output}")

    final_output = "\n\n---\n\n".join(results)

    st.session_state.messages.append({
        "role": "assistant",
        "content": final_output
    })

    with st.chat_message("assistant"):
        st.markdown(final_output)