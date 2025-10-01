import streamlit as st
from services.api import get_all_medicines, get_medicines_by_category, CATEGORIES
from utils.helpers import currency_fmt

def main():
    st.title("Listado de Productos")
    sel_ph = st.session_state.get("selected_pharmacy", "Todas")
    sel_cat = st.session_state.get("selected_category", "Todas")

    st.write("Categorías destacadas:")
    top5 = CATEGORIES[:5]
    for c in top5:
        if st.button(c, key=f"med_cat_{c}"):
            st.session_state.selected_category = c
            st.session_state.page_num = 1

    q = st.text_input("Buscar por nombre o marca", key="med_q")

    if sel_cat != "Todas":
        products = get_medicines_by_category(sel_cat)
    else:
        products = get_all_medicines()

    filtered = []
    for m in products:
        if m.get("stock", 1) <= 0:
            continue
        if sel_ph != "Todas" and m.get("pharmacy_id") and m.get("pharmacy_id") != sel_ph:
            continue
        if q:
            if q.lower() not in m.get("name","").lower() and q.lower() not in m.get("brand","").lower():
                continue
        filtered.append(m)

    page = st.session_state.get("page_num", 1)
    per_page = 6
    start = (page-1)*per_page
    end = start + per_page
    page_items = filtered[start:end]

    for i in range(0, len(page_items), 3):
        row = page_items[i:i+3]
        cols = st.columns(3)
        for col, item in zip(cols, row):
            with col:
                st.image(item.get("plp_image_url", "assets/medicines/default_plp.jpg"), width=220)
                st.markdown(f"*{item.get('name')}*")
                st.write(currency_fmt(item.get("price",0), item.get("currency","COP")))
                if st.button("Ver detalle", key=f"med_view_{item.get('sku')}"):
                    st.session_state.selected_sku = item.get("sku")
                    st.experimental_rerun()

    total_pages = max(1, (len(filtered)+per_page-1)//per_page)
    c1, c2, c3 = st.columns([1,1,6])
    if c1.button("<< Prev") and page>1:
        st.session_state.page_num = page-1
        st.experimental_rerun()
    c2.write(f"Página {page} / {total_pages}")
    if c3.button("Next >>") and page < total_pages:
        st.session_state.page_num = page+1
        st.experimental_rerun()
