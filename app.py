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
# CONFIGURATION
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
# AUDIO DIRECTORY
# ============================================================

os.makedirs("temp", exist_ok=True)


# ============================================================
# REMOVE OLD AUDIO FILES
# ============================================================

def remove_files(days):

    mp3_files = glob.glob("temp/*.mp3")

    now = time.time()

    for file in mp3_files:

        if os.stat(file).st_mtime < now - (days * 86400):

            os.remove(file)


remove_files(7)


# ============================================================
# TRANSLATION + TEXT TO SPEECH
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
# VISUAL STYLE
# ============================================================

st.markdown(
"""
<style>

/* ============================================================
   MAIN BACKGROUND
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

    background-size: 250% 250%;

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
   AMBIENT PARTICLES
   ============================================================ */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 0;

    opacity: 0.45;

    background-image:

        radial-gradient(
            circle,
            rgba(225,210,255,0.8) 0 1px,
            transparent 2px
        );

    background-size: 97px 113px;

    animation:
        backgroundParticles 30s linear infinite;

}


@keyframes backgroundParticles {

    from {
        transform:
            translate3d(0, 0, 0);
    }

    50% {
        transform:
            translate3d(35px, -50px, 0);
    }

    to {
        transform:
            translate3d(-15px, -100px, 0);
    }

}


/* ============================================================
   ATMOSPHERE
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

    filter: blur(30px);

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
   CONTENT
   ============================================================ */

.block-container {

    position: relative;

    z-index: 1;

    max-width: 1400px;

    padding-top: 2rem;

    padding-bottom: 6rem;

}


/* ============================================================
   TITLE
   ============================================================ */

h1 {

    text-align: center;

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    font-size:
        clamp(3rem, 7vw, 6rem) !important;

    font-weight: 500 !important;

    letter-spacing: 0.14em;

    color: #eee7dc !important;

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
   HEADINGS
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
   INFO BOX
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
   BORDERED STREAMLIT CONTAINERS
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
   BUTTONS
   ============================================================ */

.stButton > button {

    width: 100%;

    min-height: 58px;

    border-radius: 5px;

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

    background-size: 300% 300%;

    color: #f0e9df;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    letter-spacing: 0.15em;

    transition: all 0.25s ease;

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
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {

    background:
        rgba(7,6,12,0.65);

    border:
        1px dashed
        rgba(170,140,215,0.35);

    border-radius: 7px;

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
   IMAGES
   ============================================================ */

[data-testid="stImage"] img {

    border-radius: 8px;

    box-shadow:

        0 0 25px
        rgba(130,80,210,0.18),

        0 20px 55px
        rgba(0,0,0,0.50);

}


/* ============================================================
   SELECT BOXES
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

    width: 100%;

    filter:
        drop-shadow(
            0 0 20px
            rgba(135,90,220,0.30)
        );

}


/* ============================================================
   MIRROR
   ============================================================ */

.magic-mirror {

    position: relative;

    width: 100%;

    height: 620px;

    overflow: hidden;

    border-radius: 18px;

    background:

        radial-gradient(
            ellipse at 50% 50%,
            rgba(75,48,120,0.34),
            rgba(12,8,22,0.96) 68%
        );

    border:
        1px solid
        rgba(190,165,235,0.42);

    box-shadow:

        0 0 20px
        rgba(140,90,220,0.30),

        0 0 70px
        rgba(100,55,190,0.20),

        inset 0 0 80px
        rgba(100,65,160,0.25);

}


/* ============================================================
   MIRROR LIGHT
   ============================================================ */

.magic-mirror::before {

    content: "";

    position: absolute;

    width: 75%;

    height: 65%;

    left: 12.5%;

    top: 17%;

    border-radius: 50%;

    background:
        radial-gradient(
            ellipse,
            rgba(175,145,235,0.13),
            rgba(90,55,160,0.07) 45%,
            transparent 72%
        );

    filter: blur(20px);

    animation:
        mirrorBreathing 5s ease-in-out infinite;

}


@keyframes mirrorBreathing {

    0%, 100% {

        transform:
            scale(0.94);

        opacity:
            0.55;

    }

    50% {

        transform:
            scale(1.08);

        opacity:
            1;

    }

}


/* ============================================================
   MOVING LIGHT
   ============================================================ */

.mirror-light {

    position: absolute;

    width: 240px;

    height: 240px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(225,210,255,0.18),
            rgba(130,90,220,0.08),
            transparent 70%
        );

    filter: blur(12px);

    animation:
        lightMovement 9s ease-in-out infinite alternate;

    pointer-events: none;

}


@keyframes lightMovement {

    0% {

        left: 8%;
        top: 15%;

    }

    30% {

        left: 62%;
        top: 12%;

    }

    60% {

        left: 75%;
        top: 62%;

    }

    100% {

        left: 20%;
        top: 65%;

    }

}


/* ============================================================
   PARTICLES INSIDE MIRROR
   ============================================================ */

.magic-particles {

    position: absolute;

    inset: 0;

    overflow: hidden;

    pointer-events: none;

}


.magic-particle {

    position: absolute;

    width: 3px;

    height: 3px;

    border-radius: 50%;

    background:
        rgba(225,215,255,0.90);

    box-shadow:
        0 0 8px
        rgba(190,160,255,0.90);

    animation:
        particleFloat var(--duration) ease-in-out infinite;

    animation-delay:
        var(--delay);

}


@keyframes particleFloat {

    0% {

        transform:
            translate3d(
                0,
                30px,
                0
            )
            scale(0.4);

        opacity: 0;

    }

    15% {

        opacity: 0.85;

    }

    50% {

        transform:
            translate3d(
                var(--drift),
                -180px,
                0
            )
            scale(1);

        opacity: 1;

    }

    85% {

        opacity: 0.65;

    }

    100% {

        transform:
            translate3d(
                calc(var(--drift) * -0.5),
                -390px,
                0
            )
            scale(0.2);

        opacity: 0;

    }

}


/* ============================================================
   MIRROR CONTENT
   ============================================================ */

.mirror-content {

    position: absolute;

    inset: 0;

    z-index: 5;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    padding: 60px;

    text-align: center;

}


.mirror-label {

    font-family:
        Georgia,
        serif;

    font-size: 0.75rem;

    letter-spacing: 0.35em;

    color:
        rgba(205,190,225,0.65);

    margin-bottom: 25px;

    text-transform: uppercase;

}


.mirror-message {

    max-width: 850px;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        clamp(1.5rem, 3vw, 2.7rem);

    line-height: 1.45;

    color: #eee8f5;

    text-shadow:

        0 0 8px
        rgba(230,215,255,0.55),

        0 0 30px
        rgba(150,105,230,0.40);

}


/* ============================================================
   DECIPHER ANIMATION
   ============================================================ */

.deciphered {

    animation:
        messageReveal 1.4s ease forwards;

}


@keyframes messageReveal {

    0% {

        opacity: 0;

        transform:
            scale(0.94);

        filter:
            blur(12px);

    }

    60% {

        opacity: 1;

        filter:
            blur(1px);

    }

    100% {

        opacity: 1;

        transform:
            scale(1);

        filter:
            blur(0);

    }

}


/* ============================================================
   SCANNING BEAM
   ============================================================ */

.scan-beam {

    position: absolute;

    left: 5%;

    right: 5%;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(220,205,255,0.85),
            transparent
        );

    box-shadow:

        0 0 10px
        rgba(200,175,255,0.9),

        0 0 35px
        rgba(140,90,230,0.7);

    opacity: 0.75;

    animation:
        scanning 4s linear infinite;

}


@keyframes scanning {

    0% {

        top: 15%;

        opacity: 0;

    }

    10% {

        opacity: 1;

    }

    90% {

        opacity: 1;

    }

    100% {

        top: 85%;

        opacity: 0;

    }

}


/* ============================================================
   MIRROR FRAME
   ============================================================ */

.magic-mirror-frame {

    position: absolute;

    inset: 14px;

    border:
        1px solid
        rgba(200,180,235,0.14);

    border-radius: 13px;

    pointer-events: none;

}


.magic-mirror-frame::before,
.magic-mirror-frame::after {

    content: "";

    position: absolute;

    width: 45px;

    height: 45px;

    border-color:
        rgba(210,190,245,0.45);

}


.magic-mirror-frame::before {

    top: -1px;

    left: -1px;

    border-top: 2px solid;

    border-left: 2px solid;

}


.magic-mirror-frame::after {

    bottom: -1px;

    right: -1px;

    border-bottom: 2px solid;

    border-right: 2px solid;

}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .magic-mirror {

        height: 500px;

    }

    .mirror-content {

        padding: 35px;

    }

}

</style>
""",
unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.title("ESPEJO MÁGICO")

st.caption(
    "DESCIFRA MENSAJES OCULTOS EN CUALQUIER IDIOMA"
)


# ============================================================
# INSTRUCTIONS
# ============================================================

st.subheader("Instrucciones")

st.info(
    """
    **1. Elige cámara o imagen.**

    **2. Introduce el mensaje.**

    **3. Selecciona los idiomas en el panel lateral.**

    **4. Pulsa "DECIFRAR Y TRADUCIR".**
    """
)


# ============================================================
# IMAGE SOURCE
# ============================================================

st.subheader("Fuente de imagen")

camera_col, upload_col = st.columns(2)


with camera_col:

    with st.container(border=True):

        st.markdown("### CÁMARA")

        st.write(
            "Fotografía el mensaje."
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
            "Carga una imagen."
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
# CAMERA PROCESSING OPTION
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
# PARTICLES
# ============================================================

particles = ""

particle_data = [

    (7, 14, 18, -5, 35),
    (13, 21, 23, -11, -40),
    (19, 9, 17, -4, 55),
    (25, 31, 26, -16, -30),
    (31, 17, 20, -7, 45),
    (37, 42, 28, -20, -55),
    (43, 12, 19, -3, 30),
    (49, 28, 24, -14, -45),
    (55, 51, 31, -18, 60),
    (61, 19, 21, -8, -35),
    (67, 37, 27, -15, 50),
    (73, 11, 22, -6, -60),
    (79, 45, 29, -19, 40),
    (85, 26, 18, -5, -30),
    (91, 57, 25, -13, 55),
    (16, 63, 30, -22, -45),
    (34, 72, 21, -9, 35),
    (52, 67, 27, -17, -50),
    (70, 76, 23, -12, 45),
    (88, 69, 32, -24, -35)

]


for left, bottom, duration, delay, drift in particle_data:

    particles += f"""
    <span
        class="magic-particle"
        style="
            left:{left}%;
            bottom:{bottom}%;
            --duration:{duration}s;
            --delay:{delay}s;
            --drift:{drift}px;
        ">
    </span>
    """


# ============================================================
# MIRROR STATE
# ============================================================

if text.strip():

    mirror_label = "MENSAJE DETECTADO"

    mirror_message = text.strip()

    mirror_class = "mirror-message deciphered"

else:

    mirror_label = "ESPERANDO MENSAJE"

    mirror_message = (
        "Introduce una imagen para que el espejo "
        "pueda descifrarla."
    )

    mirror_class = "mirror-message"


# ============================================================
# MAGIC MIRROR
# ============================================================

st.subheader("Espejo")

st.markdown(
f"""
<div class="magic-mirror">

    <div class="magic-mirror-frame"></div>

    <div class="mirror-light"></div>

    <div class="magic-particles">

        {particles}

    </div>

    <div class="scan-beam"></div>

    <div class="mirror-content">

        <div class="mirror-label">
            {mirror_label}
        </div>

        <div class="{mirror_class}">
            {mirror_message}
        </div>

    </div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# OCR INFORMATION
# ============================================================

if text.strip():

    st.markdown("### Información")

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
# TRANSLATION SETTINGS
# ============================================================

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
# TRANSLATE
# ============================================================

st.markdown("---")

translate = st.button(
    "DECIFRAR Y TRADUCIR",
    use_container_width=True
)


# ============================================================
# TRANSLATION RESULT
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


            # =================================================
            # DECIPHERED MESSAGE
            # =================================================

            st.subheader(
                "Mensaje descifrado"
            )


            output_placeholder = st.empty()

            current_text = ""


            for character in output_text:

                current_text += character

                output_placeholder.markdown(
                    f"### {current_text}"
                )

                time.sleep(0.015)


            st.success(
                "Mensaje descifrado y traducido."
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
