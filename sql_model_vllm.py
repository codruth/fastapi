from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from vllm import LLM, SamplingParams
import psycopg2
import torch

# Load Hugging Face Model
model_name = "gaussalgo/T5-LM-Large-text2sql-spider"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Load the model using vLLM
llm = LLM("gaussalgo/T5-LM-Large-text2sql-spider")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


# Initialize FastAPI app
app = FastAPI()

# PostgreSQL Configuration
DB_CONFIG = {
    "dbname": "test",
    "user": "codrut",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

# Request model
class SQLRequest(BaseModel):
    query: str
    schema: str

# Function to generate SQL from text
def generate_sql(natural_language_query, schema):
    input_text = f"Question: {natural_language_query} Schema: {schema}"
    sampling_params = SamplingParams(temperature=0.0, max_tokens=150)

    outputs = llm.generate([input_text], sampling_params)
    sql_query = outputs[0].outputs[0].text.strip()

    return sql_query

# Function to execute SQL on PostgreSQL
def execute_sql(sql_query):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(sql_query)
        result = cursor.fetchall()

        conn.close()
        return result
    except Exception as e:
        return str(e)

# API Endpoint: Convert NL to SQL
@app.post("/generate-sql/")
def generate_sql_endpoint(request: SQLRequest):
    try:
        sql_query = generate_sql(request.query, request.schema)
        return {"sql_query": sql_query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoint: Convert & Execute SQL
@app.post("/execute-sql/")
def execute_sql_endpoint(request: SQLRequest):
    try:
        sql_query = generate_sql(request.query, request.schema)
        result = execute_sql(sql_query)
        return {"sql_query": sql_query, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
