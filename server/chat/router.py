# server/chat/router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .rag_pipeline import ask_query

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/query", response_model=QueryResponse)
async def query_handler(request: QueryRequest):
    try:
        response = ask_query(request.question)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
