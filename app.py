import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
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

text = " "


# ============================================================
# CARPETA DE AUDIO
# ============================================================

try:
    os.mkdir("temp")
except:
    pass


# ============================================================
# LIMPIEZA DE ARCHIVOS
# ============================================================

def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) != 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)

                print("Eliminado:", f)


remove_files(7)


# ============================================================
# TRADUCCIÓN + AUDIO
# ============================================================

def text_to_speech(
    input_language,
    output_language,
    text,
    tld
):

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

        my_file_name = text[0:20]

    except:

        my_file_name = "audio"


    # Evitar caracteres problemáticos en nombres de archivo

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

/* Fondo general */

.stApp {

    background:
        radial-gradient(
            circle at 50% 15%,
            rgba(86, 61, 125, 0.28),
            transparent 25%
        ),
        radial-gradient(
            circle at 15% 70%,
            rgba(40, 65, 105, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 60%,
            rgba(100, 45, 95, 0.18),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #05040a,
            #0b0812,
            #050409
        );

}


/* Contenedor */

.block-container {

    max-width: 1400px;

    padding-top: 2rem;
    padding-bottom: 5rem;

}


/* Títulos */

h1 {

    text-align: center;

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    font-size:
        clamp(3rem, 7vw, 6rem) !important;

    letter-spacing:
        0.12em;

    color:
        #eee7dc !important;

    text-shadow:
        0 0 10px rgba(190,170,230,0.45),
        0 0 35px rgba(100,70,170,0.35);

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


/* Subtítulo */

.mirror-description {

    text-align: center;

    color: #89818e;

    font-size: 0.75rem;

    letter-spacing: 0.3em;

    text-transform: uppercase;

    margin-bottom: 35px;

}


/* ============================================================
   ESPEJO
   ============================================================ */

.mirror {

    position: relative;

    min-height: 460px;

    margin: 20px auto 45px auto;

    padding: 65px 45px;

    max-width: 1050px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

    border-radius:
        48% 48% 43% 43% / 18% 18% 48% 48%;

    border:
        4px solid rgba(173,150,198,0.48);

    background:

        radial-gradient(
            ellipse at center,
            rgba(100,75,155,0.28),
            rgba(19,14,31,0.96) 50%,
            rgba(5,4,9,0.99) 78%
        );

    box-shadow:

        inset 0 0 35px rgba(190,160,255,0.10),

        inset 0 0 100px rgba(80,50,160,0.22),

        0 0 15px rgba(200,180,230,0.20),

        0 0 55px rgba(100,65,180,0.30),

        0 30px 100px rgba(0,0,0,0.75);

    overflow: hidden;

    animation:
        mirrorBreathing 5s ease-in-out infinite;

}


@keyframes mirrorBreathing {

    0%, 100% {

        box-shadow:

            inset 0 0 35px rgba(190,160,255,0.08),

            inset 0 0 100px rgba(80,50,160,0.18),

            0 0 15px rgba(200,180,230,0.18),

            0 0 45px rgba(100,65,180,0.25),

            0 30px 100px rgba(0,0,0,0.75);

    }

    50% {

        box-shadow:

            inset 0 0 50px rgba(200,170,255,0.15),

            inset 0 0 130px rgba(100,65,190,0.25),

            0 0 25px rgba(220,200,245,0.28),

            0 0 75px rgba(120,75,210,0.38),

            0 30px 100px rgba(0,0,0,0.75);

    }

}


/* Luz interna */

.mirror::before {

    content: "";

    position: absolute;

    width: 500px;

    height: 500px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(170,130,255,0.13),
            transparent 68%
        );

    animation:
        mirrorLight 6s ease-in-out infinite;

    pointer-events: none;

}


@keyframes mirrorLight {

    0%, 100% {

        transform:
            scale(0.75);

        opacity:
            0.4;

    }

    50% {

        transform:
            scale(1.35);

        opacity:
            0.9;

    }

}


/* Contenido */

.mirror-title {

    position: relative;

    z-index: 2;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        clamp(0.75rem, 1.5vw, 1rem);

    letter-spacing:
        0.35em;

    text-transform:
        uppercase;

    color:
        #978ba5;

    margin-bottom:
        25px;

}


.mirror-text {

    position: relative;

    z-index: 2;

    max-width: 850px;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        clamp(1.5rem, 3vw, 2.7rem);

    line-height:
        1.5;

    color:
        #eee8df;

    text-shadow:
        0 0 15px rgba(190,170,240,0.35);

    animation:
        textReveal 1s ease;

}


@keyframes textReveal {

    from {

        opacity: 0;

        transform:
            translateY(15px);

        filter:
            blur(10px);

    }

    to {

        opacity: 1;

        transform:
            translateY(0);

        filter:
            blur(0);

    }

}


/* Estado */

.mirror-status {

    position: relative;

    z-index: 2;

    margin-top: 35px;

    color:
        #817887;

    font-size:
        0.65rem;

    letter-spacing:
        0.22em;

    text-transform:
        uppercase;

}


.mirror-orb {

    display: inline-block;

    width: 8px;

    height: 8px;

    border-radius: 50%;

    margin-right: 10px;

    background:
        #b394e5;

    box-shadow:
        0 0 8px #b394e5,
        0 0 20px rgba(170,120,240,0.8);

    animation:
        orbPulse 1.4s infinite;

}


@keyframes orbPulse {

    0%, 100% {

        transform:
            scale(0.7);

        opacity:
            0.5;

    }

    50% {

        transform:
            scale(1.3);

        opacity:
            1;

    }

}


/* ============================================================
   PANELES
   ============================================================ */

[data-testid="stFileUploader"] {

    background:
        rgba(10,8,15,0.85);

    border:
        1px solid rgba(180,160,210,0.16);

    padding:
        18px;

    transition:
        0.3s ease;

}


[data-testid="stFileUploader"]:hover {

    border-color:
        rgba(165,125,225,0.6);

    box-shadow:
        0 0 35px rgba(110,70,190,0.15);

}


/* ============================================================
   BOTONES
   ============================================================ */

.stButton > button {

    min-height:
        55px;

    border-radius:
        3px;

    border:
        1px solid rgba(170,135,215,0.55);

    background:
        linear-gradient(
            135deg,
            rgba(54,35,75,0.95),
            rgba(20,15,29,0.98)
        );

    color:
        #eee7dc;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    letter-spacing:
        0.16em;

    transition:
        all 0.3s ease;

}


.stButton > button:hover {

    transform:
        translateY(-3px);

    border-color:
        rgba(215,190,245,0.9);

    box-shadow:
        0 0 25px rgba(150,105,230,0.28),
        0 0 60px rgba(110,70,190,0.14);

}


/* ============================================================
   SELECTORES
   ============================================================ */

div[data-baseweb="select"] > div {

    background:
        #0d0a13 !important;

    border:
        1px solid rgba(180,160,205,0.18) !important;

}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #06050a,
            #0b0811
        );

    border-right:
        1px solid rgba(180,160,205,0.12);

    box-shadow:
        15px 0 70px rgba(0,0,0,0.6);

}


/* ============================================================
   MÉTRICAS
   ============================================================ */

[data-testid="stMetric"] {

    background:
        rgba(15,11,22,0.7);

    border:
        1px solid rgba(170,145,200,0.12);

    padding:
        15px;

}


/* ============================================================
   AUDIO
   ============================================================ */

audio {

    width: 100%;

    filter:
        drop-shadow(
            0 0 20px rgba(130,90,210,0.25)
        );

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
    "RECONOCIMIENTO · DECIFRADO · TRADUCCIÓN · VOZ",
    unsafe_allow_html=False
)


# ============================================================
# INSTRUCCIONES
# ============================================================

with st.expander(
    "INSTRUCCIONES"
):

    st.write(
        """
        El espejo puede interpretar el texto contenido en una imagen
        y posteriormente traducirlo a otro idioma.

        1. Selecciona una fuente de imagen.
           Puedes utilizar la cámara o cargar una imagen desde tu equipo.

        2. Procura que el texto sea nítido, tenga suficiente iluminación
           y aparezca relativamente recto.

        3. Si utilizas la cámara, puedes activar el filtro de imagen
           desde el panel lateral.

        4. El espejo analizará la imagen mediante reconocimiento óptico
           de caracteres y mostrará el texto que consiga identificar.

        5. Selecciona en el panel lateral el idioma del texto original
           y el idioma al que deseas traducirlo.

        6. Selecciona el acento de la voz cuando corresponda.

        7. Presiona "DECIFRAR Y TRADUCIR".

        8. El resultado aparecerá en el espejo y podrás reproducir
           la traducción mediante audio.
        """
    )


# ============================================================
# ESPEJO INICIAL
# ============================================================

st.markdown(
    """
    <div class="mirror">
        <div class="mirror-title">
            Estado del espejo
        </div>

        <div class="mirror-text">
            Esperando una imagen...
        </div>

        <div class="mirror-status">
            <span class="mirror-orb"></span>
            Sistema preparado
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUENTE DE IMAGEN
# ============================================================

st.subheader(
    "Fuente de imagen"
)


cam_ = st.checkbox(
    "Usar cámara"
)


if cam_:

    img_file_buffer = st.camera_input(
        "Toma una fotografía del texto"
    )

else:

    img_file_buffer = None


with st.sidebar:

    st.subheader(
        "Procesamiento de imagen"
    )

    filtro = st.radio(
        "Aplicar filtro a la imagen de cámara",
        (
            "Sí",
            "No"
        )
    )


# ============================================================
# CARGAR IMAGEN
# ============================================================

bg_image = st.file_uploader(
    "Cargar imagen",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)


# ============================================================
# OCR DESDE ARCHIVO
# ============================================================

if bg_image is not None:

    uploaded_file = bg_image

    st.image(
        uploaded_file,
        caption="Imagen cargada",
        use_container_width=True
    )


    img_bytes = uploaded_file.getvalue()

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


# ============================================================
# OCR DESDE CÁMARA
# ============================================================

if img_file_buffer is not None:

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
# RESULTADO OCR
# ============================================================

clean_text = text.strip()


if clean_text:

    safe_text = (
        clean_text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    st.markdown(
        f"""
        <div class="mirror">

            <div class="mirror-title">
                Texto identificado
            </div>

            <div class="mirror-text">
                {safe_text}
            </div>

            <div class="mirror-status">
                <span class="mirror-orb"></span>
                Texto decifrado
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Palabras",
            len(clean_text.split())
        )


    with col2:

        st.metric(
            "Caracteres",
            len(clean_text)
        )


else:

    st.info(
        "El espejo todavía no ha identificado texto."
    )


# ============================================================
# TRADUCCIÓN
# ============================================================

st.markdown("---")

st.subheader(
    "Traducción"
)


with st.sidebar:

    st.markdown("---")

    st.subheader(
        "Configuración de traducción"
    )


    translator = Translator()


    # --------------------------------------------------------
    # IDIOMA DE ENTRADA
    # --------------------------------------------------------

    in_lang = st.selectbox(
        "Idioma del texto original",
        (
            "Inglés",
            "Español",
            "Bengalí",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Ruso",
            "Alemán"
        )
    )


    input_languages = {

        "Inglés": "en",
        "Español": "es",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja",
        "Ruso": "ru",
        "Alemán": "de"

    }


    input_language = input_languages[in_lang]


    # --------------------------------------------------------
    # IDIOMA DE SALIDA
    # --------------------------------------------------------

    out_lang = st.selectbox(
        "Idioma de traducción",
        (
            "Inglés",
            "Español",
            "Bengalí",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Ruso",
            "Alemán"
        )
    )


    output_languages = {

        "Inglés": "en",
        "Español": "es",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja",
        "Ruso": "ru",
        "Alemán": "de"

    }


    output_language = output_languages[out_lang]


    # --------------------------------------------------------
    # ACENTO
    # --------------------------------------------------------

    english_accent = st.selectbox(
        "Acento de la voz",
        (
            "Predeterminado",
            "India",
            "Reino Unido",
            "Estados Unidos",
            "Canadá",
            "Australia",
            "Irlanda",
            "Sudáfrica"
        )
    )


    accent_domains = {

        "Predeterminado": "com",
        "India": "co.in",
        "Reino Unido": "co.uk",
        "Estados Unidos": "com",
        "Canadá": "ca",
        "Australia": "com.au",
        "Irlanda": "ie",
        "Sudáfrica": "co.za"

    }


    tld = accent_domains[english_accent]


# ============================================================
# CONVERSIÓN
# ============================================================

display_output_text = st.checkbox(
    "Mostrar también el texto traducido"
)


if st.button(
    "DECIFRAR Y TRADUCIR"
):

    if not clean_text:

        st.warning(
            "El espejo necesita una imagen que contenga texto antes de poder realizar la traducción."
        )

    else:

        result, output_text = text_to_speech(
            input_language,
            output_language,
            text,
            tld
        )


        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        safe_output = (
            output_text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )


        st.markdown(
            f"""
            <div class="mirror">

                <div class="mirror-title">
                    Traducción completada
                </div>

                <div class="mirror-text">
                    {safe_output}
                </div>

                <div class="mirror-status">
                    <span class="mirror-orb"></span>
                    Mensaje traducido
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # AUDIO
        # ----------------------------------------------------

        st.subheader(
            "Voz de la traducción"
        )


        audio_file = open(
            f"temp/{result}.mp3",
            "rb"
        )


        audio_bytes = audio_file.read()


        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )


        if display_output_text:

            st.markdown("---")

            st.subheader(
                "Texto traducido"
            )

            st.write(
                output_text
            )
