import streamlit as st 

try:
    from views.pharmacy import main as pharmacy_page
except Exception as e:
    pharmacy_page = None
    PHARM_IMPORT_ERR = e

try:
    from views.medicine import main as medicine_page
except Exception as e:
    medicine_page = None
    MED_IMPORT_ERR = e

try:
    from views.carshop import main as cart_page
except Exception as e:
    cart_page = None
    CART_IMPORT_ERR = e

# product_detail es opcional - si no existe, lo avisamos en UI
try:
    from views.product_detail import main as product_detail_page
except Exception as e:
    product_detail_page = None
    PD_IMPORT_ERR = e

st.set_page_config(page_title="Farmacia Online", layout="wide", initial_sidebar_state="expanded")

# Estado base
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "car" not in st.session_state:   # ✅ usar "car"
    st.session_state.car = {}
if "selected_sku" not in st.session_state:
    st.session_state.selected_sku = None

# Sidebar - navegación
st.sidebar.title("Menú")
menu = st.sidebar.radio("Ir a:", ["Home", "Farmacias", "Medicamentos", "Carrito de compras"], key="menu_select")
st.session_state.page = menu

# Sidebar - resumen carrito
st.sidebar.markdown("---")
st.sidebar.header("🛒 Carrito")
car = st.session_state.get("car", {})   # ✅ usar "car"
if car:
    total = 0
    for key, item in car.items():
        st.sidebar.write(f"{item['name']} ({item['qty']}) - {item['price']:,} COP")
        total += item["qty"] * item["price"]
    st.sidebar.write(f"**Total: {total:,.0f} COP**")
    if st.sidebar.button("Vaciar carrito"):
        st.session_state.car = {}
        st.experimental_rerun()
else:
    st.sidebar.write("Carrito vacío")

# Si hay un SKU seleccionado, mostramos el detalle (si existe la vista)
if st.session_state.get("selected_sku"):
    if product_detail_page:
        product_detail_page()
    else:
        st.error("La vista de detalle no está disponible (views/product_detail.py faltante).")
        st.write("Error de import:", PD_IMPORT_ERR)
        if st.button("Volver al listado"):
            st.session_state.selected_sku = None
            st.experimental_rerun()
else:
    if st.session_state.page == "Home":
        try:
            from Home import main as home_page
            home_page()
        except Exception as e:
            st.error("Error cargando Home.")
            st.write("Error de import:", e)
    elif st.session_state.page == "Farmacias":
        if pharmacy_page:
            pharmacy_page()
        else:
            st.error("Farmacias no disponible (views/pharmacy.py faltante).")
            st.write("Error de import:", PHARM_IMPORT_ERR)
    elif st.session_state.page == "Medicamentos":
        if medicine_page:
            medicine_page()
        else:
            st.error("Medicamentos no disponible (views/medicine.py faltante).")
            st.write("Error de import:", MED_IMPORT_ERR)
    elif st.session_state.page == "Carrito de compras":
        if cart_page:
            cart_page()
        else:
            st.error("Carrito no disponible (views/carshop.py faltante).")
            st.write("Error de import:", CART_IMPORT_ERR)
