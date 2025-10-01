import streamlit as st
from services.api import post_checkout
from utils.helpers import currency_fmt

def main():
    st.title("Carrito y Pago")
    cart = st.session_state.get("cart", {}) # 👈 Corregido: usar "cart"
    if not cart:
        st.info("El carrito está vacío.")
        return

    total = 0
    to_remove = []

    # La clave 'k' es una tupla (pharmacy_id, sku)
    for k, it in cart.items(): 
        ph_id, sku = k  # 👈 Desempaquetar la clave aquí
        st.write(f"*{it['name']}* (SKU: {it['sku']})")
        qty = st.number_input(f"Cantidad_{k}", min_value=0, value=it["qty"])
        if qty == 0:
            to_remove.append(k)
        else:
            it["qty"] = qty # Actualizar cantidad en el carrito

        subtotal = it["qty"] * it["price"]
        st.write(f"{currency_fmt(it['price'], 'COP')} — Subtotal: {subtotal:,} COP")
        total += subtotal

        if st.button(f"Eliminar", key=f"del_{k}"): # Texto del botón simplificado
            to_remove.append(k)

    for r in to_remove:
        cart.pop(r, None)

    st.write("---")
    st.write(f"Total a pagar: {total:,} COP")

    if st.button("Pagar ahora"):
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
