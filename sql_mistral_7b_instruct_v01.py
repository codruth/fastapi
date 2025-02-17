from fastapi import FastAPI
from pydantic import BaseModel
from vllm import LLM, SamplingParams

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

class SchemaRequest(BaseModel):
    schema: str
    query_description: str

llm = LLM(model="mistralai/Mistral-7B-Instruct-v0.1")
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

@app.post("/generate-text/")
def generate_text(request: PromptRequest):
    outputs = llm.generate([request.prompt], sampling_params)
    generated_text = outputs[0].outputs[0].text if outputs else ""
    return {"prompt": request.prompt, "generated_text": generated_text}

@app.post("/generate-sql/")
def generate_sql(request: SchemaRequest):
    prompt = f"Generate an SQL query for the following schema: {request.schema}. The query should {request.query_description}."
    outputs = llm.generate([prompt], sampling_params)
    generated_query = outputs[0].outputs[0].text if outputs else ""
    return {"schema": request.schema, "query": generated_query}
