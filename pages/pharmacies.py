import streamlit as st
from components.banner import show_banner
from services.api import get_pharmacies

st.title("🏥 Listado de Farmacias")
show_banner()

pharmacies = get_pharmacies()
for ph in pharmacies:
    st.write(f"### {ph['name']} - NIT: {ph['nit']}")

