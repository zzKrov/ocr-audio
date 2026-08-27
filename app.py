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
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Espejo Mágico",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


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

def text_to_speech(input_language, output_language, text, tld):

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

    filename = text[:20]

    filename = "".join(
        c for c in filename
        if c.isalnum() or c in (" ", "_", "-")
    ).strip()

    if not filename:
        filename = "audio"

    # Avoid problematic path characters
    filename = filename.replace("/", "_")
    filename = filename.replace("\\", "_")

    filepath = f"temp/{filename}.mp3"

    tts.save(filepath)

    return filename, trans_text


# ============================================================
# MAIN PAGE VISUAL STYLE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 15% 20%,
                rgba(90, 45, 170, 0.25),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 25%,
                rgba(40, 90, 180, 0.20),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(150, 40, 140, 0.18),
                transparent 35%
            ),
            linear-gradient(
                125deg,
                #030207,
                #0a0613,
                #050914,
                #100711,
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

        50% {
            background-position: 100% 75%;
        }

        100% {
            background-position: 0% 50%;
        }
    }


    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }


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
            0 0 10px rgba(230,215,255,0.55),
            0 0 30px rgba(150,100,240,0.40),
            0 0 70px rgba(90,50,180,0.30);
    }


    h2,
    h3 {
        font-family:
            Georgia,
            "Times New Roman",
            serif !important;

        color: #ddd5c9 !important;
    }


    [data-testid="stAlert"] {
        background:
            rgba(10,8,17,0.80) !important;

        border:
            1px solid rgba(175,145,220,0.25) !important;
    }


    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #050409,
                #0b0711
            );

        border-right:
            1px solid rgba(175,145,210,0.15);
    }


    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(22,15,34,0.90),
                rgba(6,5,11,0.94)
            );

        border:
            1px solid rgba(175,145,220,0.22);

        border-radius: 10px;

        box-shadow:
            inset 0 0 35px rgba(130,80,200,0.06),
            0 15px 55px rgba(0,0,0,0.40);

        transition:
            transform 0.25s ease,
            border-color 0.25s ease,
            box-shadow 0.25s ease;
    }


    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform:
            translateY(-5px);

        border-color:
            rgba(210,180,245,0.60);

        box-shadow:
            inset 0 0 45px rgba(140,90,220,0.10),
            0 20px 70px rgba(90,45,170,0.30);
    }


    .stButton > button {
        width: 100%;

        min-height: 55px;

        border-radius: 5px;

        border:
            1px solid rgba(180,145,225,0.60);

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

        letter-spacing: 0.12em;

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
            0 0 25px rgba(170,120,245,0.40),
            0 0 70px rgba(100,60,190,0.20);
    }


    [data-testid="stFileUploader"] {
        background:
            rgba(7,6,12,0.65);

        border:
            1px dashed rgba(170,140,215,0.35);

        border-radius: 7px;

        transition:
            all 0.3s ease;
    }


    [data-testid="stFileUploader"]:hover {
        border-color:
            rgba(210,180,245,0.75);

        box-shadow:
            0 0 35px rgba(120,70,200,0.20);
    }


    [data-testid="stImage"] img {
        border-radius: 8px;

        box-shadow:
            0 0 25px rgba(130,80,210,0.18),
            0 20px 55px rgba(0,0,0,0.50);
    }


    div[data-baseweb="select"] > div {
        background:
            rgba(9,7,14,0.95) !important;

        border:
            1px solid rgba(175,145,215,0.22) !important;
    }


    div[data-baseweb="select"] > div:hover {
        border-color:
            rgba(205,175,245,0.65) !important;
    }


    audio {
        width: 100%;
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
    
    **3. Selecciona los idiomas.**
    
    **4. Pulsa «DECIFRAR Y TRADUCIR».**
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

        st.write("Fotografía el mensaje.")

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

        st.write("Carga una imagen.")

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
# SIDEBAR PROCESSING
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


if bg_image is not None:

    img_bytes = bg_image.getvalue()

    img_cv = cv2.imdecode(
        np.frombuffer(
            img_bytes,
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )

    if img_cv is not None:

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

    if cv2_img is not None:

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
# MIRROR TEXT
# ============================================================

if text.strip():

    mirror_text = html.escape(
        text.strip()
    )

    mirror_label = "MENSAJE DETECTADO"

else:

    mirror_text = (
        "Introduce una imagen para comenzar."
    )

    mirror_label = "ESPERANDO MENSAJE"


# ============================================================
# MAGIC MIRROR
#
# IMPORTANT:
# The HTML is rendered inside an isolated Streamlit
# component. Nothing from this block is rendered as
# visible source code on the main Streamlit page.
# ============================================================

mirror_html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

* {{
    box-sizing: border-box;
}}

html,
body {{

    margin: 0;

    padding: 0;

    width: 100%;

    height: 100%;

    overflow: hidden;

    background: transparent;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

}}


/* ============================================================
   MIRROR
   ============================================================ */

.magic-mirror {{

    position: relative;

    width: 100%;

    height: 620px;

    overflow: hidden;

    border-radius: 20px;

    background:

        radial-gradient(
            ellipse at 50% 50%,
            rgba(95,60,150,0.34),
            rgba(12,8,22,0.98) 67%
        );

    border:
        1px solid
        rgba(195,170,235,0.45);

    box-shadow:

        0 0 20px
        rgba(145,95,225,0.35),

        0 0 80px
        rgba(105,60,190,0.25),

        inset 0 0 90px
        rgba(100,65,160,0.30);

    transform:
        translate3d(0,0,0);

    transition:
        transform 0.15s ease-out;

}}


/* ============================================================
   INTERNAL BLOOM
   ============================================================ */

.bloom {{

    position: absolute;

    width: 70%;

    height: 70%;

    left: 15%;

    top: 15%;

    border-radius: 50%;

    background:

        radial-gradient(
            ellipse,
            rgba(210,190,255,0.16),
            rgba(125,80,210,0.10) 35%,
            transparent 70%
        );

    filter:
        blur(25px);

    animation:
        bloomPulse 5s ease-in-out infinite;

    pointer-events: none;

}}


@keyframes bloomPulse {{

    0% {{
        transform: scale(0.90);
        opacity: 0.55;
    }}

    50% {{
        transform: scale(1.10);
        opacity: 1;
    }}

    100% {{
        transform: scale(0.90);
        opacity: 0.55;
    }}

}}


/* ============================================================
   MOVING LIGHT
   ============================================================ */

.mirror-light {{

    position: absolute;

    width: 280px;

    height: 280px;

    border-radius: 50%;

    background:

        radial-gradient(
            circle,
            rgba(235,220,255,0.20),
            rgba(140,95,230,0.09),
            transparent 70%
        );

    filter:
        blur(12px);

    pointer-events: none;

    transition:
        left 0.25s ease-out,
        top 0.25s ease-out;

}}


/* ============================================================
   PARTICLE FIELD
   ============================================================ */

.magic-particles {{

    position: absolute;

    inset: 0;

    overflow: hidden;

    pointer-events: none;

}}


/* ============================================================
   PARTICLES
   ============================================================ */

.magic-particle {{

    position: absolute;

    width: var(--size);

    height: var(--size);

    border-radius: 50%;

    background:
        rgba(225,215,255,0.90);

    box-shadow:
        0 0 8px
        rgba(190,160,255,0.85);

    opacity: 0;

    animation:
        particleMove
        var(--duration)
        ease-in-out
        var(--delay)
        infinite;

}}


@keyframes particleMove {{

    0% {{

        transform:
            translate3d(
                0,
                70px,
                0
            )
            scale(0.25);

        opacity: 0;

    }}

    12% {{
        opacity: 0.8;
    }}

    50% {{

        transform:
            translate3d(
                var(--drift),
                -190px,
                0
            )
            scale(1);

        opacity: 1;

    }}

    80% {{
        opacity: 0.55;
    }}

    100% {{

        transform:
            translate3d(
                var(--drift2),
                -470px,
                0
            )
            scale(0.15);

        opacity: 0;

    }}

}}


/* ============================================================
   SECONDARY PARTICLES
   ============================================================ */

.spark {{

    position: absolute;

    width: 2px;

    height: 2px;

    border-radius: 50%;

    background:
        white;

    box-shadow:
        0 0 10px
        rgba(225,215,255,0.95);

    animation:
        sparkPulse
        var(--duration)
        ease-in-out
        var(--delay)
        infinite;

}}


@keyframes sparkPulse {{

    0%,
    100% {{
        opacity: 0;
        transform: scale(0.3);
    }}

    50% {{
        opacity: 1;
        transform: scale(1.7);
    }}

}}


/* ============================================================
   SCANNING BEAM
   ============================================================ */

.scan-beam {{

    position: absolute;

    left: 4%;

    right: 4%;

    height: 2px;

    background:

        linear-gradient(
            90deg,
            transparent,
            rgba(230,215,255,0.90),
            transparent
        );

    box-shadow:

        0 0 12px
        rgba(210,185,255,0.95),

        0 0 45px
        rgba(140,90,230,0.75);

    opacity: 0.7;

    animation:
        scanning 4.5s linear infinite;

}}


@keyframes scanning {{

    0% {{
        top: 10%;
        opacity: 0;
    }}

    10% {{
        opacity: 0.85;
    }}

    90% {{
        opacity: 0.85;
    }}

    100% {{
        top: 90%;
        opacity: 0;
    }}

}}


/* ============================================================
   MIRROR CONTENT
   ============================================================ */

.mirror-content {{

    position: absolute;

    inset: 0;

    z-index: 10;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    padding: 60px;

    text-align: center;

    pointer-events: none;

}}


.mirror-label {{

    margin-bottom: 28px;

    font-size: 0.72rem;

    letter-spacing: 0.34em;

    color:
        rgba(210,195,230,0.68);

    text-transform:
        uppercase;

}}


.mirror-message {{

    max-width: 900px;

    max-height: 390px;

    overflow: auto;

    font-size:
        clamp(1.35rem, 3vw, 2.6rem);

    line-height: 1.5;

    color:
        #eee8f5;

    text-shadow:

        0 0 8px
        rgba(230,215,255,0.55),

        0 0 25px
        rgba(150,105,230,0.45),

        0 0 60px
        rgba(100,60,190,0.30);

    animation:
        messageAppear 1.5s ease forwards;

}}


@keyframes messageAppear {{

    0% {{

        opacity: 0;

        transform:
            scale(0.92);

        filter:
            blur(15px);

    }}

    50% {{

        opacity: 0.75;

        filter:
            blur(4px);

    }}

    100% {{

        opacity: 1;

        transform:
            scale(1);

        filter:
            blur(0);

    }}

}}


/* ============================================================
   FRAME
   ============================================================ */

.frame {{

    position: absolute;

    inset: 14px;

    border:
        1px solid
        rgba(210,190,240,0.16);

    border-radius:
        14px;

    pointer-events: none;

    z-index: 20;

}}


.frame::before,
.frame::after {{

    content: "";

    position: absolute;

    width: 55px;

    height: 55px;

    border-color:
        rgba(215,195,245,0.55);

}}


.frame::before {{

    top: -1px;

    left: -1px;

    border-top: 2px solid;

    border-left: 2px solid;

}}


.frame::after {{

    bottom: -1px;

    right: -1px;

    border-bottom: 2px solid;

    border-right: 2px solid;

}}


/* ============================================================
   CURSOR GLOW
   ============================================================ */

.cursor-glow {{

    position: absolute;

    width: 180px;

    height: 180px;

    border-radius: 50%;

    background:

        radial-gradient(
            circle,
            rgba(210,190,255,0.14),
            transparent 70%
        );

    transform:
        translate(-50%, -50%);

    pointer-events: none;

    z-index: 3;

    transition:
        left 0.08s linear,
        top 0.08s linear;

}}


@media (max-width: 700px) {{

    .magic-mirror {{
        height: 500px;
    }}

    .mirror-content {{
        padding: 30px;
    }}

}}

</style>

</head>


<body>

<div class="magic-mirror">

    <div class="bloom"></div>

    <div class="mirror-light"></div>

    <div class="magic-particles"></div>

    <div class="cursor-glow"></div>

    <div class="scan-beam"></div>

    <div class="frame"></div>

    <div class="mirror-content">

        <div class="mirror-label">
            {html.escape(mirror_label)}
        </div>

        <div class="mirror-message">
            {mirror_text}
        </div>

    </div>

</div>


<script>

/* ============================================================
   PARTICLE GENERATOR
   ============================================================ */

const particleContainer =
    document.querySelector(".magic-particles");


for (let i = 0; i < 85; i++) {{

    const particle =
        document.createElement("span");

    particle.className =
        "magic-particle";

    particle.style.left =
        Math.random() * 100 + "%";

    particle.style.bottom =
        Math.random() * 65 + "%";

    particle.style.setProperty(
        "--size",
        (1 + Math.random() * 3) + "px"
    );

    particle.style.setProperty(
        "--duration",
        (9 + Math.random() * 18) + "s"
    );

    particle.style.setProperty(
        "--delay",
        (-Math.random() * 20) + "s"
    );

    particle.style.setProperty(
        "--drift",
        (-100 + Math.random() * 200) + "px"
    );

    particle.style.setProperty(
        "--drift2",
        (-150 + Math.random() * 300) + "px"
    );

    particleContainer.appendChild(
        particle
    );
}}


/* ============================================================
   SPARK GENERATOR
   ============================================================ */

for (let i = 0; i < 35; i++) {{

    const spark =
        document.createElement("span");

    spark.className =
        "spark";

    spark.style.left =
        Math.random() * 100 + "%";

    spark.style.top =
        Math.random() * 100 + "%";

    spark.style.setProperty(
        "--duration",
        (2 + Math.random() * 5) + "s"
    );

    spark.style.setProperty(
        "--delay",
        (-Math.random() * 6) + "s"
    );

    particleContainer.appendChild(
        spark
    );
}}


/* ============================================================
   MOUSE TRACKING
   ============================================================ */

const mirror =
    document.querySelector(".magic-mirror");

const light =
    document.querySelector(".mirror-light");

const glow =
    document.querySelector(".cursor-glow");


mirror.addEventListener(
    "mousemove",
    function(event) {{

        const rect =
            mirror.getBoundingClientRect();

        const x =
            event.clientX - rect.left;

        const y =
            event.clientY - rect.top;

        const centerX =
            rect.width / 2;

        const centerY =
            rect.height / 2;

        const rotateX =
            ((y - centerY) / centerY) * -1.5;

        const rotateY =
            ((x - centerX) / centerX) * 1.5;

        mirror.style.transform =
            `perspective(1200px)
             rotateX(${{rotateX}}deg)
             rotateY(${{rotateY}}deg)
             scale(1.005)`;


        light.style.left =
            (x - 140) + "px";

        light.style.top =
            (y - 140) + "px";


        glow.style.left =
            x + "px";

        glow.style.top =
            y + "px";

    }}
);


mirror.addEventListener(
    "mouseleave",
    function() {{

        mirror.style.transform =
            "perspective(1200px) rotateX(0deg) rotateY(0deg) scale(1)";

        light.style.left =
            "50%";

        light.style.top =
            "50%";

        glow.style.left =
            "50%";

        glow.style.top =
            "50%";

    }}
);

</script>

</body>

</html>
"""


components.html(
    mirror_html,
    height=650,
    scrolling=False
)


# ============================================================
# OCR INFORMATION
# ============================================================

if text.strip():

    st.markdown("### Texto reconocido")

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
# TRANSLATION BUTTON
# ============================================================

st.markdown("---")

translate_button = st.button(
    "DECIFRAR Y TRADUCIR",
    use_container_width=True
)


# ============================================================
# TRANSLATION
# ============================================================

if translate_button:

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


            # ================================================
            # TRANSLATED MESSAGE
            # ================================================

            st.subheader(
                "Mensaje descifrado"
            )

            output_placeholder = st.empty()

            current_text = ""

            for character in output_text:

                current_text += character

                output_placeholder.markdown(
                    f"### {html.escape(current_text)}"
                )

                time.sleep(0.015)


            st.success(
                "Mensaje descifrado y traducido."
            )


            # ================================================
            # AUDIO
            # ================================================

            st.subheader(
                "Traducción de audio"
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
