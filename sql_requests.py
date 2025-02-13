import requests

# API endpoint
url = "http://127.0.0.1:8000/execute-sql/"

# Request payload
data = {
    "query": "Get all employees with extra hours greater than 5.",
    "schema": "\"employees\" \"id\" int, \"salary\" decimal(10,2), \"nr_extra_hours\" int, primary key: \"id\" [SEP]"
}
print("Data: ", data)
# Send the POST request
response = requests.post(url, json=data, headers={"Content-Type": "application/json"})

# Print the response
print("Status Code:", response.status_code)
print("Response:", response.json())
