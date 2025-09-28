import streamlit as st
from components.banner import show_banner
from services.api import get_pharmacies

st.title("🏠 Bienvenido a la Plataforma de Farmacias")

show_banner()

st.sidebar.title("Farmacias")
pharmacies = get_pharmacies()
for ph in pharmacies:
    st.sidebar.write(f"🏥 {ph['name']} ({ph['nit']})")


