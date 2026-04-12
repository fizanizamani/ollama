import ollama

client = ollama.Client()

system_prompt = "You are an expert Python developer. Review the following code for bugs."

user_code = """
def add(a, b):
    return a - b
"""

response = client.chat(
    model="qwen3.5:cloud",
    messages=[
        {"role": "system", "content": system_prompt},   #system template
        {"role": "user", "content": user_code}          #Actual User input 
    ]
)

print(response.message.content)