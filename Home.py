# frontend/app.py
import streamlit as st
from services.api import get_pharmacies, get_all_medicines, CATEGORIES
from typing import List, Dict, Any
from components.banner import show_banner # Asumimos que show_banner existe

st.set_page_config(
    page_title="Farmacia Online",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=300) # Cache data for 5 minutes
def cached_get_pharmacies() -> List[Dict[str, Any]]:
    """Cached function to get pharmacies."""
    return get_pharmacies()

@st.cache_data(ttl=300) # Cache data for 5 minutes
def cached_get_all_medicines() -> List[Dict[str, Any]]:
    """Cached function to get all medicines."""
    return get_all_medicines()

def filter_medicines(medicines: List[Dict[str, Any]], category: str, pharmacy_id: str, query: str) -> List[Dict[str, Any]]:
    """Filters a list of medicines based on category, pharmacy, and search query."""
    filtered_list = []
    query_lower = query.lower() if query else ""

    for m in medicines:
        if m.get("stock", 1) <= 0:
            continue
        if category != "Todas" and m.get("category") != category:
            continue
        if pharmacy_id != "Todas" and m.get("pharmacy_id") != pharmacy_id:
            continue
        if query_lower and not (query_lower in m.get("name", "").lower() or query_lower in m.get("brand", "").lower()):
            continue
        filtered_list.append(m)
    return filtered_list

def main():
    # Inicializar variables en session_state si no existen
    if "selected_pharmacy" not in st.session_state:
        st.session_state.selected_pharmacy = "Todas"
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Todas"
    if "page_num" not in st.session_state:
        st.session_state.page_num = 1
    if "cart" not in st.session_state:
        st.session_state.cart = {}

    # Banner (si lo usas)
    show_banner(asset_folder="assets/banners")

    st.sidebar.title("Navegación")
    st.sidebar.info("Usa el menú para navegar entre las páginas.")

    st.title("Catálogo de Productos")
    cols = st.columns([2,8])
    with cols[0]:
        st.subheader("Farmacias")
        phs = cached_get_pharmacies()
        options = ["Todas"]
        for p in phs:
            ph_id = p.get('_id') or p.get('id') or p.get('pharmacy_id')
            label = f"{p.get('name')}|{ph_id}"
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
                st.experimental_rerun()

        q = st.text_input("Buscar producto o marca", key="home_q")
        if st.button("Limpiar filtros"):
            st.session_state.selected_category = "Todas"
            st.session_state.selected_pharmacy = "Todas"
            st.session_state.page_num = 1
            st.experimental_rerun()

        all_medicines = cached_get_all_medicines()
        sel_ph = st.session_state.get("selected_pharmacy", "Todas")
        sel_cat = st.session_state.get("selected_category", "Todas")
        filtered = filter_medicines(all_medicines, sel_cat, sel_ph, q)

        page = st.session_state.get("page_num", 1)
        per_page = 6
        start = (page-1)*per_page
        end = start + per_page
        page_items = filtered[start:end]

        if not page_items:
            st.info("No se encontraron productos con los filtros seleccionados.")

        cols_grid = st.columns(3)
        for i, item in enumerate(page_items):
            c = cols_grid[i % 3]
            with c:
                st.image(item.get("plp_image_url", "assets/medicines/default_plp.jpg"), width=200)
                st.markdown(f"**{item.get('name')}**")
                st.write(f"{item.get('price',0):,} {item.get('currency','COP')}")
                if st.button("Ver detalle", key=f"home_view_{item.get('sku')}"):
                    st.session_state.selected_sku = item.get("sku")
                    st.experimental_rerun()

        total_pages = (len(filtered) + per_page - 1) // per_page if filtered else 1
        c1, c2, c3 = st.columns([1,1,6])
        if page > 1 and c1.button("<< Prev"):
            st.session_state.page_num = page-1
            st.experimental_rerun()
        c2.write(f"Página {page} / {total_pages}")
        if page < total_pages and c3.button("Next >>"):
            st.session_state.page_num = page+1
            st.experimental_rerun()

if __name__ == "__main__":
    main()
