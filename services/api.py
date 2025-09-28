# services/api.py
import requests

BASE_URL = "http://localhost:5000"  
TIMEOUT = 6

def _safe_get(url):
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("GET error:", url, e)
        return None

def _safe_put(url, json_data):
    try:
        r = requests.put(url, json=json_data, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("PUT error:", url, e)
        return None

# Pharmacies
def get_pharmacies():
    res = _safe_get(f"{BASE_URL}/pharmacy/getAll")
    if isinstance(res, list):
        return res
    # fallback minimal list
    return [{"name":"Farmatodo","nit":"F01"},{"name":"Cruz Verde","nit":"F02"}]

def get_pharmacy_by_nit(nit):
    return _safe_get(f"{BASE_URL}/pharmacy/get/{nit}")

# Medicines
def get_medicines_by_category(category):
    return _safe_get(f"{BASE_URL}/medicine/getByCategory/{category}") or []

# If you have an endpoint to get all medicines, use it; otherwise we rely on categories
def get_all_medicines():
    # attempt a generic endpoint (not present in your routes by default)
    res = _safe_get(f"{BASE_URL}/medicine/getAll")
    return res or []

# Stock
def get_stock_by_pharmacy(pharmacy_id):
    return _safe_get(f"{BASE_URL}/stock/getByPharmacy/{pharmacy_id}") or []

def update_stock(pharmacy_id, sku, new_quantity):
    payload = {"pharmacy_id": pharmacy_id, "sku": sku, "quantity": new_quantity}
    return _safe_put(f"{BASE_URL}/stock/update", payload)

