import time
import requests
def api_request(method, url, params=None, data=None, json=None, headers=None,max_retries=4):
    attempts = 0
    while True:
        response = requests.request(method, url, params=params, data=data, json=json, headers=headers,timeout=10)
        if response.status_code == 429:
            if attempts == max_retries:
                print("Max attempts reached")
                break
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                wait_time = int(retry_after)
            else:
                wait_time=2**attempts
            time.sleep(wait_time)
            attempts += 1
            continue
        response.raise_for_status()
        return response.json()