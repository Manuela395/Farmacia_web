import requests

BASE_URL = "http://localhost:5000"

# ---- Farmacias ----
def get_pharmacies():
    return requests.get(f"{BASE_URL}/pharmacy/getAll").json()

def get_pharmacy(nit):
    return requests.get(f"{BASE_URL}/pharmacy/get/{nit}").json()

# ---- Medicamentos ----
def get_medicines_by_category(category):
    return requests.get(f"{BASE_URL}/medicine/getByCategory/{category}").json()

# ---- Stock ----
def get_stock_by_pharmacy(pharmacy_id):
    return requests.get(f"{BASE_URL}/stock/getByPharmacy/{pharmacy_id}").json()

def update_stock(pharmacy_id, sku, new_quantity):
    data = {"pharmacy_id": pharmacy_id, "sku": sku, "quantity": new_quantity}
    return requests.put(f"{BASE_URL}/stock/update", json=data).json()
