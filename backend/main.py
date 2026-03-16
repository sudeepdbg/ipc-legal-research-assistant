from fastapi import FastAPI
from pydantic import BaseModel
import ollama
import os
from retriever import LegalRetriever
from prompts import build_prompt

app = FastAPI()
retriever = LegalRetriever()

class QueryRequest(BaseModel):
    text: str

@app.post("/query")
async def legal_query(request: QueryRequest):
    # 1. Retrieve relevant chunks
    results = retriever.retrieve(request.text)
    # 2. Build prompt
    prompt = build_prompt(request.text, results)
    # 3. Call Ollama
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    answer = response['message']['content']
    # Optionally return sources as well
    return {"answer": answer, "sources": results}
