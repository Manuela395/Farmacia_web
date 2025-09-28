# frontend/pages/pharmacies.py
import streamlit as st
from services.api import get_pharmacies, get_all_medicines
from utils.helpers import currency_fmt

def main():
    st.title("Farmacias")
    phs = get_pharmacies()
    if not phs:
        st.info("No se encontró endpoint /pharmacies en el backend. Asegúrate de exponerlo o crea farmacias manualmente.")
    options = ["Todas"] + [f"{p.get('name')}|{p.get('_id', p.get('id', ''))}" for p in phs]
    sel = st.selectbox("Seleccionar farmacia", options, key="pharm_view_select")
    if sel == "Todas":
        st.session_state.selected_pharmacy = "Todas"
    else:
        _, pid = sel.rsplit("|",1)
        st.session_state.selected_pharmacy = pid

    # listar productos de esa farmacia (filtrado local)
    allm = get_all_medicines()
    sel_ph = st.session_state.get("selected_pharmacy", "Todas")
    filtered = []
    for m in allm:
        if sel_ph != "Todas" and m.get("pharmacy_id") and m.get("pharmacy_id") != sel_ph:
            continue
        if m.get("stock",1) <= 0:
            continue
        filtered.append(m)

    # mostrar grid simple
    for item in filtered[:30]:
        st.image(item.get("plp_image_url","assets/medicines/default_plp.jpg"), width=180)
        st.markdown(f"**{item.get('name')}** - {currency_fmt(item.get('price',0), item.get('currency','COP'))}")
        st.write(item.get("category"))
        if st.button("Ver detalle", key=f"ph_view_{item.get('sku')}"):
            st.session_state.view_sku = item.get("sku")
            st.experimental_rerun()

if __name__ == "__main__":
    main()