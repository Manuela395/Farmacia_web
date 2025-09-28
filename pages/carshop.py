# frontend/pages/carshop.py
import streamlit as st
from services.api import post_checkout
from utils.helpers import currency_fmt

def main():
    st.title("Carrito y Pago")
    cart = st.session_state.get("cart", {})
    if not cart:
        st.info("El carrito está vacío.")
        return
    total = 0
    to_remove = []
    for k, it in cart.items():
        st.write(f"**{it['name']}** (SKU: {it['sku']})")
        qty = st.number_input(f"Cantidad_{k}", min_value=0, value=it["qty"])
        if qty == 0:
            to_remove.append(k)
        else:
            it["qty"] = qty
        subtotal = it["qty"] * it["price"]
        st.write(f"{currency_fmt(it['price'], 'COP')} — Subtotal: {subtotal:,} COP")
        total += subtotal
        if st.button(f"Eliminar {it['sku']}", key=f"del_{k}"):
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
            st.success("Pago exitoso 🎉")
            st.session_state.cart = {}
            st.experimental_rerun()
        else:
            st.error(f"Error al pagar: {res.get('error')}")

if __name__ == "__main__":
    main()