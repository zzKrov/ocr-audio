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
# ESTILOS VISUALES: TERCIOPELO MÍSTICO, LÁMPARA DE LAVA GPU Y RESPLANDOR
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,500;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #06030b !important;
    color: #eee7dc !important;
    font-family: 'Spectral', Georgia, serif !important;
    overflow-x: hidden;
}

[data-testid="stHeader"] { background: transparent !important; }

/* Fondo líquido de terciopelo y amatista acelerado por GPU */
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(192, 132, 252, 0.16) 0%, transparent 40%),
        radial-gradient(circle at 85% 30%, rgba(147, 51, 234, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 50% 85%, rgba(95, 60, 150, 0.18) 0%, transparent 50%),
        linear-gradient(135deg, #06030b 0%, #120622 50%, #06030b 100%) !important;
    background-size: 200% 200% !important;
    animation: velvetLava 15s ease infinite alternate !important;
}

@keyframes velvetLava {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 100%; }
}

.brand-signature {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c084fc;
    margin-bottom: 2px;
}

.main-title {
    font-size: 2.3rem;
    font-weight: 700;
    text-align: center;
    color: #ffffff;
    margin-bottom: 0.2rem;
    text-shadow: 0 0 25px rgba(192, 132, 252, 0.45);
}

.sub-lead {
    text-align: center;
    color: #cbd5e1;
    font-size: 0.95rem;
    margin-bottom: 1.6rem;
}

.card-frame {
    background: rgba(18, 9, 32, 0.85);
    border: 1px solid rgba(192, 132, 252, 0.3);
    border-radius: 8px;
    padding: 18px;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    margin-bottom: 14px;
}

div.stButton > button {
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    background: linear-gradient(135deg, #7c3aed 0%, #c084fc 100%) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 0.8rem 1.6rem !important;
    box-shadow: 0 0 20px rgba(192, 132, 252, 0.35) !important;
    transition: all 0.25s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 35px rgba(192, 132, 252, 0.65) !important;
}

.trans-result-card {
    background: rgba(18, 9, 32, 0.88);
    border-left: 4px solid #c084fc;
    border-radius: 6px;
    padding: 16px 20px;
    margin: 14px 0;
    font-size: 1.15rem;
    color: #f8fafc;
    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="brand-signature">Krov Industries · Óptica y Traducción</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Espejo Mágico de Lectura</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-lead">Extracción de texto en imágenes, traducción inmediata y síntesis de voz</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# FUENTE DE ENTRADA CON PERSISTENCIA EN SESIÓN
# ------------------------------------------------------------
col_cam, col_up = st.columns(2, gap="medium")
uploaded_bytes = None

with col_cam:
    st.markdown('<div class="card-frame">', unsafe_allow_html=True)
    st.markdown("#### 1. Captura por cámara")
    use_camera = st.checkbox("Activar visor de cámara", key="use_camera_box")
    cam_shot = st.camera_input("Capturar", label_visibility="collapsed") if use_camera else None
    if cam_shot:
        uploaded_bytes = cam_shot.getvalue()
        st.session_state["stored_mirror_image"] = uploaded_bytes
    st.markdown('</div>', unsafe_allow_html=True)

with col_up:
    st.markdown('<div class="card-frame">', unsafe_allow_html=True)
    st.markdown("#### 2. Carga de archivo")
    file_up = st.file_uploader("Selecciona imagen (.png, .jpg, .jpeg):", type=["png", "jpg", "jpeg"])
    if file_up:
        uploaded_bytes = file_up.getvalue()
        st.session_state["stored_mirror_image"] = uploaded_bytes
    st.markdown('</div>', unsafe_allow_html=True)

active_image_bytes = uploaded_bytes or st.session_state.get("stored_mirror_image", None)

with st.sidebar:
    st.markdown("### Configuración de Imagen")
    invert_filter = st.radio("Inversión de contraste:", ("No", "Sí"))
    
    st.markdown("---")
    st.markdown("### Configuración de Idiomas")
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
# PIPELINE OCR MEJORADO CON FILTRADO BILATERAL Y CLAHE
# ------------------------------------------------------------
extracted_text = ""

if active_image_bytes:
    img_cv = cv2.imdecode(np.frombuffer(active_image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img_cv is not None:
        if invert_filter == "Sí":
            img_cv = cv2.bitwise_not(img_cv)
        
        # 1. Escala de grises
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # 2. Filtrado bilateral para eliminar ruido conservando bordes de letras
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # 3. Realce adaptativo de contraste (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        try:
            extracted_text = pytesseract.image_to_string(enhanced, config='--psm 3').strip()
            if not extracted_text:
                extracted_text = pytesseract.image_to_string(enhanced, config='--psm 6').strip()
        except Exception:
            try:
                extracted_text = pytesseract.image_to_string(gray).strip()
            except Exception:
                extracted_text = ""

if extracted_text:
    st.session_state["stored_ocr_text"] = extracted_text

persisted_text = st.session_state.get("stored_ocr_text", "")

# ------------------------------------------------------------
# COMPONENTE DEL ESPEJO MÁGICO 3D INTERACTIVO
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
    overflow: hidden; background: transparent; font-family: 'Spectral', Georgia, serif;
}}
.magic-mirror {{
    position: relative; width: 100%; height: 420px;
    overflow: hidden; border-radius: 16px;
    background: radial-gradient(ellipse at 50% 50%, rgba(95,60,150,0.38), rgba(12,8,22,0.98) 70%);
    border: 1px solid rgba(192,132,252,0.45);
    box-shadow: 0 0 25px rgba(192,132,252,0.35), inset 0 0 90px rgba(100,65,160,0.35);
    transition: transform 0.15s ease-out;
}}
.bloom {{
    position: absolute; width: 70%; height: 70%; left: 15%; top: 15%;
    border-radius: 50%;
    background: radial-gradient(ellipse, rgba(210,190,255,0.18), transparent 70%);
    filter: blur(25px); pointer-events: none;
}}
.scan-beam {{
    position: absolute; left: 4%; right: 4%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(230,215,255,0.95), transparent);
    box-shadow: 0 0 12px rgba(210,185,255,0.95);
    animation: scan 4s linear infinite; pointer-events: none;
}}
@keyframes scan {{
    0% {{ top: 10%; opacity: 0; }}
    15% {{ opacity: 0.9; }}
    85% {{ opacity: 0.9; }}
    100% {{ top: 90%; opacity: 0; }}
}}
.particles {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
.particle {{
    position: absolute; width: 2.5px; height: 2.5px; border-radius: 50%;
    background: rgba(225,215,255,0.85); box-shadow: 0 0 6px rgba(190,160,255,0.8);
    animation: floatUp 8s ease-in-out infinite;
}}
@keyframes floatUp {{
    0% {{ transform: translateY(40px) scale(0.2); opacity: 0; }}
    20% {{ opacity: 0.85; }}
    80% {{ opacity: 0.85; }}
    100% {{ transform: translateY(-360px) scale(1); opacity: 0; }}
}}
.content {{
    position: absolute; inset: 0; z-index: 10;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 30px; text-align: center;
}}
.badge {{
    font-size: 0.75rem; letter-spacing: 0.3em; color: rgba(210,195,230,0.75);
    margin-bottom: 14px; text-transform: uppercase; font-family: monospace;
}}
.msg {{
    max-width: 820px; max-height: 250px; overflow-y: auto;
    font-size: clamp(1.2rem, 2.5vw, 2rem); line-height: 1.5; color: #eee8f5;
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
for(let i=0; i<60; i++) {{
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

components.html(mirror_component_html, height=440, scrolling=False)

if active_image_bytes and not persisted_text:
    st.info("La imagen fue cargada pero el texto no pudo ser extraído automáticamente. Puedes introducirlo manualmente para traducir:")
    persisted_text = st.text_input("Ingresar texto detectado manualmente:", value="")

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
        with st.spinner("Traduciendo y generando síntesis oral..."):
            try:
                translator = Translator()
                in_code = languages[in_lang]
                out_code = languages[out_lang]
                tld = accents[accent]

                translation = translator.translate(persisted_text, src=in_code, dest=out_code)
                trans_res = translation.text

                st.markdown(f'<div class="trans-result-card"><b>Traducción ({out_lang}):</b><br>«{trans_res}»</div>', unsafe_allow_html=True)

                tts = gTTS(trans_res, lang=out_code, tld=tld, slow=False)
                audio_file = f"temp/mirror_audio_{int(time.time())}.mp3"
                tts.save(audio_file)

                with open(audio_file, "rb") as af:
                    st.audio(af.read(), format="audio/mp3")

            except Exception as e:
                st.error(f"Error en la traducción o síntesis: {e}")

# Limpieza periódica de audios antiguos
def limpiar_archivos_antiguos(days=7):
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < time.time() - (days * 86400):
            try:
                os.remove(f)
            except Exception:
                pass

limpiar_archivos_antiguos()
