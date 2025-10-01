import streamlit as st
from services.api import get_pharmacies, get_all_medicines, CATEGORIES
from typing import List, Dict, Any
from components.banner import show_banner

st.set_page_config(
    page_title="Farmacia Online",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=300)
def cached_get_pharmacies() -> List[Dict[str, Any]]:
    return get_pharmacies()

@st.cache_data(ttl=300)
def cached_get_all_medicines() -> List[Dict[str, Any]]:
    return get_all_medicines()

def filter_medicines(medicines, category, pharmacy_id, query):
    filtered = []
    query_lower = query.lower() if query else ""

    for m in medicines:
        if m.get("stock", 0) <= 0:
            continue
        if category != "Todas" and m.get("category", "").strip().lower() != category.strip().lower():
            continue
        if pharmacy_id != "Todas" and str(m.get("pharmacy_id")) != str(pharmacy_id):
            continue
        if query_lower and not (
            query_lower in m.get("name", "").lower()
            or query_lower in m.get("brand", "").lower()
        ):
            continue
        filtered.append(m)

    return filtered

def main():
    # Estado inicial
    if "selected_pharmacy" not in st.session_state:
        st.session_state.selected_pharmacy = "Todas"
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Todas"
    if "page_num" not in st.session_state:
        st.session_state.page_num = 1
    if "cart" not in st.session_state:
        st.session_state.cart = {}

    # Sidebar: farmacias
    st.sidebar.title("Farmacias")
    phs = cached_get_pharmacies()
    options = {"Todas": "Todas"}
    for ph in phs:
        options[ph.get("name", "Desconocida")] = ph.get("id") or ph.get("nit")

    sel = st.sidebar.radio("Seleccionar farmacia", list(options.keys()), index=0, key="home_ph_select")
    st.session_state.selected_pharmacy = options[sel]

    # Banner superior
    show_banner(asset_folder="assets/banners")

    # Categorías (top 5)
    st.subheader("Categorías (top 5)")
    top5 = CATEGORIES[:5]
    cols = st.columns(len(top5))
    for i, c in enumerate(top5):
        if cols[i].button(c, key=f"home_cat_{c}"):
            st.session_state.selected_category = c
            st.session_state.page_num = 1
            st.rerun()   # ✅ reemplazo

    # Buscador
    q = st.text_input("Buscar producto o marca", key="home_q")
    if st.button("Limpiar filtros"):
        st.session_state.selected_category = "Todas"
        st.session_state.selected_pharmacy = "Todas"
        st.session_state.page_num = 1
        st.rerun()   

    # Listado de productos
    all_medicines = cached_get_all_medicines()
    sel_ph = st.session_state.get("selected_pharmacy", "Todas")
    sel_cat = st.session_state.get("selected_category", "Todas")
    filtered = filter_medicines(all_medicines, sel_cat, sel_ph, q)

    # Paginación
    page = st.session_state.get("page_num", 1)
    per_page = 6
    start = (page - 1) * per_page
    end = start + per_page
    page_items = filtered[start:end]

    if not page_items:
        st.info("No se encontraron productos con los filtros seleccionados.")

    # Mostrar en grilla
    cols_grid = st.columns(3)
    for i, item in enumerate(page_items):
        c = cols_grid[i % 3]
        with c:
            st.image(item.get("plp_image_url", "assets/medicines/default_plp.jpg"),
                     width=200, use_container_width=False)
            st.markdown(f"**{item.get('name')}**")
            st.write(f"{item.get('price',0):,} {item.get('currency','COP')}")
            if st.button("Ver detalle", key=f"home_view_{item.get('sku')}"):
                st.session_state.selected_sku = item.get("sku")
                st.rerun()   # ✅ reemplazo

    # Navegación
    total_pages = (len(filtered) + per_page - 1) // per_page if filtered else 1
    c1, c2, c3 = st.columns([1, 1, 6])
    if page > 1 and c1.button("<< Prev"):
        st.session_state.page_num = page - 1
        st.rerun()   # ✅ reemplazo
    c2.write(f"Página {page} / {total_pages}")
    if page < total_pages and c3.button("Next >>"):
        st.session_state.page_num = page + 1
        st.rerun()   

if __name__ == "__main__":
    main()

