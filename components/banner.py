import streamlit as st
from pathlib import Path
from PIL import Image
import time

def _get_banner_paths(asset_folder: str):
    """Busca imágenes dentro de la carpeta de banners."""
    p = Path(asset_folder)
    if not p.exists():
        return []
    return sorted([str(x) for x in p.iterdir() if x.suffix.lower() in [".jpg", ".jpeg", ".png"]])

def show_banner(asset_folder="assets/banners", autoplay=True, interval=5):
    """Muestra un carrusel de banners con autoplay y botones centrados."""
    st.markdown(
        """
<style>
.banner-wrapper {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}
.banner-img {
    max-width: 80%;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.banner-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background-color: rgba(255,255,255,0.8);
    border: none;
    font-size: 26px;
    font-weight: bold;
    padding: 10px 16px;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
}
.banner-btn:hover {
    background-color: #ff4b4b;
    color: white;
    transform: translateY(-50%) scale(1.1);
}
.banner-btn.left {
    left: 5%;
}
.banner-btn.right {
    right: 5%;
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

    # Contenedor del banner
    st.markdown('<div class="banner-wrapper">', unsafe_allow_html=True)
    img_path = paths[st.session_state.banner_index]
    try:
        img = Image.open(img_path)
        st.image(img, use_container_width=True)
    except Exception:
        st.image(img_path, use_container_width=True)

    # Botones de navegación
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("◀", key="banner_prev"):
            st.session_state.banner_index = (st.session_state.banner_index - 1) % len(paths)
            st.rerun()
    with col2:
        if st.button("▶", key="banner_next"):
            st.session_state.banner_index = (st.session_state.banner_index + 1) % len(paths)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # --- Autoplay ---
    if autoplay:
        if "last_autoplay" not in st.session_state:
            st.session_state.last_autoplay = time.time()
        if time.time() - st.session_state.last_autoplay > interval:
            st.session_state.banner_index = (st.session_state.banner_index + 1) % len(paths)
            st.session_state.last_autoplay = time.time()
            st.rerun()
