from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent

app = FastAPI(title="MetricMind Agent API")

# Allow our Next.js frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local dev only — we'll tighten this later
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    text_answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = agent.invoke({"messages": [{"role": "user", "content": request.question}]})
    final_message = result["messages"][-1]
    return ChatResponse(text_answer=final_message.content)


@app.get("/")
def health_check():
    return {"status": "MetricMind agent is running"}