import streamlit as st

# Banners: horizontal images + call-to-action message.
# Reemplaza las URLs por tus imágenes/banner si lo deseas.
BANNERS = [
    {
        "img":"https://placehold.co/1200x300/0ea5e9/ffffff?text=Migraña:+Migranol+alivio+rápido",
        "msg":"Migraña muy fuerte — Migranol es la solución. ¡Cómpralo ahora!"
    },
    {
        "img":"https://placehold.co/1200x300/f97316/ffffff?text=Fiebre+y+Dolor:+Paracetamol",
        "msg":"Fiebre y dolor: paracetamol para aliviarte rápido."
    },
    {
        "img":"https://placehold.co/1200x300/16a34a/ffffff?text=Antibióticos:+Amoxicilina",
        "msg":"Infecciones bacterianas: Amoxicilina confiable."
    },
    {
        "img":"https://placehold.co/1200x300/7c3aed/ffffff?text=Vitaminas:+Energía+diaria",
        "msg":"Vitaminas y suplementos: recarga tu energía con vitamina C."
    },
    {
        "img":"https://placehold.co/1200x300/ef4444/ffffff?text=Pediátricos:+Cuidado+seguro",
        "msg":"Pediátricos: fórmulas seguras para los más pequeños."
    },
]

def render_banner():
    if "banner_idx" not in st.session_state:
        st.session_state["banner_idx"] = 0

    idx = st.session_state["banner_idx"] % len(BANNERS)
    banner = BANNERS[idx]

    left, middle, right = st.columns([1, 10, 1])
    with left:
        if st.button("◀", key="banner_prev"):
            st.session_state["banner_idx"] = (st.session_state["banner_idx"] - 1) % len(BANNERS)
            st.experimental_rerun()
    with middle:
        st.image(banner["img"], use_column_width=True)
        st.markdown(f"<div style='text-align:center; font-weight:600'>{banner['msg']}</div>", unsafe_allow_html=True)
    with right:
        if st.button("▶", key="banner_next"):
            st.session_state["banner_idx"] = (st.session_state["banner_idx"] + 1) % len(BANNERS)
            st.experimental_rerun()


