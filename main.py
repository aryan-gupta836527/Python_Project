import os
import requests
from dotenv import load_dotenv
import time
def api_request(method, url, headers=None, params=None,json=None,data=None,timeout=10,max_retries=3):
    attempts=0
    while True:
        response=requests.request(method, url, headers=headers, params=params, json=json, data=data, timeout=timeout)
        if response.status_code==429:
            if attempts >= max_retries:
                raise requests.exceptions.RequestException("Max retries exceeded")
            retry_after=response.headers.get("retry-after")
            if retry_after:
                wait=int(retry_after)
            else:
                wait=2**attempts
            print(f"Retrying in {wait} seconds...")
            time.sleep(wait)
            attempts+=1
            continue
        response.raise_for_status()
        return response.json()
url_search="https://api.open-meteo.com/v1/search"

