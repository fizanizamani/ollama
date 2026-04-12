start cmd /k "cd /d E:\OLLAMA_PROJECT && uvicorn main:app --reload --port 800"
timeout /t 5
start cmd /k "cd /d E:\OLLAMA_PROJECT\frontend && npm run dev"
timeout /t 5
start chrome http://localhost:5173