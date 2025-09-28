import streamlit as st

def navbar():
    st.markdown("""
    <style>
    .navbar {
        background-color: #2E86C1;
        padding: 10px;
        text-align: center;
    }
    .navbar a {
        margin: 0 15px;
        color: white;
        font-weight: bold;
        text-decoration: none;
    }
    </style>
    <div class="navbar">
        <a href="/1_home" target="_self">🏠 Home</a>
        <a href="/2_medicines" target="_self">💊 Medicamentos</a>
        <a href="/3_pharmacies" target="_self">🏥 Farmacias</a>
        <a href="/4_carshop" target="_self">🛒 Carrito</a>
    </div>
    """, unsafe_allow_html=True)


