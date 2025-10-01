import streamlit as st
from services.api import post_checkout
from utils.helpers import currency_fmt

def main():
    st.title("Carrito y Pago")
    cart = st.session_state.get("cart", {}) # 👈 Corregido: usar "cart"
    
    if not cart:
        st.info("El carrito está vacío.")
        if st.button("⬅️ Volver al catálogo"):
            st.session_state.current_page = "list"
            st.rerun()
        return

    total = 0
    to_remove = []

    # Encabezados de la tabla
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    col1.markdown("**Producto**")
    col2.markdown("**Cantidad**")
    col3.markdown("**Subtotal**")
    st.divider()

    # La clave 'k' es una tupla (pharmacy_id, sku)
    for k, it in cart.items(): 
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.markdown(f"**{it['name']}**")
                st.caption(f"SKU: {it['sku']}")

            with col2:
                qty = st.number_input(" ", min_value=0, value=it["qty"], key=f"qty_{k}", label_visibility="collapsed")
                if qty == 0:
                    to_remove.append(k)
                else:
                    it["qty"] = qty

            with col3:
                subtotal = it["qty"] * it["price"]
                st.write(f"${subtotal:,.0f} COP")
                total += subtotal

            with col4:
                if st.button("❌", key=f"del_{k}", help="Eliminar producto"):
                    to_remove.append(k)

    for r in to_remove:
        cart.pop(r, None)

    st.divider()
    
    # Resumen y botón de pago
    col_total1, col_total2 = st.columns([3, 1])
    with col_total1:
        st.subheader(f"Total a pagar: ${total:,.0f} COP")
    with col_total2:
        if st.button("Pagar ahora", use_container_width=True, type="primary"):
            items = []
            for (ph, sku), it in cart.items():
                items.append({"pharmacy_id": it.get("pharmacy_id") or ph, "sku": it["sku"], "qty": it["qty"]})
            res = post_checkout(items)
            if res.get("ok"):
                st.success("Pago exitoso 🎉. Tu carrito ha sido vaciado.")
                st.session_state.cart = {}   # 👈 Corregido: vaciar "cart"
                st.rerun() # Usar st.rerun() en lugar de experimental_rerun()
            else:
                st.error(f"Error al pagar: {res.get('error')}")

    if st.button("⬅️ Seguir comprando"):
        st.session_state.current_page = "list"
        st.rerun()
