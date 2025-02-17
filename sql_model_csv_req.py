import requests

# API Endpoint
url = "http://127.0.0.1:8000/upload-csv/"

# Path to the CSV file
file_path = "./resources/employees.csv"

# Natural Language Request
request_text = "Insert all records from CSV to employee table"

# Prepare the file for upload
files = {"file": open(file_path, "rb")}
data = {"request": request_text}

# Send the POST request
response = requests.post(url, files=files, data=data)

# Print the API response
print(response.json())
