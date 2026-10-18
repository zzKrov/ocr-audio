import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="Reconocimiento Óptico // Krov Industries",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LÍNEA BASE VISUAL: GRADIENTES NEÓN Y FLUIDOS DE ALTO CONTRASTE
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #05020a !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    overflow-x: hidden;
}

[data-testid="stHeader"] { background: transparent !important; }

/* 1. Fondo de gradiente continuo animado */
.stApp {
    background: linear-gradient(135deg, #05020a 0%, #150320 30%, #200418 60%, #070312 100%) !important;
    background-size: 300% 300% !important;
    animation: crimsonShift 18s ease infinite alternate !important;
}

@keyframes crimsonShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 2. Esferas orgánicas fluidas de luz */
.fluid-glow-1 {
    position: fixed;
    top: 15%;
    left: -120px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(255, 23, 79, 0.14) 0%, rgba(155, 66, 255, 0.04) 55%, transparent 70%);
    border-radius: 40% 60% 70% 30% / 50% 60% 40% 50%;
    filter: blur(80px);
    animation: fluidDrift1 20s infinite alternate ease-in-out;
    pointer-events: none;
    z-index: 0;
}

.fluid-glow-2 {
    position: fixed;
    bottom: 5%;
    right: -100px;
    width: 550px;
    height: 550px;
    background: radial-gradient(circle, rgba(155, 66, 255, 0.12) 0%, rgba(255, 23, 79, 0.03) 55%, transparent 70%);
    border-radius: 60% 40% 50% 50% / 40% 50% 60% 50%;
    filter: blur(85px);
    animation: fluidDrift2 24s infinite alternate ease-in-out;
    pointer-events: none;
    z-index: 0;
}

@keyframes fluidDrift1 {
    0% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(120px, 60px) scale(1.15); }
    100% { transform: translate(30px, 130px) scale(0.95); }
}

@keyframes fluidDrift2 {
    0% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(-100px, -70px) scale(1.2); }
    100% { transform: translate(-20px, -110px) scale(0.92); }
}

.brand-signature {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    color: #ff174f;
    text-transform: uppercase;
    margin-bottom: 2px;
}

.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
    color: #ffffff;
    margin-bottom: 0.2rem;
    text-shadow: 0 0 25px rgba(255, 23, 79, 0.4);
}

.sub-lead {
    text-align: center;
    color: #cbd5e1;
    font-size: 0.95rem;
    margin-bottom: 1.8rem;
}

/* Visor de cámara acotado */
[data-testid="stCameraInput"] {
    max-width: 500px;
    margin: 0 auto;
}
[data-testid="stCameraInput"] video {
    max-height: 290px !important;
    border-radius: 8px !important;
    object-fit: cover !important;
    border: 1px solid rgba(255, 23, 79, 0.35) !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.8) !important;
}

/* Tarjeta de resultado */
.result-card {
    background: rgba(18, 5, 24, 0.85);
    border: 1px solid rgba(255, 23, 79, 0.25);
    border-left: 4px solid #ff174f;
    border-radius: 8px;
    padding: 1.4rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.6);
    min-height: 180px;
    font-family: 'Spectral', Georgia, serif;
    font-size: 1.15rem;
    line-height: 1.6;
    color: #f8fafc;
}

.stat-tile {
    background: rgba(18, 5, 24, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 2px solid #ff174f;
    border-radius: 6px;
    padding: 12px;
    text-align: center;
    backdrop-filter: blur(10px);
}
.stat-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
}
.stat-lbl {
    font-size: 0.72rem;
    color: #94a3b8;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
}
</style>

<div class="fluid-glow-1"></div>
<div class="fluid-glow-2"></div>
""", unsafe_allow_html=True)

# ============================================================
# ENCABEZADO
# ============================================================
st.markdown('<div class="brand-signature">Krov Industries · Reconocimiento Óptico</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Reconocimiento Óptico de Caracteres</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-lead">Captura óptica en tiempo real, preprocesamiento y extracción de texto</div>', unsafe_allow_html=True)

col_capture, col_result = st.columns([1, 1.2], gap="large")

with col_capture:
    st.markdown("### 1. Entrada de cámara")
    img_file_buffer = st.camera_input("Capturar fotografía", label_visibility="collapsed")
    
    filtro = st.radio(
        "Filtro de preprocesamiento:",
        ("Sin Filtro", "Con Filtro (Inversión de contraste)"),
        horizontal=True
    )

with col_result:
    st.markdown("### 2. Texto reconocido")
    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        if "Con Filtro" in filtro:
            cv2_img = cv2.bitwise_not(cv2_img)

        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        
        with st.spinner("Procesando caracteres con Tesseract OCR..."):
            try:
                text = pytesseract.image_to_string(img_rgb)
            except Exception:
                text = ""

        clean_text = text.strip()
        word_count = len(clean_text.split()) if clean_text else 0
        char_count = len(clean_text)

        if clean_text:
            st.markdown(f'<div class="result-card">{clean_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="result-card" style="color:#94a3b8; font-style:italic;">'
                'No se identificaron caracteres legibles. Asegúrate de enfocar con nitidez y buena iluminación.'
                '</div>',
                unsafe_allow_html=True
            )

        st.write("")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(f'<div class="stat-tile"><div class="stat-num">{word_count}</div><div class="stat-lbl">Palabras</div></div>', unsafe_allow_html=True)
        with s2:
            st.markdown(f'<div class="stat-tile"><div class="stat-num">{char_count}</div><div class="stat-lbl">Caracteres</div></div>', unsafe_allow_html=True)
        with s3:
            modo = "Filtrado" if "Con Filtro" in filtro else "Original"
            st.markdown(f'<div class="stat-tile"><div class="stat-num">{modo}</div><div class="stat-lbl">Modo</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="result-card" style="display:flex; justify-content:center; align-items:center; text-align:center; color:#94a3b8;">'
            'Toma una fotografía con la cámara para extraer el texto automáticamente.'
            '</div>',
            unsafe_allow_html=True
        )
