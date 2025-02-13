import torch
from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str

# Load Mistral 7B Instruct
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.3",
    device_map="auto",
    torch_dtype="auto"
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Replace with the frontend origin or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods: GET, POST, DELETE, etc.
    allow_headers=["*"],  # Allow all headers
)
@app.post("/chat/")
async def chat(request: ChatRequest):

    print("CUDA available:", torch.cuda.is_available())
    print("CUDA device count:", torch.cuda.device_count())

    try:
        # Tokenize the input prompt
        inputs = tokenizer(request.prompt, return_tensors="pt").to("cuda")

        # Generate response using Mistral
        outputs = model.generate(inputs.input_ids, max_length=100)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
