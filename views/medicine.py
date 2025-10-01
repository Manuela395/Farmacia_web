import streamlit as st
from services.api import get_all_medicines, get_medicines_by_category, CATEGORIES
from utils.helpers import currency_fmt

def main():
    st.title("Listado de Productos")
    # filtros superior: farmacia desde session (si existe) y categorías top5
    sel_ph = st.session_state.get("selected_pharmacy", "Todas")
    sel_cat = st.session_state.get("selected_category", "Todas")

    st.write("Categorías destacadas:")
    top5 = CATEGORIES[:5]
    for c in top5:
        if st.button(c, key=f"med_cat_{c}"):
            st.session_state.selected_category = c
            st.session_state.page_num = 1

    q = st.text_input("Buscar por nombre o marca", key="med_q")

    # obtener productos: si categoría seleccionada, pedimos al backend por categoría (optimiz.)
    if sel_cat != "Todas":
        products = get_medicines_by_category(sel_cat)
    else:
        products = get_all_medicines()

    # Filtrar por farmacia y búsqueda y stock>0
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

    # paginado 6 por página (3 x 2)
    page = st.session_state.get("page_num", 1)
    per_page = 6
    start = (page-1)*per_page
    end = start + per_page
    page_items = filtered[start:end]

    # grid
    for i in range(0, len(page_items), 3):
        row = page_items[i:i+3]
        cols = st.columns(3)
        for col, item in zip(cols, row):
            with col:
                st.image(item.get("plp_image_url", "assets/medicines/default_plp.jpg"), width=220)
                st.markdown(f"*{item.get('name')}*")
                st.write(currency_fmt(item.get("price",0), item.get("currency","COP")))
                qty = st.number_input("Cantidad", min_value=1, max_value=item.get("stock",1), value=1, key=f"qty_{item.get('sku')}")
                if st.button("Agregar al carrito", key=f"add_{item.get('sku')}"):
                    cart = st.session_state.get("cart", {})
                    key = (item.get("pharmacy_id","default"), item.get("sku"))
                    if key in cart:
                        cart[key]["qty"] += qty
                    else:
                        cart[key] = {
                            "sku": item.get("sku"),
                            "name": item.get("name"),
                            "qty": qty,
                            "price": item.get("price"),
                            "pharmacy_id": item.get("pharmacy_id")
                        }
                    st.session_state.cart = cart
                    st.success("Agregado al carrito")

    total_pages = max(1, (len(filtered)+per_page-1)//per_page)
    c1, c2, c3 = st.columns([1,1,6])
    if c1.button("<< Prev") and page>1:
        st.session_state.page_num = page-1
        st.experimental_rerun()
    c2.write(f"Página {page} / {total_pages}")
    if c3.button("Next >>") and page < total_pages:
        st.session_state.page_num = page+1
        st.experimental_rerun()

    # Sidebar cart (resumen pequeño)
    with st.sidebar:
        st.header("Carrito")
        total = 0
        cart = st.session_state.get("cart", {})
        remove_keys = []
        for k, it in cart.items():
            st.write(f"*{it['name']}*")
            qty = st.number_input(f"qty_{k}", min_value=0, value=it["qty"])
            if qty == 0:
                remove_keys.append(k)
            else:
                it["qty"] = qty
            subtotal = it["qty"] * it["price"]
            st.write(f"{it['price']:,} COP — Subtotal: {subtotal:,} COP")
            total += subtotal
            if st.button(f"Eliminar {it['sku']}", key=f"del_{k}"):
                remove_keys.append(k)
        for rk in remove_keys:
            cart.pop(rk, None)
        st.write("---")
        st.write(f"Total: {total:,} COP")
        if st.button("Pagar"):
            # preparar payload y llamar post_checkout (si existe)
            items = []
            for (ph, sku), it in cart.items():
                items.append({"pharmacy_id": it.get("pharmacy_id") or ph, "sku": it["sku"], "qty": it["qty"]})
            from services.api import post_checkout
            res = post_checkout(items)
            if res.get("ok"):
                st.success("Pago exitoso")
                st.session_state.cart = {}
                st.session_state.page_num = 1
                st.experimental_rerun()
            else:
                st.error(f"Error en pago: {res.get('error')}")

if __name__ == "_main_":
    main()