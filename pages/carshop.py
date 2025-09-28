import streamlit as st
from components.banner import render_banner
from services.api import update_stock, get_stock_by_pharmacy

def run():
    st.title("🛒 Carrito de Compras")
    render_banner()

    cart = st.session_state.get("cart", [])
    if not cart:
        st.info("Tu carrito está vacío. Agrega productos desde la lista.")
        return

    st.write("### Productos en carrito")
    total = 0
    for i, item in enumerate(cart):
        st.write(f"- **{item['name']}** | ${item['price']:,} | Cantidad: {item.get('qty',1)} | Farmacia: {item.get('pharmacy','todas')}")
        total += item['price'] * item.get('qty',1)

    st.markdown(f"**Total:** ${total:,}")

    if st.button("Finalizar compra (simulada)"):
        # simulate: for each cart item decrement stock in the item's pharmacy if provided
        errors = []
        for it in cart:
            ph = it.get("pharmacy")
            sku = it.get("sku")
            qty = it.get("qty",1)
            if not ph or ph == "todas":
                errors.append(f"No se puede descontar stock sin farmacia para {it.get('name')}")
                continue
            stock_list = get_stock_by_pharmacy(ph)
            s = next((x for x in stock_list if x.get("sku")==sku or x.get("product_sku")==sku), None)
            current = s.get("quantity",0) if s else 0
            if current < qty:
                errors.append(f"No hay suficiente stock de {it.get('name')} en {ph}")
                continue
            new_q = current - qty
            res = update_stock(ph, sku, new_q)
            if res is None:
                errors.append(f"Error actualizando stock para {it.get('name')}")
        if errors:
            st.error("Algunas compras no pudieron procesarse:")
            for e in errors:
                st.write("- " + e)
        else:
            st.success("Compra simulada: stock actualizado en las farmacias.")
            st.session_state["cart"] = []