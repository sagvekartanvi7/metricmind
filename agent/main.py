from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from tools import query_semantic_layer
from agent import investigate_margin_drop, llm
from langchain_core.messages import HumanMessage

app = FastAPI(title="MetricMind Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    text_answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question_lower = request.question.lower()

    # Route "why" questions to deeper investigation
    if "why" in question_lower:
        answer = investigate_margin_drop()
        return ChatResponse(text_answer=answer)

    # Otherwise, do a simple lookup based on keywords
    metric = "revenue"
    if "cost" in question_lower:
        metric = "cost"
    elif "margin" in question_lower:
        metric = "margin"

    group_by = "transaction__region"
    if "product" in question_lower:
        group_by = "transaction__product"
    elif "quarter" in question_lower:
        group_by = "metric_time__quarter"

    raw_data = query_semantic_layer(metric, group_by)

    prompt = f"""
You are MetricMind, a business analytics assistant.
The user asked: "{request.question}"

Here is the real data from the semantic layer:
{raw_data}

Answer the user's question in 1-3 clear sentences, citing the specific numbers.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return ChatResponse(text_answer=response.content)


@app.get("/")
def health_check():
    return {"status": "MetricMind agent is running"}