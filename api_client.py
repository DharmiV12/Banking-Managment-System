import requests

BASE_URL = "http://127.0.0.1:8000"

def create_account(data):
    try:
        return requests.post(f"{BASE_URL}/create-account/", json=data)
    except requests.exceptions.ConnectionError:
        return None

def deposit(data):
    try:
        return requests.post(f"{BASE_URL}/deposite/", json=data)
    except requests.exceptions.ConnectionError:
        return None

def withdraw(data):
    try:
        return requests.post(f"{BASE_URL}/withdrawal/", json=data)
    except requests.exceptions.ConnectionError:
        return None
    
def get_balance(account_id):
    try:
        return requests.get(f"{BASE_URL}/get-balance/{account_id}")
    except requests.exceptions.ConnectionError:
        return None
    
def get_account(account_id):
    try:
        return requests.get(f"{BASE_URL}/get-account/{account_id}")
    except requests.exceptions.ConnectionError:
        return None
    
def transaction_history(account_id):
    try:
        return requests.get(f"{BASE_URL}/transaction-history/{account_id}")
    except requests.exceptions.ConnectionError:
        return None
    
def update_account(account_id, params):
    try:
        return requests.put(
        f"{BASE_URL}/update-account/{account_id}",
        params=params
    )
    except requests.exceptions.ConnectionError:
        return None

def delete_account(account_id):
    try:
        return requests.delete(f"{BASE_URL}/delete-account/{account_id}")
    except requests.exceptions.ConnectionError:
        return None