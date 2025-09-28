import streamlit as st
from components.banner import render_banner
from components.navbar import render_sidebar_pharmacies, render_top_category_submenu
from services.api import get_pharmacies, get_medicines_by_category, get_stock_by_pharmacy, get_all_medicines, update_stock
from components.cards import render_product_card

def _render_pdp(sku, selected_pharmacy):
    """Render product detail page reading medicines by category or all then find sku."""
    # try to find in all medicines first
    all_meds = get_all_medicines() or []
    prod = next((p for p in all_meds if (p.get("sku") == sku or str(p.get("_id","")) == sku or p.get("id")==sku)), None)
    # fallback: try categories
    if not prod:
        for cat in (st.session_state.get("selected_category") and [st.session_state.get("selected_category")] or []):
            lst = get_medicines_by_category(cat) or []
            prod = next((p for p in lst if (p.get("sku")==sku or p.get("id")==sku)), None)
            if prod:
                break
    if not prod:
        st.error("Producto no encontrado (verifica SKU).")
        return

    st.header(prod.get("name","Producto"))
    cols = st.columns([1,2])
    with cols[0]:
        st.image(prod.get("image") or prod.get("image_url") or "https://placehold.co/400x300", use_column_width=True)
    with cols[1]:
        st.subheader(prod.get("brand",""))
        st.write(prod.get("description","Sin descripción."))
        st.write(f"**Precio:** ${prod.get('price',0):,}")
        st.write(f"**SKU:** {prod.get('sku') or prod.get('id')}")
        # show stock per selected pharmacy
        if selected_pharmacy and selected_pharmacy != "todas":
            stock_list = get_stock_by_pharmacy(selected_pharmacy)
            s = next((x for x in stock_list if x.get("sku")== (prod.get("sku") or prod.get("id"))), None)
            qty = s.get("quantity") if s else 0
            st.write(f"**Stock en farmacia:** {qty}")
            cantidad = st.number_input("Cantidad a comprar", min_value=1, max_value=max(1, qty), value=1)
            if qty <= 0:
                st.error("No hay stock disponible en esta farmacia.")
            else:
                if st.button("Comprar ahora"):
                    new_q = qty - cantidad
                    res = update_stock(selected_pharmacy, prod.get("sku") or prod.get("id"), new_q)
                    if res is not None:
                        st.success(f"Compra simulada: {cantidad} unidad(es). Stock ahora: {new_q}")
                    else:
                        st.error("Error actualizando stock.")
        else:
            st.info("Selecciona una farmacia en la barra lateral para comprar desde un local específico.")

def run():
    st.title("💊 Medicamentos")
    render_banner()

    # sidebar pharmacies
    pharmacies = get_pharmacies()
    sel_pharmacy, labels = render_sidebar_pharmacies(pharmacies)
    prev = st.session_state.get("selected_pharmacy")
    if prev != sel_pharmacy:
        st.session_state["selected_category"] = None
        st.session_state["plp_page_idx"] = 0
    st.session_state["selected_pharmacy"] = sel_pharmacy

    # top 5 categories
    render_top_category_submenu()
    selected_cat = st.session_state.get("selected_category")

    # search
    search_by = st.selectbox("Buscar por", ["Nombre","Marca"])
    q = st.text_input("Buscar", key="med_search")

    # if a PDP SKU has been set
    if st.session_state.get("page") == "medicines_pdp" and st.session_state.get("pdp_sku"):
        _render_pdp(st.session_state["pdp_sku"], sel_pharmacy)
        if st.button("Volver al catálogo"):
            st.session_state.pop("pdp_sku", None)
            st.session_state["page"] = "medicines"
            st.experimental_rerun()
        return

    # load medicines for selected category
    medicines = []
    if selected_cat:
        medicines = get_medicines_by_category(selected_cat) or []
    else:
        # if none selected, try to show all or prompt
        medicines = get_all_medicines() or []
        if not medicines:
            st.info("Selecciona una categoría arriba o usa el buscador para filtrar medicamentos.")

    # apply search filter
    filtered = []
    for m in medicines:
        if q:
            if search_by == "Nombre" and q.lower() not in (m.get("name") or "").lower():
                continue
            if search_by == "Marca" and q.lower() not in (m.get("brand") or "").lower():
                continue
        # enforce stock > 0 when a specific pharmacy selected
        if sel_pharmacy != "todas":
            stock_list = get_stock_by_pharmacy(sel_pharmacy)
            s = next((x for x in stock_list if x.get("sku")== (m.get("sku") or m.get("id"))), None)
            if not s or s.get("quantity", 0) <= 0:
                continue
        filtered.append(m)

    # pagination: 6 per page, 3 per row
    per_page = 6
    page_idx = st.session_state.get("plp_page_idx", 0)
    total_pages = max(1, (len(filtered) + per_page - 1)//per_page)
    st.write(f"Resultados: {len(filtered)} — Página {page_idx+1}/{total_pages}")

    start = page_idx * per_page
    page_items = filtered[start:start+per_page]

    # grid 3 columns
    rows = (len(page_items) + 2)//3
    idx = 0
    for r in range(rows):
        c1, c2, c3 = st.columns(3)
        for col in (c1, c2, c3):
            if idx < len(page_items):
                with col:
                    render_product_card(page_items[idx], sel_pharmacy)
                idx += 1

    # pagination controls
    c1, c2, c3 = st.columns([1,6,1])
    with c1:
        if st.button("◀ Página anterior"):
            st.session_state["plp_page_idx"] = max(0, page_idx - 1)
            st.experimental_rerun()
    with c3:
        if st.button("Página siguiente ▶"):
            st.session_state["plp_page_idx"] = min(total_pages - 1, page_idx + 1)
            st.experimental_rerun()
