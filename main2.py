import os
import openai
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Replace with the frontend origin or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods: GET, POST, DELETE, etc.
    allow_headers=["*"],  # Allow all headers
)
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat/")
async def chat(request: ChatRequest):
    print("prompt "+  request.prompt)

    if openai.api_key is None:
        print("API key not found. Make sure it's set correctly.")
    else:
        print("API key loaded successfully.")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=150
        )
        message = response.choices[0].message.content.strip()
        return {"response": message}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
