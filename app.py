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
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OCR TRANSLATOR",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# VARIABLES
# ============================================================

text = " "


# ============================================================
# TEXT TO SPEECH
# ============================================================

def text_to_speech(input_language, output_language, text, tld):

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

    tts.save(
        f"temp/{my_file_name}.mp3"
    )

    return my_file_name, trans_text


# ============================================================
# REMOVE OLD FILES
# ============================================================

def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) != 0:

        now = time.time()

        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)

                print("Deleted ", f)


try:
    os.mkdir("temp")
except:
    pass

remove_files(7)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

/* ============================================================
   FONTS
============================================================ */

@import url(
    'https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap'
);


/* ============================================================
   GLOBAL
============================================================ */

.stApp {

    background:
        radial-gradient(
            circle at 10% 15%,
            rgba(130, 15, 50, 0.24),
            transparent 27%
        ),

        radial-gradient(
            circle at 90% 10%,
            rgba(80, 25, 120, 0.23),
            transparent 28%
        ),

        radial-gradient(
            circle at 70% 85%,
            rgba(20, 75, 110, 0.15),
            transparent 25%
        ),

        radial-gradient(
            circle at 20% 90%,
            rgba(130, 35, 20, 0.13),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            #050407,
            #0b080d 35%,
            #08070b 70%,
            #040306
        );

    color: #eee7dc;

    overflow-x: hidden;
}


/* ============================================================
   ANIMATED LIGHT FIELD
============================================================ */

.stApp::before {

    content: "";

    position: fixed;

    width: 800px;
    height: 800px;

    top: -300px;
    left: 50%;

    transform: translateX(-50%);

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(180, 20, 70, 0.09),
            transparent 65%
        );

    filter: blur(50px);

    animation:
        lightMovement 12s ease-in-out infinite alternate;

    pointer-events: none;

    z-index: 0;
}


@keyframes lightMovement {

    0% {
        transform:
            translateX(-55%)
            scale(0.9);
    }

    100% {
        transform:
            translateX(-45%)
            scale(1.15);
    }
}


/* ============================================================
   PARTICLES
============================================================ */

.particle {

    position: fixed;

    width: 3px;
    height: 3px;

    border-radius: 50%;

    background: #c72a51;

    box-shadow:
        0 0 5px #c72a51,
        0 0 15px rgba(199,42,81,0.8),
        0 0 30px rgba(199,42,81,0.3);

    pointer-events: none;

    z-index: 1;

    animation:
        particleFloat linear infinite;
}


.particle.blue {

    background: #5d9bd3;

    box-shadow:
        0 0 5px #5d9bd3,
        0 0 15px rgba(93,155,211,0.7);
}


.particle.white {

    background: #e3ddd2;

    box-shadow:
        0 0 5px #e3ddd2,
        0 0 12px rgba(255,255,255,0.5);
}


@keyframes particleFloat {

    0% {

        transform:
            translateY(110vh)
            translateX(0)
            scale(0);

        opacity: 0;
    }

    10% {

        opacity: 0.8;

        transform:
            scale(1);
    }

    35% {

        transform:
            translateY(70vh)
            translateX(35px);
    }

    65% {

        transform:
            translateY(35vh)
            translateX(-30px);
    }

    90% {

        opacity: 0.7;
    }

    100% {

        transform:
            translateY(-10vh)
            translateX(50px)
            scale(0);

        opacity: 0;
    }
}


/* ============================================================
   MAIN
============================================================ */

.block-container {

    max-width: 1350px;

    padding-top: 2.5rem;
    padding-bottom: 6rem;

    position: relative;

    z-index: 5;
}


/* ============================================================
   TITLE
============================================================ */

h1 {

    font-family:
        "Cinzel",
        serif !important;

    font-size:
        clamp(3rem, 7vw, 7rem) !important;

    font-weight:
        700 !important;

    letter-spacing:
        0.12em;

    text-align:
        center;

    color:
        #eee7dc !important;

    line-height:
        0.95 !important;

    text-shadow:

        0 0 4px rgba(255,255,255,0.5),

        0 0 12px rgba(190,30,70,0.7),

        0 0 35px rgba(130,15,60,0.55),

        0 0 80px rgba(90,20,120,0.35);

    animation:
        titlePulse 5s ease-in-out infinite;
}


@keyframes titlePulse {

    0%, 100% {

        text-shadow:

            0 0 4px rgba(255,255,255,0.5),

            0 0 12px rgba(190,30,70,0.7),

            0 0 35px rgba(130,15,60,0.55),

            0 0 80px rgba(90,20,120,0.35);
    }

    50% {

        text-shadow:

            0 0 6px rgba(255,255,255,0.8),

            0 0 20px rgba(220,40,80,0.9),

            0 0 50px rgba(160,20,80,0.7),

            0 0 100px rgba(100,30,150,0.4);
    }
}


.header-subtitle {

    text-align:
        center;

    font-size:
        0.75rem;

    letter-spacing:
        0.5em;

    text-transform:
        uppercase;

    color:
        #8e8780;

    margin-top:
        1rem;

    margin-bottom:
        2.5rem;
}


/* ============================================================
   ORNAMENT
============================================================ */

.ornament {

    display:
        flex;

    align-items:
        center;

    gap:
        20px;

    margin:
        25px 0 35px 0;
}


.ornament-line {

    height:
        1px;

    flex:
        1;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(180,35,65,0.6)
        );
}


.ornament-line.right {

    background:
        linear-gradient(
            90deg,
            rgba(180,35,65,0.6),
            transparent
        );
}


.ornament-symbol {

    color:
        #c12a4d;

    font-size:
        1.3rem;

    text-shadow:
        0 0 15px rgba(200,30,70,0.7);
}


/* ============================================================
   PANELS
============================================================ */

.panel {

    background:

        linear-gradient(
            135deg,
            rgba(22,17,23,0.92),
            rgba(8,7,11,0.94)
        );

    border:
        1px solid rgba(210,200,190,0.10);

    box-shadow:

        0 25px 80px rgba(0,0,0,0.45),

        inset 0 0 40px rgba(150,20,55,0.025);

    position:
        relative;

    overflow:
        hidden;

    transition:
        transform 0.4s ease,
        border-color 0.4s ease,
        box-shadow 0.4s ease;
}


.panel:hover {

    transform:
        translateY(-4px);

    border-color:
        rgba(170,35,65,0.28);

    box-shadow:

        0 30px 90px rgba(0,0,0,0.55),

        0 0 40px rgba(120,20,50,0.07);
}


.panel::before {

    content:
        "";

    position:
        absolute;

    top:
        0;

    left:
        0;

    right:
        0;

    height:
        2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #9d2342,
            #d03b60,
            transparent
        );

    opacity:
        0.8;
}


/* ============================================================
   SECTION LABEL
============================================================ */

.section-label {

    font-family:
        "Cinzel",
        serif;

    font-size:
        0.72rem;

    font-weight:
        600;

    letter-spacing:
        0.25em;

    text-transform:
        uppercase;

    color:
        #a99f95;

    margin-bottom:
        0.8rem;
}


/* ============================================================
   CAMERA
============================================================ */

[data-testid="stCameraInput"] {

    background:
        #08070a;

    border:
        1px solid rgba(210,200,190,0.12);

    padding:
        15px;

    box-shadow:
        0 25px 70px rgba(0,0,0,0.45);

    transition:
        all 0.35s ease;
}


[data-testid="stCameraInput"]:hover {

    border-color:
        rgba(190,35,65,0.55);

    box-shadow:

        0 30px 90px rgba(0,0,0,0.55),

        0 0 40px rgba(150,20,55,0.12);
}


/* ============================================================
   CAMERA BUTTON
============================================================ */

[data-testid="stCameraInput"] button {

    background:
        linear-gradient(
            135deg,
            #161016,
            #251019
        ) !important;

    color:
        #e5ded4 !important;

    border:
        1px solid rgba(190,35,65,0.45) !important;

    border-radius:
        3px !important;

    transition:
        all 0.25s ease !important;
}


[data-testid="stCameraInput"] button:hover {

    background:
        linear-gradient(
            135deg,
            #241019,
            #3c1221
        ) !important;

    border-color:
        #c52b50 !important;

    box-shadow:
        0 0 25px rgba(190,30,65,0.25);

    transform:
        translateY(-2px);
}


/* ============================================================
   FILE UPLOADER
============================================================ */

[data-testid="stFileUploader"] {

    background:
        rgba(14,11,15,0.75);

    border:
        1px solid rgba(210,200,190,0.10);

    padding:
        20px;

    transition:
        all 0.3s ease;
}


[data-testid="stFileUploader"]:hover {

    border-color:
        rgba(180,35,65,0.4);

    background:
        rgba(25,14,20,0.8);
}


/* ============================================================
   CHECKBOX
============================================================ */

[data-testid="stCheckbox"] label {

    color:
        #aaa29a !important;

    transition:
        color 0.2s ease;
}


[data-testid="stCheckbox"] label:hover {

    color:
        #d8d0c5 !important;
}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {

    background:

        radial-gradient(
            circle at 50% 0%,
            rgba(120,20,50,0.13),
            transparent 35%
        ),

        linear-gradient(
            180deg,
            #070608,
            #0d090d
        );

    border-right:
        1px solid rgba(210,200,190,0.09);

    box-shadow:
        15px 0 60px rgba(0,0,0,0.55);
}


section[data-testid="stSidebar"] h3 {

    font-family:
        "Cinzel",
        serif !important;

    font-size:
        1.4rem !important;

    letter-spacing:
        0.08em;

    color:
        #ddd5ca !important;
}


section[data-testid="stSidebar"] label {

    color:
        #aaa29a !important;
}


/* ============================================================
   SELECTBOX
============================================================ */

div[data-baseweb="select"] > div {

    background:
        #0e0b0f !important;

    border:
        1px solid rgba(190,180,170,0.15) !important;

    border-radius:
        3px !important;

    color:
        #ddd6cc !important;

    transition:
        all 0.25s ease;
}


div[data-baseweb="select"] > div:hover {

    border-color:
        rgba(190,35,65,0.65) !important;

    box-shadow:
        0 0 20px rgba(150,20,50,0.1);
}


/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {

    width:
        100%;

    min-height:
        52px;

    border-radius:
        3px;

    border:
        1px solid rgba(190,35,65,0.55);

    background:

        linear-gradient(
            135deg,
            rgba(80,15,35,0.8),
            rgba(30,10,20,0.9)
        );

    color:
        #eee7dc;

    font-family:
        "Cinzel",
        serif;

    font-size:
        0.75rem;

    font-weight:
        600;

    letter-spacing:
        0.18em;

    box-shadow:
        0 0 15px rgba(150,20,50,0.08);

    transition:
        all 0.25s cubic-bezier(.2,.8,.2,1);
}


.stButton > button:hover {

    transform:
        translateY(-4px);

    border-color:
        #d13a5d;

    background:

        linear-gradient(
            135deg,
            rgba(130,20,50,0.9),
            rgba(55,12,30,0.95)
        );

    box-shadow:

        0 0 20px rgba(190,30,65,0.25),

        0 0 50px rgba(120,20,60,0.12);
}


.stButton > button:active {

    transform:
        scale(0.97);
}


/* ============================================================
   RESULT
============================================================ */

.result-panel {

    padding:
        30px;

    background:
        linear-gradient(
            135deg,
            rgba(18,14,19,0.95),
            rgba(7,6,9,0.98)
        );

    border:
        1px solid rgba(200,190,180,0.10);

    border-left:
        3px solid #8d2741;

    box-shadow:
        0 25px 70px rgba(0,0,0,0.4);

    position:
        relative;

    overflow:
        hidden;
}


.result-panel::after {

    content:
        "";

    position:
        absolute;

    width:
        250px;

    height:
        250px;

    right:
        -150px;

    top:
        -150px;

    border-radius:
        50%;

    background:
        radial-gradient(
            circle,
            rgba(150,20,55,0.15),
            transparent 70%
        );

    filter:
        blur(10px);
}


.result-text {

    font-family:
        "Cormorant Garamond",
        serif;

    font-size:
        1.45rem;

    line-height:
        1.65;

    color:
        #ddd5ca;

    white-space:
        pre-wrap;

}


/* ============================================================
   INFO CARDS
============================================================ */

.info-card {

    padding:
        25px 15px;

    text-align:
        center;

    background:
        linear-gradient(
            145deg,
            rgba(22,17,22,0.9),
            rgba(9,8,11,0.95)
        );

    border:
        1px solid rgba(190,180,170,0.08);

    transition:
        all 0.3s ease;
}


.info-card:hover {

    transform:
        translateY(-5px);

    border-color:
        rgba(170,30,60,0.35);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.35);
}


.info-number {

    font-family:
        "Cinzel",
        serif;

    font-size:
        1.7rem;

    color:
        #d3cbc0;

}


.info-label {

    margin-top:
        5px;

    font-size:
        0.58rem;

    letter-spacing:
        0.2em;

    text-transform:
        uppercase;

    color:
        #726b64;

}


/* ============================================================
   STATUS
============================================================ */

.status {

    display:
        flex;

    align-items:
        center;

    gap:
        10px;

    font-size:
        0.65rem;

    letter-spacing:
        0.18em;

    text-transform:
        uppercase;

    color:
        #857d75;

}


.status-dot {

    width:
        7px;

    height:
        7px;

    border-radius:
        50%;

    background:
        #b72b4d;

    box-shadow:
        0 0 12px rgba(190,35,70,0.8);

    animation:
        statusPulse 1.8s infinite;
}


@keyframes statusPulse {

    0%, 100% {
        opacity: 0.55;
        transform: scale(0.8);
    }

    50% {
        opacity: 1;
        transform: scale(1.15);
    }
}


/* ============================================================
   IMAGE
============================================================ */

[data-testid="stImage"] img {

    border:
        1px solid rgba(190,180,170,0.12);

    box-shadow:
        0 25px 80px rgba(0,0,0,0.5);

    transition:
        all 0.4s ease;
}


[data-testid="stImage"] img:hover {

    transform:
        scale(1.015);

    border-color:
        rgba(180,35,65,0.4);

    box-shadow:

        0 30px 90px rgba(0,0,0,0.6),

        0 0 35px rgba(130,20,50,0.12);
}


/* ============================================================
   AUDIO
============================================================ */

audio {

    width:
        100%;

    border-radius:
        3px;

    filter:
        drop-shadow(
            0 0 15px rgba(160,30,60,0.18)
        );
}


/* ============================================================
   DIVIDERS
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
            rgba(170,30,60,0.4),
            rgba(210,200,190,0.12),
            rgba(170,30,60,0.4),
            transparent
        ) !important;

    margin:
        35px 0 !important;
}


/* ============================================================
   RESPONSIVE
============================================================ */

@media (max-width: 768px) {

    .block-container {

        padding-left:
            1rem;

        padding-right:
            1rem;
    }

    h1 {

        font-size:
            3.3rem !important;

        letter-spacing:
            0.06em;
    }

    .header-subtitle {

        font-size:
            0.55rem;

        letter-spacing:
            0.25em;
    }

    .result-panel {

        padding:
            20px;
    }

    .result-text {

        font-size:
            1.2rem;
    }

}

</style>


<!-- ============================================================
     PARTICLES
============================================================ -->

<div class="particle"
     style="left:3%; animation-duration:18s; animation-delay:-4s;"></div>

<div class="particle"
     style="left:8%; animation-duration:14s; animation-delay:-9s;"></div>

<div class="particle blue"
     style="left:15%; animation-duration:22s; animation-delay:-15s;"></div>

<div class="particle"
     style="left:22%; animation-duration:17s; animation-delay:-6s;"></div>

<div class="particle white"
     style="left:29%; animation-duration:25s; animation-delay:-20s;"></div>

<div class="particle"
     style="left:36%; animation-duration:15s; animation-delay:-2s;"></div>

<div class="particle blue"
     style="left:44%; animation-duration:20s; animation-delay:-13s;"></div>

<div class="particle"
     style="left:52%; animation-duration:16s; animation-delay:-7s;"></div>

<div class="particle white"
     style="left:60%; animation-duration:23s; animation-delay:-18s;"></div>

<div class="particle"
     style="left:67%; animation-duration:19s; animation-delay:-5s;"></div>

<div class="particle blue"
     style="left:74%; animation-duration:14s; animation-delay:-10s;"></div>

<div class="particle"
     style="left:81%; animation-duration:21s; animation-delay:-16s;"></div>

<div class="particle white"
     style="left:88%; animation-duration:17s; animation-delay:-3s;"></div>

<div class="particle"
     style="left:95%; animation-duration:24s; animation-delay:-19s;"></div>

""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.title("OCR")

st.markdown(
    '<div class="header-subtitle">Reconocimiento óptico · Traducción · Síntesis de voz</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="ornament">

    <div class="ornament-line"></div>

    <div class="ornament-symbol">✦</div>

    <div class="ornament-line right"></div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SOURCE SELECTION
# ============================================================

st.markdown(
    '<div class="section-label">01 · Fuente de imagen</div>',
    unsafe_allow_html=True
)

cam_ = st.checkbox(
    "Usar Cámara"
)


if cam_:

    img_file_buffer = st.camera_input(
        "Toma una Foto"
    )

else:

    img_file_buffer = None


# ============================================================
# SIDEBAR · IMAGE PROCESSING
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="section-label">Procesamiento de imagen</div>',
        unsafe_allow_html=True
    )

    filtro = st.radio(
        "Filtro para imagen con cámara",
        (
            "Sí",
            "No"
        )
    )


# ============================================================
# FILE UPLOADER
# ============================================================

st.markdown(
    '<div class="section-label">Carga directa</div>',
    unsafe_allow_html=True
)

bg_image = st.file_uploader(
    "Cargar Imagen:",
    type=[
        "png",
        "jpg"
    ]
)


# ============================================================
# UPLOADED IMAGE OCR
# ============================================================

if bg_image is not None:

    uploaded_file = bg_image

    st.image(
        uploaded_file,
        caption="Imagen cargada.",
        use_container_width=True
    )

    # Save image exactly as in the original workflow

    with open(
        uploaded_file.name,
        "wb"
    ) as f:

        f.write(
            uploaded_file.read()
        )


    st.success(
        f"Imagen guardada como {uploaded_file.name}"
    )


    img_cv = cv2.imread(
        f"{uploaded_file.name}"
    )


    img_rgb = cv2.cvtColor(
        img_cv,
        cv2.COLOR_BGR2RGB
    )


    text = pytesseract.image_to_string(
        img_rgb
    )


# ============================================================
# CAMERA OCR
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


    # Fixed original condition:
    # radio returns "Sí" / "No"

    if filtro == "Sí":

        cv2_img = cv2.bitwise_not(
            cv2_img
        )

    else:

        cv2_img = cv2_img


    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )


    text = pytesseract.image_to_string(
        img_rgb
    )


# ============================================================
# OCR OUTPUT
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-label">02 · Texto reconocido</div>',
    unsafe_allow_html=True
)


clean_text = text.strip()

character_count = len(clean_text)

word_count = len(
    clean_text.split()
)


if character_count > 0:

    status_text = "Texto detectado"

else:

    status_text = "Esperando una imagen"


st.markdown(
    f"""
    <div class="status">

        <div class="status-dot"></div>

        <span>{status_text}</span>

    </div>
    """,
    unsafe_allow_html=True
)


# Escape HTML from OCR result

safe_text = (
    text
    .replace("&", "&amp;")
    .replace("<", "&lt;")
    .replace(">", "&gt;")
)


if clean_text:

    display_text = safe_text

else:

    display_text = "No se ha reconocido ningún texto."


st.markdown(
    f"""
    <div class="result-panel">

        <div class="result-text">
            {display_text}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OCR STATISTICS
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-number">
                {word_count}
            </div>

            <div class="info-label">
                Palabras
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-number">
                {character_count}
            </div>

            <div class="info-label">
                Caracteres
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    processing = (
        "Filtro"
        if filtro == "Sí"
        else "Original"
    )

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-number">
                {processing}
            </div>

            <div class="info-label">
                Procesamiento
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TRANSLATION PANEL
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-label">03 · Traducción y audio</div>',
    unsafe_allow_html=True
)


with st.sidebar:

    st.markdown("---")

    st.markdown(
        '<div class="section-label">Parámetros de traducción</div>',
        unsafe_allow_html=True
    )


    translator = Translator()


    # ========================================================
    # INPUT LANGUAGE
    # ========================================================

    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        (
            "Ingles",
            "Español",
            "Bengali",
            "koreano",
            "Mandarin",
            "Japones"
        ),
    )


    if in_lang == "Ingles":

        input_language = "en"

    elif in_lang == "Español":

        input_language = "es"

    elif in_lang == "Bengali":

        input_language = "bn"

    elif in_lang == "koreano":

        input_language = "ko"

    elif in_lang == "Mandarin":

        input_language = "zh-cn"

    elif in_lang == "Japones":

        input_language = "ja"


    # ========================================================
    # OUTPUT LANGUAGE
    # ========================================================

    out_lang = st.selectbox(
        "Select your output language",
        (
            "Ingles",
            "Español",
            "Bengali",
            "koreano",
            "Mandarin",
            "Japones"
        ),
    )


    if out_lang == "Ingles":

        output_language = "en"

    elif out_lang == "Español":

        output_language = "es"

    elif out_lang == "Bengali":

        output_language = "bn"

    elif out_lang == "koreano":

        output_language = "ko"

    elif out_lang == "Mandarin":

        output_language = "zh-cn"

    elif out_lang == "Japones":

        output_language = "ja"


    # ========================================================
    # ACCENT
    # ========================================================

    english_accent = st.selectbox(
        "Seleccione el acento",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
    )


    if english_accent == "Default":

        tld = "com"

    elif english_accent == "India":

        tld = "co.in"

    elif english_accent == "United Kingdom":

        tld = "co.uk"

    elif english_accent == "United States":

        tld = "com"

    elif english_accent == "Canada":

        tld = "ca"

    elif english_accent == "Australia":

        tld = "com.au"

    elif english_accent == "Ireland":

        tld = "ie"

    elif english_accent == "South Africa":

        tld = "co.za"


# ============================================================
# AUDIO CONTROLS
# ============================================================

display_output_text = st.checkbox(
    "Mostrar texto traducido"
)


if st.button("CONVERTIR Y REPRODUCIR"):

    if not clean_text:

        st.warning(
            "Primero debes proporcionar una imagen con texto reconocible."
        )

    else:

        result, output_text = text_to_speech(
            input_language,
            output_language,
            text,
            tld
        )


        audio_file = open(
            f"temp/{result}.mp3",
            "rb"
        )


        audio_bytes = audio_file.read()


        st.markdown(
            """
            <div class="status">

                <div class="status-dot"></div>

                <span>Audio generado correctamente</span>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )


        if display_output_text:

            st.markdown(
                """
                <br>
                <div class="section-label">
                    Texto traducido
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="result-panel">

                    <div class="result-text">
                        {output_text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )
