# frontend/pages/home.py
import streamlit as st
from services.api import get_pharmacies, get_all_medicines, CATEGORIES

def main():
    st.title("Home - Farmacias")
    # banner ya se muestra desde app.py (componentes)
    cols = st.columns([2,8])
    with cols[0]:
        st.subheader("Farmacias")
        phs = get_pharmacies()
        options = ["Todas"]
        for p in phs:
            # guardamos name|id para poder recuperar id si hace falta
            label = f"{p.get('name')}|{p.get('_id', p.get('id', p.get('pharmacy_id', '')))}"
            options.append(label)
        sel = st.radio("Seleccionar farmacia", options, index=0, key="home_ph_select")
        if sel == "Todas":
            st.session_state.selected_pharmacy = "Todas"
        else:
            _, pid = sel.rsplit("|", 1)
            st.session_state.selected_pharmacy = pid

    with cols[1]:
        st.subheader("Categorías (top 5)")
        top5 = CATEGORIES[:5]
        for c in top5:
            if st.button(c, key=f"home_cat_{c}"):
                st.session_state.selected_category = c
                st.session_state.page_num = 1

        q = st.text_input("Buscar producto o marca", key="home_q")
        if st.button("Limpiar filtros"):
            st.session_state.selected_category = "Todas"
            st.session_state.selected_pharmacy = "Todas"
            st.session_state.page_num = 1
            st.experimental_rerun()

        # Mostrar primeros 6 productos (por defecto 'Todas')
        allm = get_all_medicines()
        # aplicar filtros simples en frontend: farmacia y categoría
        sel_ph = st.session_state.get("selected_pharmacy", "Todas")
        sel_cat = st.session_state.get("selected_category", "Todas")
        filtered = []
        for m in allm:
            # filtrar stock >0 si existe field "stock"
            if m.get("stock", 1) <= 0:
                continue
            if sel_cat != "Todas" and m.get("category") != sel_cat:
                continue
            if sel_ph != "Todas":
                # asumimos que el documento puede tener campo pharmacy_id o pharmacy_name
                if m.get("pharmacy_id") and m.get("pharmacy_id") != sel_ph:
                    continue
            if q:
                if q.lower() not in m.get("name","").lower() and q.lower() not in m.get("brand","").lower():
                    continue
            filtered.append(m)

        # paginar
        page = st.session_state.get("page_num", 1)
        per_page = 6
        start = (page-1)*per_page
        end = start + per_page
        page_items = filtered[start:end]

        cols_grid = st.columns(3)
        for i, item in enumerate(page_items):
            c = cols_grid[i % 3]
            with c:
                st.image(item.get("plp_image_url", "assets/medicines/default_plp.jpg"), width=200)
                st.markdown(f"**{item.get('name')}**")
                st.write(f"{item.get('price',0):,} {item.get('currency','COP')}")
                if st.button("Ver detalle", key=f"home_view_{item.get('sku')}"):
                    st.session_state.view_sku = item.get("sku")
                    st.experimental_rerun()

        # paginador simple
        total_pages = max(1, (len(filtered)+per_page-1)//per_page)
        c1, c2, c3 = st.columns([1,1,6])
        if c1.button("<< Prev") and page>1:
            st.session_state.page_num = page-1
            st.experimental_rerun()
        c2.write(f"Página {page} / {total_pages}")
        if c3.button("Next >>") and page < total_pages:
            st.session_state.page_num = page+1
            st.experimental_rerun()

if __name__ == "__main__":
    main()