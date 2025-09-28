import streamlit as st

ALL_CATEGORIES = [
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
    "Pediátricos",
]

# Visible top-right submenu (first 5 by default)
VISIBLE_CATEGORIES = ALL_CATEGORIES[:5]

def render_sidebar_pharmacies(pharmacies_list):
    """
    Renders left sidebar pharmacy selector. Accepts list of pharmacy dicts from backend.
    Returns selected pharmacy id or 'todas'.
    """
    st.sidebar.header("Farmacias")
    opts = ["todas"]
    labels = {"todas":"Todas"}
    for ph in pharmacies_list:
        pid = ph.get("nit") or ph.get("id") or str(ph.get("_id", "")) or ph.get("pharmacy_id")
        opts.append(pid)
        labels[pid] = ph.get("name", pid)
    sel = st.sidebar.radio("Selecciona farmacia:", opts, index=0, format_func=lambda x: labels.get(x, x))
    # handle reset rules externally
    return sel, labels

def render_top_category_submenu():
    """
    Renders 5-category submenu aligned to the right under the banner.
    Stores selection to st.session_state['selected_category'].
    """
    cols = st.columns([3,3,3,3,3,2])  # last col spacer
    for i, cat in enumerate(VISIBLE_CATEGORIES):
        if cols[i].button(cat):
            st.session_state["selected_category"] = cat
            st.session_state["plp_page_idx"] = 0
    # Option to choose other categories
    other = st.selectbox("Más categorías", ["--"] + ALL_CATEGORIES[5:], index=0)
    if other and other != "--":
        st.session_state["selected_category"] = other
        st.session_state["plp_page_idx"] = 0

