import streamlit as st
from components.banner import render_banner
from services.api import get_pharmacies

def run():
    st.title("🏥 Farmacias")
    render_banner()

    pharmacies = get_pharmacies()
    if not pharmacies:
        st.info("No hay farmacias disponibles o el backend no respondió.")
        return

    for ph in pharmacies:
        name = ph.get("name")
        nit = ph.get("nit") or ph.get("id") or str(ph.get("_id",""))
        address = ph.get("address", "")
        city = ph.get("city", "")
        st.markdown(f"### {name}")
        st.write(f"- Identificador: **{nit}**")
        if address:
            st.write(f"- Dirección: {address}")
        if city:
            st.write(f"- Ciudad: {city}")
        st.markdown("---")

