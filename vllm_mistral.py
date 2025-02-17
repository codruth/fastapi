from fastapi import FastAPI, HTTPException
from vllm import LLM, SamplingParams

app = FastAPI()

# Load the model using VLLM (Replace with your preferred model)
llm = LLM(model="mistralai/Mistral-7B-Instruct-v0.3", dtype="float32", device="cpu")

@app.post("/chat/")
async def chat(prompt: str):
    try:
        sampling_params = SamplingParams(
            max_tokens=50,
            temperature=0.7,
            top_k=50
        )

        # Generate the output using VLLM
        output = llm.generate(prompt, sampling_params)
        response_text = output[0].outputs[0].text

        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
