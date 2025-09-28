# streamlit_app.py
import streamlit as st
from components.navbar import ALL_CATEGORIES
from pages import router

st.set_page_config(page_title="Web Pharmacy", layout="wide")

# initialize session state keys safely
defaults = {
    "page": "home",
    "cart": [],
    "plp_page_idx": 0,
    "selected_category": None,
    "selected_pharmacy": "todas",
    "banner_idx": 0,
    "pdp_sku": None
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# left sidebar navigation quick links
st.sidebar.title("Navegación")
choice = st.sidebar.radio("Ir a:", ["home","medicines","pharmacies","carshop"], index=["home","medicines","pharmacies","carshop"].index(st.session_state.get("page","home")))
st.session_state["page"] = choice

# run page
router.run_page(choice)

