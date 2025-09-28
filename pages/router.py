# pages/router.py
import pages.home as home
import pages.medicines as medicines
import pages.pharmacies as pharmacies
import pages.carshop as carshop

PAGES = {
    "home": home,
    "medicines": medicines,
    "pharmacies": pharmacies,
    "carshop": carshop,
}

def run_page(page_key: str):
    mod = PAGES.get(page_key, home)
    mod.run()
