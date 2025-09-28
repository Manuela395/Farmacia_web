import streamlit as st
from components.banner import show_banner
from components.cards import medicine_card
from services.api import get_medicines_by_category, get_pharmacies

categories = [
    "Analgésicos y antipiréticos",
    "Antiinflamatorios",
    "Antibióticos",
    "Antivirales",
    "Antifúngicos",
    "Antihipertensivos",
    "Antidiabéticos",
    "Cardiovasculares",
    "Antidepresivos y ansiolíticos",
    "Antihistamínicos y antialérgicos",
    "Gastrointestinales",
    "Vitaminas y suplementos",
    "Anticonceptivos y hormonales",
    "Oftálmicos y óticos",
    "Pediátricos"
]

st.title("💊 Medicamentos")
show_banner()

st.sidebar.title("Categorías")
category = st.sidebar.selectbox("Selecciona una categoría", categories)

st.sidebar.title("Farmacias")
pharmacies = get_pharmacies()
pharmacy_names = [ph["name"] for ph in pharmacies]
selected_pharmacy = st.sidebar.selectbox("Selecciona farmacia", pharmacy_names)
pharmacy_id = next((ph["nit"] for ph in pharmacies if ph["name"] == selected_pharmacy), None)

if category and pharmacy_id:
    medicines = get_medicines_by_category(category)
    for med in medicines:
        medicine_card(med, pharmacy_id)
