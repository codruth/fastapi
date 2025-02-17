from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vllm import LLM, SamplingParams
import psycopg2
import torch


app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

class SchemaRequest(BaseModel):
    schema: str
    query_description: str

DB_CONFIG = {
    "dbname": "test",
    "user": "codrut",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

class TaskRequest(BaseModel):
    description: str

llm = LLM(model="mistralai/Mistral-7B-Instruct-v0.1")
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
class SQLRequest(BaseModel):
    query: str
    schema: str

# Function to generate SQL from text
def generate_sql(natural_language_query, schema):
    input_text = f"Question: {natural_language_query} Schema: {schema}"

    print("input_text: ", input_text)
    outputs = llm.generate([input_text], sampling_params)
    print("outputs: ", outputs)
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
        print("sql_query", sql_query)
        return {"sql_query": sql_query, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
