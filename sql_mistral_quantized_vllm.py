from fastapi import FastAPI, HTTPException
from vllm import LLM

app = FastAPI()



@app.post("/generate-sql/")
async def generate_sql():
    """Generate SQL query from natural language input using vLLM."""
    try:
        llm = LLM(model="google/flan-t5-small")  # A lightweight model that works on CPU
        print("vLLM is running on CPU successfully!")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Run FastAPI with:
# uvicorn filename:app --reload
