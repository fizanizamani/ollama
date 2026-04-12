from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from docx import Document
import asyncio
import pickle
import ollama
import faiss
import numpy as np
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- VECTOR DB ----------------
dimension = 1024
index = faiss.IndexFlatL2(dimension)
chunks_store = []

def load_notes():
    folder = "notes"
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".docx"):
            doc = Document(os.path.join(folder, file))
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            docs.append(text)
    return docs

def chunk(text, size=100, overlap=20):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size-overlap)]

def embed(text):
    return np.array(
        ollama.embeddings(model="mxbai-embed-large", prompt=text)["embedding"],
        dtype="float32"
    )

def build_index():
    global chunks_store, index
    if os.path.exists("index.pkl"):
        print("Loading index from cache...")
        with open("index.pkl", "rb") as f:
            data = pickle.load(f)
        chunks_store = data["chunks"]
        vectors = np.array(data["vectors"], dtype="float32")
        index.add(vectors)
        print("Index loaded!")
        return
    print("Building index from notes...")
    docs = load_notes()
    vectors = []
    for doc in docs:
        for c in chunk(doc):
            v = embed(c)
            index.add(np.array([v]))
            chunks_store.append(c)
            vectors.append(v)
    with open("index.pkl", "wb") as f:
        pickle.dump({"vectors": vectors, "chunks": chunks_store}, f)
    print("Index built and cached!")

build_index()

# ---------------- API ----------------
class Query(BaseModel):
    message: str

def search(query, k=5):
    q = embed(query)
    D, I = index.search(np.array([q]), k)
    return [chunks_store[i] for i in I[0]]

@app.post("/chat")
async def chat(query: Query):
    docs = search(query.message)
    context = "\n".join(docs)
    prompt = f"""You are a helpful AI that answers using ONLY the context.

Context:
{context}

Question:
{query.message}
"""
    res = await asyncio.to_thread(
        ollama.chat,
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"answer": res["message"]["content"]}

@app.options("/chat")
def options_chat():
    return JSONResponse(content={}, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })