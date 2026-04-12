import ollama
import ollama

client = ollama.Client()

model = "llama3.2:3b"

prompt = "Which Model are you and what can you do?"

response = client.generate(model, prompt)
print("Response from Ollama:")
print(response.response)