import streamlit as st

banners = [
    {"img": "https://placehold.co/1200x300?text=Analgésicos", "msg": "Migraña muy fuerte, migranol es la solución."},
    {"img": "https://placehold.co/1200x300?text=Antibióticos", "msg": "Combate infecciones bacterianas con Amoxicilina."},
    {"img": "https://placehold.co/1200x300?text=Antivirales", "msg": "Defiéndete de los virus con Aciclovir."},
    {"img": "https://placehold.co/1200x300?text=Vitaminas", "msg": "Refuerza tu sistema inmune con Vitamina C."},
    {"img": "https://placehold.co/1200x300?text=Cardiovasculares", "msg": "Cuida tu corazón con Atorvastatina."},
]

def show_banner():
    if "banner_index" not in st.session_state:
        st.session_state.banner_index = 0

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if st.button("⬅️"):
            st.session_state.banner_index = (st.session_state.banner_index - 1) % len(banners)

    with col2:
        banner = banners[st.session_state.banner_index]
        st.image(banner["img"], use_column_width=True)
        st.markdown(f"<h4 style='text-align:center'>{banner['msg']}</h4>", unsafe_allow_html=True)

    with col3:
        if st.button("➡️"):
            st.session_state.banner_index = (st.session_state.banner_index + 1) % len(banners)
