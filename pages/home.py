# pages/home.py
import streamlit as st
from components.banner import render_banner
from components.navbar import render_sidebar_pharmacies, render_top_category_submenu, ALL_CATEGORIES
from services.api import get_pharmacies, get_medicines_by_category, get_stock_by_pharmacy
from components.cards import render_product_card

def run():
    st.title("🏠 Home - Farmacias")
    render_banner()

    # Sidebar: pharmacies
    pharmacies = get_pharmacies()
    sel_pharmacy, ph_labels = render_sidebar_pharmacies(pharmacies)

    # If pharmacy changed, clear category per requirement
    prev = st.session_state.get("selected_pharmacy")
    if prev != sel_pharmacy:
        st.session_state["selected_category"] = None
        st.session_state["plp_page_idx"] = 0
    st.session_state["selected_pharmacy"] = sel_pharmacy

    # Top-right submenu of 5 categories
    render_top_category_submenu()
    selected_cat = st.session_state.get("selected_category")

    if selected_cat:
        st.info(f"Categoría seleccionada: **{selected_cat}**")

    # Search area
    search_by = st.selectbox("Buscar por:", ["Nombre", "Marca"], index=0)
    q = st.text_input("Buscar producto (presiona Enter para aplicar):", value="", key="home_search")

    # Load medicines list based on category (if any)
    medicines = []
    if selected_cat:
        medicines = get_medicines_by_category(selected_cat) or []
    else:
        # if no category selected, show prompt
        st.info("Selecciona una categoría en el submenú para ver productos aquí (o ve a 'Medicines').")
        medicines = []

    # Filter by search (name or brand) and by stock per pharmacy rules
    filtered = []
    for m in medicines:
        name = (m.get("name") or "").lower()
        brand = (m.get("brand") or "").lower()
        if q:
            if search_by == "Nombre" and q.lower() not in name:
                continue
            if search_by == "Marca" and q.lower() not in brand:
                continue

        # stock filter: if a specific pharmacy selected, product must have stock >0 there
        if sel_pharmacy != "todas":
            stock_list = get_stock_by_pharmacy(sel_pharmacy)
            # find by sku
            sku = m.get("sku") or m.get("id")
            s = next((x for x in stock_list if x.get("sku") == sku or x.get("product_sku") == sku), None)
            if not s or s.get("quantity", 0) <= 0:
                continue
        # if 'todas' we include product (later PDP/cart will check stock when buying)
        filtered.append(m)

    # Pagination 6 per page
    per_page = 6
    page_idx = st.session_state.get("plp_page_idx", 0)
    total_pages = max(1, (len(filtered) + per_page - 1) // per_page)
    st.write(f"Resultados: {len(filtered)} — Página {page_idx+1} de {total_pages}")

    start = page_idx * per_page
    for prod in filtered[start:start+per_page]:
        render_product_card(prod, sel_pharmacy)

    # Pagination controls
    c1, c2, c3 = st.columns([1,6,1])
    with c1:
        if st.button("◀ Página anterior"):
            st.session_state["plp_page_idx"] = max(0, page_idx - 1)
            st.experimental_rerun()
    with c3:
        if st.button("Página siguiente ▶"):
            st.session_state["plp_page_idx"] = min(total_pages - 1, page_idx + 1)
            st.experimental_rerun()

