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
# VARIABLES
# ============================================================

text = ""


# ============================================================
# CARPETA DE AUDIO
# ============================================================

os.makedirs("temp", exist_ok=True)


# ============================================================
# LIMPIEZA DE ARCHIVOS
# ============================================================

def remove_files(days):

    mp3_files = glob.glob("temp/*.mp3")

    now = time.time()

    for file in mp3_files:

        if os.stat(file).st_mtime < now - (days * 86400):

            os.remove(file)


remove_files(7)


# ============================================================
# TRADUCCIÓN Y AUDIO
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

    trans_text = translation.text

    tts = gTTS(
        trans_text,
        lang=output_language,
        tld=tld,
        slow=False
    )

    try:

        my_file_name = text[:20]

    except:

        my_file_name = "audio"


    my_file_name = "".join(
        c for c in my_file_name
        if c.isalnum() or c in (" ", "_", "-")
    ).strip()


    if not my_file_name:

        my_file_name = "audio"


    tts.save(
        f"temp/{my_file_name}.mp3"
    )

    return my_file_name, trans_text


# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
"""
<style>

/* ============================================================
   FONDO
   ============================================================ */

.stApp {

    background:
        radial-gradient(
            circle at 15% 20%,
            rgba(105, 60, 190, 0.25),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 25%,
            rgba(50, 110, 210, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(170, 50, 150, 0.20),
            transparent 35%
        ),
        linear-gradient(
            125deg,
            #030207,
            #0b0614,
            #050916,
            #100713,
            #030207
        );

    background-size:
        250% 250%;

    animation:
        backgroundFlow 18s ease infinite;

}


@keyframes backgroundFlow {

    0% {
        background-position: 0% 50%;
    }

    25% {
        background-position: 70% 20%;
    }

    50% {
        background-position: 100% 75%;
    }

    75% {
        background-position: 30% 100%;
    }

    100% {
        background-position: 0% 50%;
    }

}


/* ============================================================
   PARTÍCULAS
   ============================================================ */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 0;

    opacity: 0.55;

    background-image:

        radial-gradient(
            circle,
            rgba(225,210,255,0.9) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle,
            rgba(125,180,255,0.75) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle,
            rgba(210,150,255,0.65) 0 1px,
            transparent 2px
        );

    background-size:
        73px 91px,
        137px 157px,
        211px 193px;

    animation:
        particleDrift 35s linear infinite;

}


@keyframes particleDrift {

    0% {
        transform:
            translate(0, 0);
    }

    50% {
        transform:
            translate(25px, -40px);
    }

    100% {
        transform:
            translate(-15px, -80px);
    }

}


/* ============================================================
   NIEBLA LUMINOSA
   ============================================================ */

.stApp::after {

    content: "";

    position: fixed;

    inset: -20%;

    pointer-events: none;

    z-index: 0;

    background:

        radial-gradient(
            circle at 20% 30%,
            rgba(120,70,220,0.10),
            transparent 15%
        ),

        radial-gradient(
            circle at 75% 20%,
            rgba(50,120,220,0.09),
            transparent 17%
        ),

        radial-gradient(
            circle at 55% 80%,
            rgba(190,60,180,0.09),
            transparent 20%
        );

    filter:
        blur(30px);

    animation:
        atmosphericMotion 12s ease-in-out infinite alternate;

}


@keyframes atmosphericMotion {

    from {
        transform:
            translate(-3%, -2%)
            scale(1);
    }

    to {
        transform:
            translate(3%, 3%)
            scale(1.10);
    }

}


/* ============================================================
   CONTENIDO
   ============================================================ */

.block-container {

    position: relative;

    z-index: 1;

    max-width:
        1400px;

    padding-top:
        2rem;

    padding-bottom:
        6rem;

}


/* ============================================================
   TÍTULO
   ============================================================ */

h1 {

    text-align:
        center;

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    font-size:
        clamp(3rem, 7vw, 6rem) !important;

    font-weight:
        500 !important;

    letter-spacing:
        0.14em;

    color:
        #eee7dc !important;

    text-shadow:

        0 0 10px
        rgba(230,215,255,0.60),

        0 0 30px
        rgba(150,100,240,0.45),

        0 0 70px
        rgba(90,50,180,0.35);

    animation:
        titlePulse 4s ease-in-out infinite;

}


@keyframes titlePulse {

    0%, 100% {

        filter:
            brightness(0.95);

    }

    50% {

        filter:
            brightness(1.15);

    }

}


/* ============================================================
   SUBTÍTULOS
   ============================================================ */

h2,
h3 {

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    color:
        #ddd5c9 !important;

}


/* ============================================================
   INSTRUCCIONES
   ============================================================ */

[data-testid="stAlert"] {

    background:
        rgba(10,8,17,0.82) !important;

    border:
        1px solid
        rgba(175,145,220,0.25) !important;

    box-shadow:
        0 15px 50px
        rgba(0,0,0,0.35);

}


/* ============================================================
   TARJETAS
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        linear-gradient(
            145deg,
            rgba(22,15,34,0.92),
            rgba(6,5,11,0.94)
        );

    border:
        1px solid
        rgba(175,145,220,0.22);

    border-radius:
        10px;

    box-shadow:

        inset 0 0 35px
        rgba(130,80,200,0.06),

        0 15px 55px
        rgba(0,0,0,0.40);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;

}


div[data-testid="stVerticalBlockBorderWrapper"]:hover {

    transform:
        translateY(-6px)
        scale(1.01);

    border-color:
        rgba(210,180,245,0.60);

    box-shadow:

        inset 0 0 45px
        rgba(140,90,220,0.10),

        0 20px 75px
        rgba(90,45,170,0.30),

        0 0 30px
        rgba(160,110,240,0.14);

}


/* ============================================================
   BOTONES
   ============================================================ */

.stButton > button {

    width:
        100%;

    min-height:
        58px;

    border-radius:
        5px;

    border:
        1px solid
        rgba(180,145,225,0.60);

    background:

        linear-gradient(
            120deg,
            #26163a,
            #0e0916,
            #321a4b,
            #0e0916
        );

    background-size:
        300% 300%;

    color:
        #f0e9df;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    letter-spacing:
        0.15em;

    transition:
        all 0.25s ease;

}


.stButton > button:hover {

    transform:
        translateY(-3px);

    background-position:
        100% 50%;

    border-color:
        rgba(230,210,250,0.90);

    box-shadow:

        0 0 25px
        rgba(170,120,245,0.40),

        0 0 70px
        rgba(100,60,190,0.20);

}


/* ============================================================
   UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {

    background:
        rgba(7,6,12,0.65);

    border:
        1px dashed
        rgba(170,140,215,0.35);

    border-radius:
        7px;

    transition:
        all 0.3s ease;

}


[data-testid="stFileUploader"]:hover {

    border-color:
        rgba(210,180,245,0.75);

    box-shadow:
        0 0 35px
        rgba(120,70,200,0.20);

}


/* ============================================================
   IMÁGENES
   ============================================================ */

[data-testid="stImage"] img {

    border-radius:
        8px;

    box-shadow:

        0 0 25px
        rgba(130,80,210,0.18),

        0 20px 55px
        rgba(0,0,0,0.50);

}


/* ============================================================
   SELECTORES
   ============================================================ */

div[data-baseweb="select"] > div {

    background:
        rgba(9,7,14,0.95) !important;

    border:
        1px solid
        rgba(175,145,215,0.22) !important;

}


div[data-baseweb="select"] > div:hover {

    border-color:
        rgba(205,175,245,0.65) !important;

    box-shadow:
        0 0 25px
        rgba(130,80,200,0.15);

}


/* ============================================================
   MÉTRICAS
   ============================================================ */

[data-testid="stMetric"] {

    background:
        rgba(11,8,18,0.78);

    border:
        1px solid
        rgba(175,145,210,0.17);

    border-radius:
        7px;

    padding:
        15px;

    box-shadow:
        inset 0 0 25px
        rgba(120,75,190,0.05);

}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {

    background:

        radial-gradient(
            circle at 50% 10%,
            rgba(90,50,145,0.16),
            transparent 35%
        ),

        linear-gradient(
            180deg,
            #050409,
            #0b0711
        );

    border-right:
        1px solid
        rgba(175,145,210,0.14);

    box-shadow:
        15px 0 70px
        rgba(0,0,0,0.60);

}


/* ============================================================
   AUDIO
   ============================================================ */

audio {

    width:
        100%;

    filter:
        drop-shadow(
            0 0 20px
            rgba(135,90,220,0.30)
        );

}


/* ============================================================
   SEPARADORES
   ============================================================ */

hr {

    border:
        none !important;

    height:
        1px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(170,130,230,0.50),
            rgba(220,200,250,0.35),
            rgba(170,130,230,0.50),
            transparent
        ) !important;

    box-shadow:
        0 0 15px
        rgba(130,80,200,0.30);

}

</style>
""",
unsafe_allow_html=True
)


# ============================================================
# TÍTULO
# ============================================================

st.title("ESPEJO MÁGICO")

st.caption(
    "RECONOCIMIENTO ÓPTICO · TRADUCCIÓN · SÍNTESIS DE VOZ"
)


# ============================================================
# INSTRUCCIONES
# ============================================================

st.subheader("Instrucciones")

st.info(
    """
    **1. Elige cámara o imagen.**

    **2. Introduce una imagen con texto.**

    **3. Selecciona los idiomas en el panel lateral.**

    **4. Pulsa "DECIFRAR Y TRADUCIR".**

    **5. Lee o escucha el resultado.**
    """
)


# ============================================================
# FUENTE DE IMAGEN
# ============================================================

st.subheader("Fuente de imagen")


camera_col, upload_col = st.columns(2)


with camera_col:

    with st.container(border=True):

        st.markdown("### CÁMARA")

        st.write(
            "Fotografía el texto directamente."
        )

        use_camera = st.checkbox(
            "Activar cámara",
            key="camera"
        )

        if use_camera:

            img_file_buffer = st.camera_input(
                "Tomar fotografía"
            )

        else:

            img_file_buffer = None


with upload_col:

    with st.container(border=True):

        st.markdown("### IMAGEN")

        st.write(
            "Carga una imagen desde tu equipo."
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

st.subheader("Espejo")


if text.strip():

    st.success(
        "Texto identificado."
    )

    st.code(
        text.strip(),
        language=None
    )

else:

    st.write(
        "El espejo está esperando una imagen."
    )


# ============================================================
# INFORMACIÓN DEL OCR
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
            "Listo"
        )


# ============================================================
# TRADUCCIÓN
# ============================================================

st.markdown("---")

st.subheader("Traducción")


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
            "Primero proporciona una imagen con texto."
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
                "Mensaje descifrado"
            )


            # Revelación progresiva

            output_placeholder = st.empty()

            current_text = ""

            for character in output_text:

                current_text += character

                output_placeholder.markdown(
                    f"### {current_text}"
                )

                time.sleep(0.015)


            st.success(
                "Traducción completada."
            )


            # =================================================
            # AUDIO
            # =================================================

            st.subheader(
                "Escuchar traducción"
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
