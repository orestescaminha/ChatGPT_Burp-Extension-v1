# ai_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class PromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500

class PromptResponse(BaseModel):
    response: str
    usage: dict

@app.post("/api/chat", response_model=PromptResponse)
async def chat(request: PromptRequest):
    try:
        response = openai.ChatCompletion.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens
        )
        return PromptResponse(
            response=response.choices[0].message.content,
            usage=response.usage.dict()
        )
    except openai.OpenAIError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
