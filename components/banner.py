import streamlit as st
from pathlib import Path
from PIL import Image

def _get_banner_paths(asset_folder: str):
    """Busca imágenes dentro de la carpeta de banners."""
    p = Path(asset_folder)
    if not p.exists():
        return []
    return sorted([str(x) for x in p.iterdir() if x.suffix.lower() in [".jpg", ".jpeg", ".png"]])

def show_banner(asset_folder="assets/banners"):
    """Muestra un carrusel de banners con botones de navegación."""
    st.markdown(
        """
        <style>
        .banner-img {
            border-radius: 5px;
            margin-bottom: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    paths = _get_banner_paths(asset_folder)
    if not paths:
        st.warning("⚠️ No hay imágenes en la carpeta de banners")
        return

    if "banner_index" not in st.session_state:
        st.session_state.banner_index = 0

    cols = st.columns([1, 6, 1])
    with cols[0]:
        if st.button("◀", key="banner_prev"):
            st.session_state.banner_index = (st.session_state.banner_index - 1) % len(paths)

    with cols[2]:
        if st.button("▶", key="banner_next"):
            st.session_state.banner_index = (st.session_state.banner_index + 1) % len(paths)

    idx = st.session_state.banner_index
    img_path = paths[idx]

    try:
        img = Image.open(img_path)
        st.image(img, use_container_width=True)  
    except Exception:
        st.image(img_path, use_container_width=True)
