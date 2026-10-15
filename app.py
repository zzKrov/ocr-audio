import streamlit as st
import streamlit.components.v1 as components
import os
import time
import glob
import html
import cv2
import numpy as np
import pytesseract
from gtts import gTTS
from googletrans import Translator

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="Espejo Mágico // Krov Industries",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

os.makedirs("temp", exist_ok=True)

# ============================================================
# ESTILOS VISUALES
# ============================================================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 50% 20%, #150a26 0%, #080312 60%, #030107 100%);
    color: #eee7dc;
    font-family: Georgia, serif;
}

.brand-signature {
    text-align: center;
    font-family: Georgia, serif;
    font-size: 0.75rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #c084fc;
    margin-bottom: 4px;
}

h1 {
    text-align: center;
    font-size: clamp(2.3rem, 5vw, 4rem) !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em;
    color: #eee7dc !important;
    text-shadow: 0 0 10px rgba(230,215,255,0.4);
}

.stButton > button {
    width: 100%;
    min-height: 50px;
    border-radius: 4px;
    border: 1px solid rgba(180,145,225,0.60);
    background: linear-gradient(120deg, #26163a, #0e0916, #321a4b);
    color: #f0e9df;
    font-family: Georgia, serif;
    letter-spacing: 0.08em;
    font-size: 0.95rem;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(170,120,245,0.40);
    border-color: rgba(230,210,250,0.90);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="brand-signature">Krov Industries · Reconocimiento Óptico y Mágico</div>', unsafe_allow_html=True)
st.title("Espejo Mágico")
st.markdown("<p style='text-align:center; color:#ddd5c9; letter-spacing:0.08em; margin-bottom:1.5rem;'>Extracción de texto en imágenes, traducción oral y espejo reflectivo interactivo</p>", unsafe_allow_html=True)

# ------------------------------------------------------------
# FUENTE DE ENTRADA CON PERSISTENCIA
# ------------------------------------------------------------
col_cam, col_up = st.columns(2, gap="medium")
uploaded_bytes = None

with col_cam:
    with st.container(border=True):
        st.markdown("### Captura por Cámara")
        use_camera = st.checkbox("Activar visor de cámara", key="use_camera_box")
        cam_shot = st.camera_input("Capturar foto", label_visibility="collapsed") if use_camera else None
        if cam_shot:
            uploaded_bytes = cam_shot.getvalue()
            st.session_state["stored_mirror_image"] = uploaded_bytes

with col_up:
    with st.container(border=True):
        st.markdown("### Carga de Archivo")
        file_up = st.file_uploader("Seleccionar imagen (.png, .jpg, .jpeg):", type=["png", "jpg", "jpeg"])
        if file_up:
            uploaded_bytes = file_up.getvalue()
            st.session_state["stored_mirror_image"] = uploaded_bytes

active_image_bytes = uploaded_bytes or st.session_state.get("stored_mirror_image", None)

with st.sidebar:
    st.header("Parámetros de Imagen")
    invert_filter = st.radio("Invertir contraste (negativo):", ("No", "Sí"))
    
    st.header("Configuración de Traducción")
    languages = {
        "Español": "es", "Inglés": "en", "Bengalí": "bn", "Coreano": "ko",
        "Mandarín": "zh-cn", "Japonés": "ja", "Ruso": "ru", "Alemán": "de"
    }
    in_lang = st.selectbox("Idioma detectado:", list(languages.keys()), index=0)
    out_lang = st.selectbox("Idioma de destino:", list(languages.keys()), index=1)
    accents = {
        "Predeterminado": "com", "España / México": "com.mx", "Reino Unido": "co.uk", "Estados Unidos": "com"
    }
    accent = st.selectbox("Acento de audio:", list(accents.keys()), index=0)

# ------------------------------------------------------------
# PROCESAMIENTO OCR ROBUSTO
# ------------------------------------------------------------
extracted_text = ""

if active_image_bytes:
    img_cv = cv2.imdecode(np.frombuffer(active_image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img_cv is not None:
        if invert_filter == "Sí":
            img_cv = cv2.bitwise_not(img_cv)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        try:
            extracted_text = pytesseract.image_to_string(gray).strip()
        except Exception:
            try:
                extracted_text = pytesseract.image_to_string(img_cv).strip()
            except Exception:
                extracted_text = ""

if extracted_text:
    st.session_state["stored_ocr_text"] = extracted_text

persisted_text = st.session_state.get("stored_ocr_text", "")

# ------------------------------------------------------------
# RESTAURACIÓN DEL ESPEJO MÁGICO 3D CON PARTÍCULAS
# ------------------------------------------------------------
mirror_display = html.escape(persisted_text) if persisted_text else "Introduce una imagen con texto para despertar el espejo."
mirror_badge = "MENSAJE DESCIFRADO" if persisted_text else "ESPEJO EN REPOSO"

mirror_component_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{
    margin: 0; padding: 0; width: 100%; height: 100%;
    overflow: hidden; background: transparent; font-family: Georgia, serif;
}}
.magic-mirror {{
    position: relative; width: 100%; height: 460px;
    overflow: hidden; border-radius: 16px;
    background: radial-gradient(ellipse at 50% 50%, rgba(95,60,150,0.35), rgba(12,8,22,0.98) 70%);
    border: 1px solid rgba(195,170,235,0.45);
    box-shadow: 0 0 20px rgba(145,95,225,0.35), inset 0 0 90px rgba(100,65,160,0.3);
    transition: transform 0.15s ease-out;
}}
.bloom {{
    position: absolute; width: 70%; height: 70%; left: 15%; top: 15%;
    border-radius: 50%;
    background: radial-gradient(ellipse, rgba(210,190,255,0.16), transparent 70%);
    filter: blur(25px); pointer-events: none;
}}
.scan-beam {{
    position: absolute; left: 4%; right: 4%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(230,215,255,0.9), transparent);
    box-shadow: 0 0 12px rgba(210,185,255,0.95);
    animation: scan 4s linear infinite; pointer-events: none;
}}
@keyframes scan {{
    0% {{ top: 10%; opacity: 0; }}
    15% {{ opacity: 0.85; }}
    85% {{ opacity: 0.85; }}
    100% {{ top: 90%; opacity: 0; }}
}}
.particles {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
.particle {{
    position: absolute; width: 2px; height: 2px; border-radius: 50%;
    background: rgba(225,215,255,0.85); box-shadow: 0 0 6px rgba(190,160,255,0.8);
    animation: floatUp 8s ease-in-out infinite;
}}
@keyframes floatUp {{
    0% {{ transform: translateY(40px) scale(0.2); opacity: 0; }}
    20% {{ opacity: 0.8; }}
    80% {{ opacity: 0.8; }}
    100% {{ transform: translateY(-380px) scale(1); opacity: 0; }}
}}
.content {{
    position: absolute; inset: 0; z-index: 10;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 30px; text-align: center;
}}
.badge {{
    font-size: 0.75rem; letter-spacing: 0.3em; color: rgba(210,195,230,0.7);
    margin-bottom: 16px; text-transform: uppercase;
}}
.msg {{
    max-width: 820px; max-height: 280px; overflow-y: auto;
    font-size: clamp(1.2rem, 2.5vw, 2.1rem); line-height: 1.5; color: #eee8f5;
    text-shadow: 0 0 8px rgba(230,215,255,0.5), 0 0 25px rgba(150,105,230,0.4);
}}
</style>
</head>
<body>
<div class="magic-mirror" id="mirror">
    <div class="bloom"></div>
    <div class="scan-beam"></div>
    <div class="particles" id="particle-box"></div>
    <div class="content">
        <div class="badge">{mirror_badge}</div>
        <div class="msg">{mirror_display}</div>
    </div>
</div>
<script>
const pBox = document.getElementById('particle-box');
for(let i=0; i<45; i++) {{
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.left = (Math.random() * 100) + '%';
    p.style.bottom = (Math.random() * 40) + '%';
    p.style.animationDelay = (Math.random() * -8) + 's';
    p.style.animationDuration = (5 + Math.random() * 6) + 's';
    pBox.appendChild(p);
}}
const m = document.getElementById('mirror');
m.addEventListener('mousemove', (e) => {{
    const rect = m.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    m.style.transform = `perspective(800px) rotateY(${{x * 8}}deg) rotateX(${{-y * 8}}deg)`;
}});
m.addEventListener('mouseleave', () => {{
    m.style.transform = 'perspective(800px) rotateY(0deg) rotateX(0deg)';
}});
</script>
</body>
</html>
"""

components.html(mirror_component_html, height=480, scrolling=False)

# Si el OCR no detectó nada pero hay imagen, ofrecer campo de verificación
if active_image_bytes and not persisted_text:
    st.info("La imagen fue recibida pero el contraste no permitió extraer texto automáticamente. Puedes escribirlo directamente para traducirlo:")
    persisted_text = st.text_input("Ingresar texto de la imagen manualmente:", value="")

if persisted_text:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Palabras identificadas", len(persisted_text.split()))
    with col_m2:
        st.metric("Caracteres legibles", len(persisted_text))

st.write("")
translate_btn = st.button("Descifrar y traducir texto", use_container_width=True)

if translate_btn:
    if not persisted_text.strip():
        st.warning("Primero debes capturar o subir una imagen que contenga texto legible.")
    else:
        try:
            translator = Translator()
            in_code = languages[in_lang]
            out_code = languages[out_lang]
            tld = accents[accent]

            translation = translator.translate(persisted_text, src=in_code, dest=out_code)
            trans_res = translation.text

            st.markdown(f"### Traducción ({out_lang}):")
            st.markdown(f"<div style='font-size:1.3rem; color:#f3e8ff;'>«{trans_res}»</div>", unsafe_allow_html=True)

            tts = gTTS(trans_res, lang=out_code, tld=tld, slow=False)
            fp = f"temp/mirror_audio_{int(time.time())}.mp3"
            tts.save(fp)

            with open(fp, "rb") as af:
                st.audio(af.read(), format="audio/mp3")

        except Exception as e:
            st.error(f"Error en la traducción o síntesis: {e}")
