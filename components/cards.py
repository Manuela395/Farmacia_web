import streamlit as st
from services.api import get_stock_by_pharmacy, update_stock

def _find_stock(stock_list, sku):
    # stock_list expected list of dicts: {'sku':..., 'quantity':...} or similar
    for s in stock_list:
        # try common keys
        if s.get("sku") == sku or s.get("product_sku") == sku or s.get("code") == sku:
            return s
    return None

def render_product_card(product: dict, selected_pharmacy_id: str):
    """
    Renders product card with image, name, brand, price, SKU and buy buttons.
    product keys expected: name, brand, price, currency, sku, image (optional), description
    """
    img = product.get("image") or product.get("image_url") or "https://placehold.co/300x180"
    name = product.get("name", "Sin nombre")
    brand = product.get("brand", "")
    price = product.get("price", 0)
    sku = product.get("sku") or product.get("id")
    desc = product.get("description", "")

    c1, c2 = st.columns([1,2])
    with c1:
        st.image(img, use_column_width=True)
    with c2:
        st.markdown(f"**{name}**")
        if brand:
            st.markdown(f"*{brand}*")
        st.markdown(f"**Precio:** ${price:,}")
        st.markdown(f"**SKU:** {sku}")
    st.image(img, use_column_width=True)
    st.markdown(f"**{name}**")
    if brand:
        st.markdown(f"*{brand}*")
    st.markdown(f"**Precio:** ${price:,}")
    st.markdown(f"**SKU:** {sku}")

        # stock depending on pharmacy
        if selected_pharmacy_id and selected_pharmacy_id != "todas":
            stock_list = get_stock_by_pharmacy(selected_pharmacy_id)
            item = _find_stock(stock_list, sku)
            qty = item.get("quantity", 0) if item else 0
            st.markdown(f"**Stock en farmacia:** {qty}")
        else:
            st.info("Selecciona una farmacia para ver stock por local o déjalo en 'Todas' para ver todos.")
    # stock depending on pharmacy
    if selected_pharmacy_id and selected_pharmacy_id != "todas":
        stock_list = get_stock_by_pharmacy(selected_pharmacy_id)
        item = _find_stock(stock_list, sku)
        qty = item.get("quantity", 0) if item else 0
        st.markdown(f"**Stock en farmacia:** {qty}")
    else:
        st.info("Selecciona una farmacia para ver stock por local o déjalo en 'Todas' para ver todos.")

        cols = st.columns([1,1,1])
        if cols[0].button("Ver producto", key=f"view_{sku}"):
            st.session_state["page"] = "medicines_pdp"
            st.session_state["pdp_sku"] = sku
            st.experimental_rerun()
    cols = st.columns([1,1,1])
    if cols[0].button("Ver producto", key=f"view_{sku}"):
        st.session_state["page"] = "medicines_pdp"
        st.session_state["pdp_sku"] = sku
        st.experimental_rerun()

        # Comprar 1 (si stock disponible)
        if selected_pharmacy_id and selected_pharmacy_id != "todas":
            if qty > 0:
                if cols[1].button("Comprar 1", key=f"buy1_{sku}"):
                    new_q = qty - 1
                    res = update_stock(selected_pharmacy_id, sku, new_q)
                    if res is not None:
                        st.success(f"Compra simulada. Nuevo stock: {new_q}")
                        # optionally refresh page
                        st.experimental_rerun()
                    else:
                        st.error("Error actualizando stock en backend.")
            else:
                cols[1].button("Comprar 1", key=f"buy1_disabled_{sku}", disabled=True)
    # Comprar 1 (si stock disponible)
    if selected_pharmacy_id and selected_pharmacy_id != "todas":
        if qty > 0:
            if cols[1].button("Comprar 1", key=f"buy1_{sku}"):
                new_q = qty - 1
                res = update_stock(selected_pharmacy_id, sku, new_q)
                if res is not None:
                    st.success(f"Compra simulada. Nuevo stock: {new_q}")
                    # optionally refresh page
                    st.experimental_rerun()
                else:
                    st.error("Error actualizando stock en backend.")
        else:
            cols[1].button("Comprar 1", key=f"buy1_no_pharmacy_{sku}", disabled=True)
            cols[1].button("Comprar 1", key=f"buy1_disabled_{sku}", disabled=True)
    else:
        cols[1].button("Comprar 1", key=f"buy1_no_pharmacy_{sku}", disabled=True)

        if cols[2].button("Agregar al carrito", key=f"cart_{sku}"):
            cart = st.session_state.get("cart", [])
            # check if item already in cart for same pharmacy
            cart.append({"sku": sku, "name": name, "price": price, "qty": 1, "pharmacy": selected_pharmacy_id})
            st.session_state["cart"] = cart
            st.success("Añadido al carrito")


    if cols[2].button("Agregar al carrito", key=f"cart_{sku}"):
        cart = st.session_state.get("cart", [])
        # check if item already in cart for same pharmacy
        cart.append({"sku": sku, "name": name, "price": price, "qty": 1, "pharmacy": selected_pharmacy_id})
        st.session_state["cart"] = cart
        st.success("Añadido al carrito")
