# frontend/app.py
import streamlit as st
from components.banner import show_banner

st.set_page_config(
    page_title="Farmacia Online",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar variables en session_state
if "selected_pharmacy" not in st.session_state:
    st.session_state.selected_pharmacy = "Todas"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Todas"
if "page_num" not in st.session_state:
    st.session_state.page_num = 1
if "cart" not in st.session_state:
    st.session_state.cart = {}  # { (pharmacy_id, sku): {sku, name, qty, price, pharmacy_id} }

# Banner (aparece en todas las páginas)
show_banner(asset_folder="assets/banners")

st.sidebar.title("Navegación")
st.sidebar.info("Usa el menú de la izquierda para navegar")

# 🚨 IMPORTANTE:
# Streamlit automáticamente detecta los archivos dentro de /pages/
# (home.py, medicines.py, pharmacies.py, carshop.py).
# No necesitas un router manual aquí.
st.sidebar.success("Selecciona la página en el menú superior de Streamlit")
