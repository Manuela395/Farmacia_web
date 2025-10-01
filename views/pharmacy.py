import streamlit as st
from services.api import get_pharmacies, get_all_medicines
from utils.helpers import currency_fmt

def main():
    st.title("Farmacias")
    phs = get_pharmacies()
    if not phs:
        st.info("No se encontró endpoint /pharmacies en el backend.")

    options = {"Todas": "Todas"}
    for p in phs:
        options[p.get("name", "Sin nombre")] = p.get("nit")

    sel = st.selectbox("Seleccionar farmacia", list(options.keys()), key="pharm_view_select")
    st.session_state.selected_pharmacy = options[sel]

    allm = get_all_medicines()
    sel_ph = st.session_state.get("selected_pharmacy", "Todas")
    filtered = []
    for m in allm:
        if sel_ph != "Todas" and m.get("pharmacy_id") and m.get("pharmacy_id") != sel_ph:
            continue
        if m.get("stock", 1) <= 0:
            continue
        filtered.append(m)

    for item in filtered[:30]:
        st.image(item.get("plp_image_url", "assets/medicines/default_plp.jpg"), width=180)
        st.markdown(f"*{item.get('name')}* - {currency_fmt(item.get('price', 0), item.get('currency', 'COP'))}")
        st.write(item.get("category"))
        if st.button("Ver detalle", key=f"ph_view_{item.get('sku')}"):
            st.session_state.selected_sku = item.get("sku")
            st.experimental_rerun()

