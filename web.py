import streamlit as st
from components.navbar import navbar

st.set_page_config(layout="wide")
navbar()

st.markdown("### Bienvenido al sistema de farmacias con Streamlit 🚀")
st.markdown("Usa el menú superior para navegar entre las páginas.")
