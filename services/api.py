import requests
import os

BASE_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")

# Lista de categorías
CATEGORIES = [
    "Analgésicos y antipiréticos",
    "Antiinflamatorios",
    "Antibióticos",
    "Antivirales",
    "Antifúngicos",
    "Antihipertensivos",
    "Antidiabéticos",
    "Cardiovasculares",
    "Antidepresivos y ansiolíticos",
    "Antihistamínicos y antialérgicos",
    "Gastrointestinales",
    "Vitaminas y suplementos",
    "Anticonceptivos y hormonales",
    "Oftálmicos y óticos",
    "Pediátricos"
]


# -------- FARMACIAS --------
def get_pharmacies():
    try:
        r = requests.get(f"{BASE_URL}/pharmacy/getAll", timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error get_pharmacies:", e)
        return []

def get_pharmacy_by_nit(nit):
    try:
        r = requests.get(f"{BASE_URL}/pharmacy/get/{nit}", timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

# -------- MEDICINAS --------
def get_medicines_by_category(category: str):
    try:
        url = f"{BASE_URL}/medicine/getByCategory/{requests.utils.quote(category)}"
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error get_medicines_by_category:", e)
        return []

def get_all_medicines(categories):
    """Loop por categorías si no existe endpoint global"""
    docs, seen = [], set()
    for cat in categories:
        for m in get_medicines_by_category(cat):
            sku = m.get("sku")
            if sku and sku not in seen:
                docs.append(m)
                seen.add(sku)
    return docs

# -------- STOCK --------
def get_stock_by_pharmacy(pharmacy_id: str):
    try:
        r = requests.get(f"{BASE_URL}/stock/getByPharmacy/{pharmacy_id}", timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error get_stock_by_pharmacy:", e)
        return []

def update_stock(pharmacy_id: str, sku: str, qty: int):
    """Actualizar stock de un producto (ej. en checkout)"""
    try:
        payload = {"pharmacy_id": pharmacy_id, "sku": sku, "stock": qty}
        r = requests.put(f"{BASE_URL}/stock/update", json=payload, timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error update_stock:", e)
        return {"ok": False, "error": str(e)}

# -------- CHECKOUT --------
def post_checkout(items):
    """
    items = [{pharmacy_id, sku, qty}]
    Simula checkout: descuenta stock item por item con /stock/update
    """
    results = []
    for it in items:
        res = update_stock(it["pharmacy_id"], it["sku"], it["qty"])
        results.append(res)
    return {"ok": True, "results": results}