import requests

API_URL = "http://localhost:8000/execute-sql-task/"

def send_sql_task_request(description: str, file_path: str):
    with open(file_path, "rb") as file:
        files = {"file": file}
        data = {"description": description}
        response = requests.post(API_URL, files=files, data=data)

    if response.status_code == 200:
        return response.json().get("message", "Execution failed")
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == "__main__":
    csv_file_path = "./resources/employees.csv"  # Provide the actual CSV file path
    task_description = "Remove all employees who worked less than 5 extra hours"

    response_message = send_sql_task_request(task_description, csv_file_path)
    print("Server Response:")
    print(response_message)
