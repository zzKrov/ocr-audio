import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from gtts import gTTS
from googletrans import Translator


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Espejo Mágico",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CARPETA DE AUDIO
# ============================================================

os.makedirs("temp", exist_ok=True)


# ============================================================
# LIMPIEZA
# ============================================================

def remove_files(days):

    files = glob.glob("temp/*.mp3")

    now = time.time()

    for file in files:

        if os.stat(file).st_mtime < now - (days * 86400):

            os.remove(file)


remove_files(7)


# ============================================================
# TRADUCCIÓN + TTS
# ============================================================

def text_to_speech(
    input_language,
    output_language,
    text,
    tld
):

    translator = Translator()

    translation = translator.translate(
        text,
        src=input_language,
        dest=output_language
    )

    translated_text = translation.text

    tts = gTTS(
        translated_text,
        lang=output_language,
        tld=tld,
        slow=False
    )

    filename = "".join(
        c for c in text[:20]
        if c.isalnum() or c in (" ", "_", "-")
    ).strip()

    if not filename:
        filename = "audio"

    path = f"temp/{filename}.mp3"

    tts.save(path)

    return filename, translated_text


# ============================================================
# ESTILO
#
# IMPORTANTE:
# Aquí NO se utiliza HTML visible.
# Solo se inyecta CSS para modificar componentes nativos
# de Streamlit.
# ============================================================

st.markdown(
"""
<style>

/* ==========================================================
   FONDO
   ========================================================== */

.stApp {

    background:
        radial-gradient(
            circle at 50% 15%,
            rgba(93, 63, 150, 0.25),
            transparent 25%
        ),
        radial-gradient(
            circle at 15% 60%,
            rgba(40, 80, 125, 0.16),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 70%,
            rgba(115, 45, 105, 0.15),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #05040a,
            #0a0711,
            #040308
        );

}


/* ==========================================================
   CONTENEDOR
   ========================================================== */

.block-container {

    max-width: 1350px;

    padding-top: 2rem;
    padding-bottom: 5rem;

}


/* ==========================================================
   TÍTULOS
   ========================================================== */

h1 {

    text-align: center;

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    font-size:
        clamp(3rem, 7vw, 6rem) !important;

    font-weight: 500 !important;

    letter-spacing:
        0.12em;

    color:
        #eee7dc !important;

    text-shadow:
        0 0 10px rgba(205,185,235,0.45),
        0 0 35px rgba(100,65,175,0.35),
        0 0 80px rgba(80,45,150,0.25);

}


h2,
h3 {

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    color:
        #ddd5c9 !important;

}


/* ==========================================================
   INSTRUCCIONES
   ========================================================== */

.instructions {

    background:
        rgba(12,9,18,0.72);

    border:
        1px solid rgba(175,150,205,0.18);

    border-left:
        3px solid rgba(160,125,215,0.65);

    padding:
        22px 26px;

    margin:
        25px 0 40px 0;

    box-shadow:
        0 15px 50px rgba(0,0,0,0.25);

}


/* ==========================================================
   TARJETAS DE ENTRADA
   ========================================================== */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        rgba(10,8,15,0.72);

    border:
        1px solid rgba(170,145,205,0.16);

    border-radius:
        8px;

    transition:
        transform 0.3s ease,
        border-color 0.3s ease,
        box-shadow 0.3s ease;

}


div[data-testid="stVerticalBlockBorderWrapper"]:hover {

    transform:
        translateY(-5px);

    border-color:
        rgba(180,145,235,0.55);

    box-shadow:
        0 15px 45px rgba(80,45,140,0.20);

}


/* ==========================================================
   BOTONES
   ========================================================== */

.stButton > button {

    width:
        100%;

    min-height:
        52px;

    border-radius:
        4px;

    border:
        1px solid rgba(170,135,215,0.55);

    background:
        linear-gradient(
            135deg,
            rgba(55,35,78,0.95),
            rgba(19,14,29,0.98)
        );

    color:
        #eee8de;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    letter-spacing:
        0.12em;

    transition:
        all 0.25s ease;

}


.stButton > button:hover {

    transform:
        translateY(-2px);

    border-color:
        rgba(215,190,245,0.85);

    box-shadow:
        0 0 25px rgba(145,100,225,0.25);

}


/* ==========================================================
   FILE UPLOADER
   ========================================================== */

[data-testid="stFileUploader"] {

    background:
        rgba(8,7,12,0.55);

    border:
        1px dashed rgba(165,135,205,0.25);

    padding:
        15px;

}


/* ==========================================================
   CAMERA
   ========================================================== */

[data-testid="stCameraInput"] {

    background:
        rgba(8,7,12,0.55);

    border:
        1px solid rgba(165,135,205,0.18);

    padding:
        10px;

}


/* ==========================================================
   ESPEJO
   ========================================================== */

.mirror-space {

    min-height:
        480px;

    margin:
        50px auto;

    border-radius:
        50% 50% 42% 42% / 18% 18% 45% 45%;

    border:
        4px solid rgba(175,150,205,0.48);

    background:

        radial-gradient(
            circle at 50% 50%,
            rgba(135,95,190,0.32),
            rgba(35,24,55,0.72) 25%,
            rgba(9,7,15,0.98) 70%
        );

    box-shadow:

        inset 0 0 50px rgba(180,145,245,0.15),

        inset 0 0 130px rgba(90,55,170,0.28),

        0 0 18px rgba(205,185,225,0.20),

        0 0 70px rgba(110,65,190,0.28),

        0 30px 100px rgba(0,0,0,0.70);

    animation:
        mirrorMovement 7s ease-in-out infinite;

}


@keyframes mirrorMovement {

    0% {

        background-position:
            50% 50%;

        box-shadow:

            inset 0 0 50px rgba(180,145,245,0.10),

            inset 0 0 130px rgba(90,55,170,0.22),

            0 0 18px rgba(205,185,225,0.18),

            0 0 55px rgba(110,65,190,0.23),

            0 30px 100px rgba(0,0,0,0.70);

    }

    50% {

        background-position:
            58% 42%;

        box-shadow:

            inset 0 0 70px rgba(195,160,255,0.18),

            inset 0 0 160px rgba(110,70,200,0.32),

            0 0 30px rgba(220,200,245,0.30),

            0 0 100px rgba(120,70,220,0.35),

            0 30px 100px rgba(0,0,0,0.70);

    }

    100% {

        background-position:
            50% 50%;

        box-shadow:

            inset 0 0 50px rgba(180,145,245,0.10),

            inset 0 0 130px rgba(90,55,170,0.22),

            0 0 18px rgba(205,185,225,0.18),

            0 0 55px rgba(110,65,190,0.23),

            0 30px 100px rgba(0,0,0,0.70);

    }

}


/* ==========================================================
   MÉTRICAS
   ========================================================== */

[data-testid="stMetric"] {

    background:
        rgba(12,9,18,0.75);

    border:
        1px solid rgba(170,145,200,0.15);

    padding:
        15px;

}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #06050a,
            #0b0811
        );

    border-right:
        1px solid rgba(180,160,205,0.12);

}


/* ==========================================================
   SELECTORES
   ========================================================== */

div[data-baseweb="select"] > div {

    background:
        #0d0a13 !important;

    border:
        1px solid rgba(180,160,205,0.18) !important;

}


/* ==========================================================
   AUDIO
   ========================================================== */

audio {

    width:
        100%;

}


/* ==========================================================
   SEPARADORES
   ========================================================== */

hr {

    border:
        none !important;

    height:
        1px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(160,120,210,0.45),
            transparent
        ) !important;

}

</style>
""",
unsafe_allow_html=True
)


# ============================================================
# TÍTULO
# ============================================================

st.title("ESPEJO MÁGICO")

st.markdown(
    "RECONOCIMIENTO ÓPTICO · TRADUCCIÓN · SÍNTESIS DE VOZ"
)


# ============================================================
# INSTRUCCIONES EXPLÍCITAS
# ============================================================

st.subheader("Cómo utilizar el espejo")

st.info(
    """
    **1. Elige una fuente de imagen.**
    Selecciona una de las dos opciones siguientes: cámara o archivo.

    **2. Proporciona una imagen que contenga texto.**
    Procura que el texto esté enfocado, bien iluminado y sea claramente visible.

    **3. El espejo analizará la imagen.**
    El sistema utilizará reconocimiento óptico de caracteres para identificar
    las palabras presentes en ella.

    **4. Revisa el texto reconocido.**
    Si el resultado contiene errores, utiliza una imagen más nítida y vuelve
    a intentarlo.

    **5. Configura la traducción.**
    En el panel lateral selecciona el idioma original y el idioma al que
    quieres traducir el texto.

    **6. Pulsa "DECIFRAR Y TRADUCIR".**
    El espejo procesará el mensaje y mostrará la traducción.

    **7. Reproduce el resultado.**
    Una vez terminada la traducción, podrás escucharla mediante el reproductor
    de audio.
    """
)


# ============================================================
# FUENTE DE IMAGEN
# ============================================================

st.subheader("1. Selecciona la fuente")


camera_col, upload_col = st.columns(2)


# ============================================================
# CÁMARA
# ============================================================

with camera_col:

    with st.container(border=True):

        st.markdown("### CÁMARA")

        st.write(
            "Utiliza la cámara para fotografiar directamente el texto."
        )

        use_camera = st.checkbox(
            "Activar cámara",
            key="camera"
        )

        if use_camera:

            img_file_buffer = st.camera_input(
                "Toma una fotografía"
            )

        else:

            img_file_buffer = None


# ============================================================
# ARCHIVO
# ============================================================

with upload_col:

    with st.container(border=True):

        st.markdown("### IMAGEN")

        st.write(
            "Carga una fotografía o imagen que ya tengas en tu equipo."
        )

        bg_image = st.file_uploader(
            "Seleccionar imagen",
            type=[
                "png",
                "jpg",
                "jpeg"
            ],
            key="upload"
        )


# ============================================================
# PROCESAMIENTO
# ============================================================

with st.sidebar:

    st.header("Procesamiento")

    filtro = st.radio(
        "Filtro para la cámara",
        (
            "Sí",
            "No"
        )
    )


# ============================================================
# OCR
# ============================================================

text = ""


# Archivo

if bg_image is not None:

    img_bytes = bg_image.getvalue()

    img_cv = cv2.imdecode(
        np.frombuffer(
            img_bytes,
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )

    img_rgb = cv2.cvtColor(
        img_cv,
        cv2.COLOR_BGR2RGB
    )

    text = pytesseract.image_to_string(
        img_rgb
    )


# Cámara

elif img_file_buffer is not None:

    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(
            bytes_data,
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )

    if filtro == "Sí":

        cv2_img = cv2.bitwise_not(
            cv2_img
        )

    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )

    text = pytesseract.image_to_string(
        img_rgb
    )


# ============================================================
# ESPEJO
# ============================================================

st.subheader("2. El espejo")


if text.strip():

    mirror_text = text.strip()

    st.markdown(
        f"""
        <style>

        .ocr-result-box {{
            background:
                rgba(12,9,20,0.82);

            border:
                1px solid rgba(180,150,220,0.25);

            border-radius:
                8px;

            padding:
                30px;

            margin:
                20px 0;

            box-shadow:
                0 0 50px rgba(100,60,180,0.15);

            animation:
                resultAppear 0.8s ease;

        }}

        @keyframes resultAppear {{

            from {{
                opacity: 0;
                transform: translateY(20px);
                filter: blur(8px);
            }}

            to {{
                opacity: 1;
                transform: translateY(0);
                filter: blur(0);
            }}

        }}

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### Texto identificado"
    )

    st.code(
        mirror_text,
        language=None
    )

else:

    st.markdown(
        """
        <style>

        .waiting-space {
            height: 480px;

            border-radius:
                50% 50% 42% 42% / 18% 18% 45% 45%;

            border:
                4px solid rgba(175,150,205,0.48);

            background:

                radial-gradient(
                    circle at 50% 50%,
                    rgba(115,80,175,0.32),
                    rgba(30,20,48,0.75) 30%,
                    rgba(7,5,12,0.99) 72%
                );

            box-shadow:

                inset 0 0 60px rgba(180,140,245,0.15),

                inset 0 0 150px rgba(85,50,160,0.30),

                0 0 25px rgba(190,165,220,0.20),

                0 0 80px rgba(100,55,180,0.30),

                0 30px 100px rgba(0,0,0,0.75);

            animation:
                waitingMirror 6s ease-in-out infinite;

        }

        @keyframes waitingMirror {

            0%, 100% {

                transform:
                    scale(1);

                filter:
                    brightness(0.9);

            }

            50% {

                transform:
                    scale(1.015);

                filter:
                    brightness(1.15);

            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "Selecciona una imagen para comenzar."
    )


# ============================================================
# DATOS OCR
# ============================================================

if text.strip():

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Palabras",
            len(text.split())
        )

    with col2:

        st.metric(
            "Caracteres",
            len(text.strip())
        )

    with col3:

        st.metric(
            "Estado",
            "Texto encontrado"
        )


# ============================================================
# TRADUCCIÓN
# ============================================================

st.markdown("---")

st.subheader(
    "3. Traducción"
)


with st.sidebar:

    st.header(
        "Configuración de traducción"
    )


    languages = {

        "Inglés": "en",
        "Español": "es",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja",
        "Ruso": "ru",
        "Alemán": "de"

    }


    in_lang = st.selectbox(
        "Idioma original",
        list(languages.keys())
    )

    input_language = languages[in_lang]


    out_lang = st.selectbox(
        "Idioma de destino",
        list(languages.keys())
    )

    output_language = languages[out_lang]


    accents = {

        "Predeterminado": "com",
        "India": "co.in",
        "Reino Unido": "co.uk",
        "Estados Unidos": "com",
        "Canadá": "ca",
        "Australia": "com.au",
        "Irlanda": "ie",
        "Sudáfrica": "co.za"

    }


    accent = st.selectbox(
        "Acento de voz",
        list(accents.keys())
    )

    tld = accents[accent]


# ============================================================
# BOTÓN
# ============================================================

translate = st.button(
    "DECIFRAR Y TRADUCIR",
    use_container_width=True
)


# ============================================================
# RESULTADO
# ============================================================

if translate:

    if not text.strip():

        st.warning(
            "No se encontró texto. Primero proporciona una imagen."
        )

    else:

        try:

            result, output_text = text_to_speech(
                input_language,
                output_language,
                text,
                tld
            )


            st.subheader(
                "4. Mensaje descifrado"
            )


            # Texto progresivo

            output_placeholder = st.empty()

            current_text = ""

            for character in output_text:

                current_text += character

                output_placeholder.markdown(
                    f"### {current_text}"
                )

                time.sleep(0.015)


            st.success(
                "La traducción ha sido completada."
            )


            # ==================================================
            # AUDIO
            # ==================================================

            st.subheader(
                "5. Escuchar traducción"
            )


            with open(
                f"temp/{result}.mp3",
                "rb"
            ) as audio_file:

                audio_bytes = audio_file.read()


            st.audio(
                audio_bytes,
                format="audio/mp3"
            )


        except Exception as e:

            st.error(
                f"No fue posible completar la traducción: {e}"
            )
