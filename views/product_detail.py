import streamlit as st
from services.api import get_all_medicines
from utils.helpers import currency_fmt

def main():
    sku = st.session_state.get("selected_sku")
    if not sku:
        st.warning("No se seleccionó ningún producto.")
        return

    meds = get_all_medicines()
    product = next((m for m in meds if m.get("sku") == sku), None)

    if not product:
        st.error("Producto no encontrado.")
        if st.button("Volver al listado"):
            st.session_state.selected_sku = None
            st.session_state.current_page = "list"
            st.rerun()
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            product.get("pdp_image_url") or product.get("plp_image_url") or "assets/medicines/default_plp.jpg",
            width=360
        )
    with col2:
        st.header(product.get("name"))
        st.write(f"**Marca:** {product.get('brand','N/A')}")
        st.write(f"**SKU:** {product.get('sku')}")
        st.write(f"**Farmacia:** {product.get('pharmacy_name', product.get('pharmacy','Desconocida'))}")
        st.write(f"**Precio:** {currency_fmt(product.get('price',0), product.get('currency','COP'))}")
        st.write(f"**Stock disponible:** {product.get('stock',0)}")

        qty = st.number_input("Cantidad", min_value=1, max_value=product.get("stock", 1), value=1, key=f"pd_qty_{sku}")

        if st.button("🛒 Agregar al carrito"):
            cart = st.session_state.get("cart", {})
            key = (product.get("pharmacy_id", "default"), product.get("sku"))
            if key in cart:
                cart[key]["qty"] += qty
            else:
                cart[key] = {
                    "sku": product.get("sku"),
                    "name": product.get("name"),
                    "qty": qty,
                    "price": product.get("price"),
                    "pharmacy_id": product.get("pharmacy_id"),
                    "image_url": product.get("plp_image_url", "assets/medicines/default_plp.jpg")
                }
            st.session_state.cart = cart
            st.success(f"{product.get('name')} agregado al carrito.")

    if st.button("⬅️ Volver al listado"):
        st.session_state.current_page = "list"
        st.rerun()
