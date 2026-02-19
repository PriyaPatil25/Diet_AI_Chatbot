from fastapi import FastAPI, Cookie, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import ChatRequest
from database import collection, get_history
from llm import chain
from datetime import datetime
import uuid
import time

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.get("/")
def home():
    return {"message": "Diet Specialist Backend Running"}


@app.post("/chat")
def chat(request: ChatRequest, response: Response, session_id: str = Cookie(default=None)):

    # 1️⃣ Validate input early
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # 2️⃣ Create session if not exists
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id)

    # 3️⃣ Load limited history
    history = get_history(session_id)

    try:
        # 4️⃣ Measure LLM latency
        start_time = time.time()

        llm_response = chain.invoke({
            "history": history,
            "question": request.question
        })

        latency = round(time.time() - start_time, 2)
        assistant_reply = llm_response.content

    except Exception:
        raise HTTPException(status_code=500, detail="LLM service unavailable")

    # 5️⃣ Store user message
    collection.insert_one({
        "user_id": session_id,
        "role": "user",
        "message": request.question,
        "timestamp": datetime.utcnow()
    })

    # 6️⃣ Store assistant message (with latency)
    collection.insert_one({
        "user_id": session_id,
        "role": "assistant",
        "message": assistant_reply,
        "latency": latency,
        "timestamp": datetime.utcnow()
    })

    return {
        "response": assistant_reply,
        "latency": latency
    }
