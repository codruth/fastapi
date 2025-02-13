import asyncio
from fastapi import FastAPI, HTTPException
from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str

app = FastAPI()

model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.3",
    device_map="auto",
    torch_dtype="auto"
)


semaphore = asyncio.Semaphore(2)
active_requests = 0


@app.post("/chat/")
async def chat(req: ChatRequest):
    global active_requests

    async with semaphore:
        active_requests += 1
        print(f"Active Requests: {active_requests}")
        print("suntem aici")
        try:

            inputs = tokenizer(req.prompt, return_tensors="pt", padding=True, truncation=True)
            inputs = inputs.to("cpu")


            outputs = model.generate(inputs.input_ids, attention_mask=inputs.attention_mask, max_length=50)

            response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            return {"response": response_text}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            async with lock:
                active_requests -= 1
            print(f"Active Requests (After Completion): {active_requests}")
