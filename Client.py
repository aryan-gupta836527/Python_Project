import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE_URL = "http://127.0.0.1:5000"
API_KEY = os.getenv("API_KEY")
headers = {"X-API-KEY": API_KEY}
def show_response(response):
    print("\nStatus:", response.status_code)
    try:
        print("Response:", response.json())
    except:
        print("Response:", response.text)
print("\n--- GET ALL EXPENSES ---")
response = requests.get(f"{BASE_URL}/expenses",headers=headers)
show_response(response)
print("\n--- CREATE EXPENSE ---")
expense = {"id": 1,"title": "Lunch","amount": 250,"category": "Food","date": "2026-09-10"}
response = requests.post(
f"{BASE_URL}/expenses",headers=headers,json=expense)
show_response(response)
print("\n--- GET EXPENSE BY ID ---")
response = requests.get(f"{BASE_URL}/expenses/1",headers=headers)
show_response(response)
print("\n--- PUT EXPENSE ---")
updated_expense = {"id": 1,"title": "Dinner","amount": 500,"category": "Food","date": "2026-09-10"}
response = requests.put(f"{BASE_URL}/expenses/1",headers=headers,json=updated_expense)
show_response(response)
print("\n--- PATCH EXPENSE ---")
patch_data = {"id": 1,"amount": 450}
response = requests.patch(f"{BASE_URL}/expenses/1",headers=headers,json=patch_data)
show_response(response)
print("\n--- FILTER BY CATEGORY ---")
response = requests.get(f"{BASE_URL}/expenses",headers=headers,params={"category": "Food"})
show_response(response)
print("\n--- FILTER BY AMOUNT ---")
response = requests.get(f"{BASE_URL}/expenses",headers=headers,params={"min_amount": 100,"max_amount": 500})
show_response(response)
print("\n--- CATEGORY + AMOUNT FILTER ---")
response = requests.get(f"{BASE_URL}/expenses",headers=headers,params={"category": "Food","min_amount": 100})
show_response(response)
print("\n--- PAGINATION ---")
response = requests.get(f"{BASE_URL}/expenses",headers=headers,params={"skip": 0,"limit": 5})
show_response(response)
print("\n--- DELETE EXPENSE ---")
response = requests.delete(f"{BASE_URL}/expenses/1",headers=headers)
show_response(response)
print("\n--- GET DELETED EXPENSE ---")
response = requests.get(f"{BASE_URL}/expenses/1",headers=headers)
show_response(response)