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

def remove_files(days):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    for file in mp3_files:
        if os.stat(file).st_mtime < now - (days * 86400):
            try:
                os.remove(file)
            except Exception:
                pass

remove_files(7)

# ============================================================
# TRADUCCIÓN Y SÍNTESIS DE AUDIO
# ============================================================
def text_to_speech(input_language, output_language, text, tld):
    translator = Translator()
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text

    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)

    filename = text[:20]
    filename = "".join(c for c in filename if c.isalnum() or c in (" ", "_", "-")).strip()
    if not filename:
        filename = "audio"

    filename = filename.replace("/", "_").replace("\\", "_")
    filepath = f"temp/{filename}.mp3"
    tts.save(filepath)

    return filename, trans_text

# ============================================================
# ESTILOS VISUALES GÓTICOS
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(90, 45, 170, 0.22), transparent 30%),
            radial-gradient(circle at 85% 25%, rgba(40, 90, 180, 0.18), transparent 30%),
            linear-gradient(125deg, #030207, #0a0613, #050914, #030207);
        color: #eee7dc;
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
        font-family: Georgia, serif !important;
        font-size: clamp(2.5rem, 5vw, 4.5rem) !important;
        font-weight: 500 !important;
        letter-spacing: 0.12em;
        color: #eee7dc !important;
        text-shadow: 0 0 10px rgba(230,215,255,0.5), 0 0 30px rgba(150,100,240,0.3);
    }

    .stButton > button {
        width: 100%;
        min-height: 52px;
        border-radius: 4px;
        border: 1px solid rgba(180,145,225,0.60);
        background: linear-gradient(120deg, #26163a, #0e0916, #321a4b);
        color: #f0e9df;
        font-family: Georgia, serif;
        letter-spacing: 0.1em;
        font-size: 0.95rem;
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(230,210,250,0.90);
        box-shadow: 0 0 25px rgba(170,120,245,0.40);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="brand-signature">Krov Industries · Reconocimiento Óptico y Mágico</div>', unsafe_allow_html=True)
st.title("Espejo Mágico")
st.markdown("<p style='text-align:center; color:#ddd5c9; letter-spacing:0.1em; margin-bottom:1.5rem;'>Reconocimiento de texto en imágenes y traducción oral inmediata</p>", unsafe_allow_html=True)

with st.expander("Instrucciones de uso", expanded=False):
    st.write(
        "1. Toma una fotografía con la cámara o carga una imagen desde tu equipo.\n"
        "2. El sistema extraerá el texto mediante reconocimiento óptico de caracteres.\n"
        "3. Selecciona el idioma de origen, el de destino y la modulación vocal en la barra lateral.\n"
        "4. Presiona el botón para descifrar, traducir y reproducir la traducción en audio."
    )

st.subheader("Fuente de imagen")
camera_col, upload_col = st.columns(2)

with camera_col:
    with st.container(border=True):
        st.markdown("### Cámara en vivo")
        st.write("Fotografía un documento o texto físico.")
        use_camera = st.checkbox("Activar visor de cámara", key="camera")
        img_file_buffer = st.camera_input("Capturar fotografía") if use_camera else None

with upload_col:
    with st.container(border=True):
        st.markdown("### Archivo local")
        st.write("Carga una imagen en formato digital.")
        bg_image = st.file_uploader("Seleccionar imagen del equipo", type=["png", "jpg", "jpeg"], key="upload")

with st.sidebar:
    st.header("Procesamiento de imagen")
    filtro = st.radio("Invertir contraste (filtro negativo):", ("No", "Sí"))

text = ""

if bg_image is not None:
    img_bytes = bg_image.getvalue()
    img_cv = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img_cv is not None:
        if filtro == "Sí":
            img_cv = cv2.bitwise_not(img_cv)
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)

elif img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    if cv2_img is not None:
        if filtro == "Sí":
            cv2_img = cv2.bitwise_not(cv2_img)
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)

if text.strip():
    mirror_text = html.escape(text.strip())
    mirror_label = "Texto Reconocido"
else:
    mirror_text = "Carga o fotografía un documento para comenzar el análisis."
    mirror_label = "En Espera de Imagen"

mirror_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{
    margin: 0; padding: 0; width: 100%; height: 100%;
    overflow: hidden; background: transparent;
    font-family: Georgia, serif;
}}
.magic-mirror {{
    position: relative; width: 100%; height: 500px;
    overflow: hidden; border-radius: 16px;
    background: radial-gradient(ellipse at 50% 50%, rgba(95,60,150,0.34), rgba(12,8,22,0.98) 67%);
    border: 1px solid rgba(195,170,235,0.45);
    box-shadow: 0 0 20px rgba(145,95,225,0.35), inset 0 0 90px rgba(100,65,160,0.30);
}}
.mirror-content {{
    position: absolute; inset: 0; z-index: 10;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 40px; text-align: center;
}}
.mirror-label {{
    margin-bottom: 20px; font-size: 0.8rem; letter-spacing: 0.3em;
    color: rgba(210,195,230,0.7); text-transform: uppercase;
}}
.mirror-message {{
    max-width: 850px; max-height: 320px; overflow: auto;
    font-size: clamp(1.2rem, 2.5vw, 2.2rem); line-height: 1.5; color: #eee8f5;
    text-shadow: 0 0 8px rgba(230,215,255,0.55), 0 0 25px rgba(150,105,230,0.45);
}}
</style>
</head>
<body>
<div class="magic-mirror">
    <div class="mirror-content">
        <div class="mirror-label">{html.escape(mirror_label)}</div>
        <div class="mirror-message">{mirror_text}</div>
    </div>
</div>
</body>
</html>
"""

components.html(mirror_html, height=520, scrolling=False)

if text.strip():
    st.markdown("### Métricas del texto extraído")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de palabras", len(text.split()))
    with col2:
        st.metric("Total de caracteres", len(text.strip()))
    with col3:
        st.metric("Estado OCR", "Lectura correcta")

with st.sidebar:
    st.header("Configuración de traducción")
    languages = {
        "Español": "es", "Inglés": "en", "Bengalí": "bn", "Coreano": "ko",
        "Mandarín": "zh-cn", "Japonés": "ja", "Ruso": "ru", "Alemán": "de"
    }
    in_lang = st.selectbox("Idioma detectado:", list(languages.keys()), index=0)
    input_language = languages[in_lang]

    out_lang = st.selectbox("Idioma a traducir:", list(languages.keys()), index=1)
    output_language = languages[out_lang]

    accents = {
        "Predeterminado": "com", "España / México": "com.mx", "Reino Unido": "co.uk",
        "Estados Unidos": "com", "Canadá": "ca", "Australia": "com.au"
    }
    accent = st.selectbox("Acento de voz:", list(accents.keys()), index=0)
    tld = accents[accent]

st.markdown("---")

translate_button = st.button("Descifrar y traducir texto", use_container_width=True)

if translate_button:
    if not text.strip():
        st.warning("Primero debes capturar o subir una imagen que contenga texto legible.")
    else:
        try:
            result_name, output_text = text_to_speech(input_language, output_language, text, tld)
            st.subheader("Mensaje descifrado y traducido:")

            output_placeholder = st.empty()
            current_text = ""
            for character in output_text:
                current_text += character
                output_placeholder.markdown(f"### {html.escape(current_text)}")
                time.sleep(0.015)

            st.success("Traducción completada con éxito.")
            st.subheader("Traducción en audio:")

            with open(f"temp/{result_name}.mp3", "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")

        except Exception as e:
            st.error(f"No fue posible completar la traducción: {e}")
