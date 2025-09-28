import streamlit as st
from services.api import update_stock, get_stock_by_pharmacy

def medicine_card(medicine, pharmacy_id):
    col1, col2 = st.columns([3,1])
    with col1:
        st.write(f"**{medicine['name']}** ({medicine['brand']})")
        st.write(f"💲 {medicine['price']} {medicine['currency']}")
    with col2:
        if st.button(f"Comprar", key=medicine["sku"]):
            stock = get_stock_by_pharmacy(pharmacy_id)
            item_stock = next((s for s in stock if s["sku"] == medicine["sku"]), None)
            if item_stock and item_stock["quantity"] > 0:
                new_q = item_stock["quantity"] - 1
                update_stock(pharmacy_id, medicine["sku"], new_q)
                st.success(f"✅ Compra realizada. Stock: {new_q}")
            else:
                st.error("❌ No hay stock disponible")

