from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import pandas as pd
import psycopg2
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from io import StringIO

app = FastAPI()

# PostgreSQL Configuration
DB_CONFIG = {
    "dbname": "test",  # Change this to your database name
    "user": "codrut",  # Change this to your database username
    "password": "admin",  # Change this to your database password
    "host": "localhost",
    "port": "5432",
}

MODEL_NAME = "gaussalgo/T5-LM-Large-text2sql-spider"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def get_db_connection():
    """Connect to PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def generate_sql_query(natural_language_query, table_name, df):
    """Use T5-LM-Large-text2sql-spider to generate an SQL query."""

    # Extract schema dynamically from DataFrame
    schema = ", ".join([f"{col} {str(df[col].dtype)}" for col in df.columns])

    print("natural_language_query: ", natural_language_query)

    input_text = f"""
    Convert this natural language request into a SQL INSERT statement for PostgreSQL.
    
    Request: "{natural_language_query}"
    
    The SQL should insert multiple rows using placeholders (%s).

    Table: {table_name}

    Schema:
    {schema}

    """

    print("input_text: ", input_text)

    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)
    outputs = model.generate(inputs.input_ids, max_length=256)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("generated_sql: ", generated_sql)

    if "INSERT INTO" not in generated_sql:
        raise ValueError("LLM did not generate a valid INSERT query")

    return generated_sql

@app.post("/upload-csv/")
async def upload_csv(
        file: UploadFile = File(...),
        request: str = Form(...)
):
    """Upload a CSV file and insert data using an LLM-generated SQL query."""
    try:
        # Read CSV content
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode("utf-8")))

        # Ensure required columns exist
        required_columns = {"salary", "nr_extra_hours"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail="CSV must contain 'salary' and 'nr_extra_hours'")

        # Generate SQL query using LLM
        table_name = "employees"
        insert_query = generate_sql_query(request, table_name, df)

        # Connect to PostgreSQL and execute query
        conn = get_db_connection()
        cursor = conn.cursor()

        values = [tuple(row) for row in df.itertuples(index=False, name=None)]
        cursor.executemany(insert_query, values)

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "CSV data successfully inserted into employees table"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
