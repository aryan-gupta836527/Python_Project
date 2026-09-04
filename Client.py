import requests
url = "http://127.0.0.1:5000/users"
response1 = requests.post(url, json={"id": 1, "name": "John Doe"})
response2 = requests.post(url, json={"id": 1, "name": "Jane Smith"})
response3 = requests.post(url, json={"id": 2, "name": "Bob Johnson"})
response4 = requests.get(url)
print(response1.json())
print(response1.status_code)
print(response2.json())
print(response2.status_code)
print(response3.json())
print(response3.status_code)
print(response4.json())
print(response4.status_code)