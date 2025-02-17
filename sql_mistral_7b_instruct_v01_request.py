import requests

API_URL = "http://localhost:8000/generate-sql/"

def get_sql_query(schema: str, query_description: str):
    payload = {"schema": schema, "query_description": query_description}
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("query", "No query generated")
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == "__main__":
    schema = "id, salary, nr_extra_hours"
    query_description = "I need to show all exployees who worked more than 5 extra hours"
    sql_query = get_sql_query(schema, query_description)
    print("Generated SQL Query:")
    print(sql_query)
