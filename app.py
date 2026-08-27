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
    page_title="The Magic Mirror",
    page_icon="◈",
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
# REMOVE OLD AUDIO FILES
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
# VISUAL SYSTEM
#
# IMPORTANT:
# The animated mirror is contained inside ONE markdown block.
# There are no standalone HTML fragments in the Streamlit body.
# ============================================================

st.markdown("""
<style>

/* ------------------------------------------------------------
   FONTS
------------------------------------------------------------ */

@import url(
    'https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap'
);


/* ------------------------------------------------------------
   GLOBAL BACKGROUND
------------------------------------------------------------ */

.stApp {

    background:
        radial-gradient(
            circle at 50% 15%,
            rgba(75, 42, 120, 0.22),
            transparent 28%
        ),
        radial-gradient(
            circle at 15% 70%,
            rgba(25, 75, 110, 0.14),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 60%,
            rgba(110, 35, 80, 0.15),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #040308,
            #080611,
            #05040a
        );

    color: #e8e2d8;
}


/* ------------------------------------------------------------
   REMOVE DEFAULT STREAMLIT TOP SPACE
------------------------------------------------------------ */

.block-container {

    max-width: 1350px;

    padding-top: 2rem;
    padding-bottom: 5rem;
}


/* ------------------------------------------------------------
   TYPOGRAPHY
------------------------------------------------------------ */

html,
body,
[class*="css"] {

    font-family:
        "Inter",
        sans-serif;
}


h1 {

    font-family:
        "Cinzel",
        serif !important;

    font-size:
        clamp(3rem, 7vw, 6.5rem) !important;

    font-weight:
        600 !important;

    letter-spacing:
        0.12em;

    text-align:
        center;

    color:
        #eee8dd !important;

    line-height:
        1 !important;

    text-shadow:
        0 0 8px rgba(220,210,255,0.35),
        0 0 30px rgba(110,75,190,0.35),
        0 0 70px rgba(70,40,150,0.25);
}


h2,
h3 {

    font-family:
        "Cinzel",
        serif !important;

    color:
        #ded7cb !important;
}


/* ------------------------------------------------------------
   HEADER
------------------------------------------------------------ */

.mirror-subtitle {

    text-align:
        center;

    color:
        #827c91;

    font-size:
        0.68rem;

    letter-spacing:
        0.42em;

    text-transform:
        uppercase;

    margin-top:
        0.8rem;

    margin-bottom:
        2rem;
}


.mirror-divider {

    width:
        100%;

    height:
        1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(137,105,205,0.65),
            rgba(220,210,190,0.25),
            rgba(137,105,205,0.65),
            transparent
        );

    margin:
        25px 0 35px 0;
}


/* ------------------------------------------------------------
   MIRROR
------------------------------------------------------------ */

.magic-mirror {

    position:
        relative;

    width:
        min(100%, 1050px);

    min-height:
        470px;

    margin:
        0 auto 40px auto;

    padding:
        42px;

    box-sizing:
        border-box;

    border-radius:
        48% 48% 45% 45% / 18% 18% 48% 48%;

    background:

        radial-gradient(
            ellipse at 50% 45%,
            rgba(93,70,155,0.23),
            rgba(16,12,30,0.96) 48%,
            rgba(4,4,9,0.99) 75%
        );

    border:
        4px solid rgba(155,130,190,0.55);

    box-shadow:

        inset 0 0 40px rgba(170,130,255,0.10),

        inset 0 0 100px rgba(70,45,140,0.18),

        0 0 12px rgba(190,170,220,0.25),

        0 0 45px rgba(100,60,180,0.25),

        0 35px 100px rgba(0,0,0,0.7);

    overflow:
        hidden;

    transition:
        box-shadow 0.5s ease,
        transform 0.5s ease;
}


.magic-mirror:hover {

    transform:
        translateY(-3px);

    box-shadow:

        inset 0 0 50px rgba(190,150,255,0.13),

        inset 0 0 120px rgba(70,45,140,0.2),

        0 0 20px rgba(210,190,235,0.32),

        0 0 70px rgba(100,60,190,0.32),

        0 40px 120px rgba(0,0,0,0.75);
}


/* ------------------------------------------------------------
   MIRROR INNER FRAME
------------------------------------------------------------ */

.magic-mirror::before {

    content:
        "";

    position:
        absolute;

    inset:
        14px;

    border-radius:
        inherit;

    border:
        1px solid rgba(220,210,235,0.25);

    box-shadow:
        inset 0 0 20px rgba(200,180,255,0.08);

    pointer-events:
        none;
}


/* ------------------------------------------------------------
   MOVING LIGHT
------------------------------------------------------------ */

.magic-mirror::after {

    content:
        "";

    position:
        absolute;

    width:
        400px;

    height:
        400px;

    left:
        50%;

    top:
        50%;

    transform:
        translate(-50%, -50%);

    background:
        radial-gradient(
            circle,
            rgba(180,140,255,0.13),
            transparent 65%
        );

    filter:
        blur(20px);

    animation:
        mirrorPulse 5s ease-in-out infinite;

    pointer-events:
        none;
}


@keyframes mirrorPulse {

    0%, 100% {
        transform:
            translate(-50%, -50%)
            scale(0.85);

        opacity:
            0.45;
    }

    50% {
        transform:
            translate(-50%, -50%)
            scale(1.25);

        opacity:
            0.9;
    }
}


/* ------------------------------------------------------------
   PARTICLE FIELD
------------------------------------------------------------ */

.mirror-particles {

    position:
        absolute;

    inset:
        0;

    pointer-events:
        none;
}


.mirror-particles span {

    position:
        absolute;

    width:
        3px;

    height:
        3px;

    border-radius:
        50%;

    background:
        #cbb9ff;

    box-shadow:
        0 0 5px #cbb9ff,
        0 0 15px rgba(170,130,255,0.9),
        0 0 30px rgba(120,80,220,0.5);

    animation:
        particleRise var(--duration) linear infinite;

    animation-delay:
        var(--delay);

    left:
        var(--left);

    bottom:
        -10px;

    opacity:
        0;
}


.mirror-particles span:nth-child(3n) {

    background:
        #e8dfc9;

    box-shadow:
        0 0 5px #e8dfc9,
        0 0 18px rgba(240,225,190,0.65);
}


.mirror-particles span:nth-child(4n) {

    width:
        2px;

    height:
        2px;

    background:
        #7db3d8;

    box-shadow:
        0 0 10px #7db3d8;
}


@keyframes particleRise {

    0% {

        transform:
            translate3d(
                0,
                20px,
                0
            )
            scale(0);

        opacity:
            0;
    }

    10% {

        opacity:
            0.9;

        transform:
            scale(1);
    }

    40% {

        transform:
            translate3d(
                var(--drift),
                -160px,
                0
            )
            scale(1.15);
    }

    70% {

        transform:
            translate3d(
                calc(var(--drift) * -0.5),
                -330px,
                0
            )
            scale(0.8);
    }

    100% {

        transform:
            translate3d(
                var(--drift),
                -550px,
                0
            )
            scale(0);

        opacity:
            0;
    }
}


/* ------------------------------------------------------------
   MIRROR CONTENT
------------------------------------------------------------ */

.mirror-content {

    position:
        relative;

    z-index:
        10;

    min-height:
        380px;

    display:
        flex;

    flex-direction:
        column;

    justify-content:
        center;

    align-items:
        center;

    text-align:
        center;
}


.mirror-eyebrow {

    font-family:
        "Cinzel",
        serif;

    font-size:
        0.65rem;

    letter-spacing:
        0.35em;

    text-transform:
        uppercase;

    color:
        #988cae;

    margin-bottom:
        22px;
}


.mirror-message {

    max-width:
        850px;

    font-family:
        "Cinzel",
        serif;

    font-size:
        clamp(1.4rem, 3vw, 2.5rem);

    line-height:
        1.55;

    color:
        #eee8dd;

    text-shadow:
        0 0 12px rgba(200,180,255,0.3);

    white-space:
        pre-wrap;

    word-break:
        break-word;

    animation:
        messageAppear 0.9s ease both;
}


@keyframes messageAppear {

    from {

        opacity:
            0;

        transform:
            translateY(15px);

        filter:
            blur(8px);
    }

    to {

        opacity:
            1;

        transform:
            translateY(0);

        filter:
            blur(0);
    }
}


/* ------------------------------------------------------------
   DECIPHERING CURSOR
------------------------------------------------------------ */

.decipher-cursor {

    display:
        inline-block;

    width:
        2px;

    height:
        1.1em;

    margin-left:
        4px;

    vertical-align:
        middle;

    background:
        #c8b4ff;

    box-shadow:
        0 0 12px #b18cff;

    animation:
        cursorBlink 0.75s infinite;
}


@keyframes cursorBlink {

    0%, 45% {
        opacity:
            1;
    }

    46%, 100% {
        opacity:
            0;
    }
}


/* ------------------------------------------------------------
   STATUS
------------------------------------------------------------ */

.mirror-status {

    display:
        flex;

    justify-content:
        center;

    align-items:
        center;

    gap:
        10px;

    margin-top:
        25px;

    font-size:
        0.62rem;

    letter-spacing:
        0.25em;

    text-transform:
        uppercase;

    color:
        #81788d;
}


.status-orb {

    width:
        7px;

    height:
        7px;

    border-radius:
        50%;

    background:
        #a982e8;

    box-shadow:
        0 0 8px #a982e8,
        0 0 20px rgba(150,100,240,0.7);

    animation:
        orbPulse 1.5s infinite;
}


@keyframes orbPulse {

    0%, 100% {
        transform:
            scale(0.75);

        opacity:
            0.55;
    }

    50% {
        transform:
            scale(1.25);

        opacity:
            1;
    }
}


/* ------------------------------------------------------------
   NORMAL STREAMLIT PANELS
------------------------------------------------------------ */

[data-testid="stFileUploader"] {

    background:
        rgba(10,8,16,0.8);

    border:
        1px solid rgba(180,160,210,0.13);

    padding:
        18px;

    transition:
        0.3s ease;
}


[data-testid="stFileUploader"]:hover {

    border-color:
        rgba(150,110,220,0.5);

    box-shadow:
        0 0 30px rgba(110,70,190,0.10);
}


[data-testid="stCameraInput"] {

    background:
        rgba(8,7,12,0.85);

    border:
        1px solid rgba(180,160,210,0.15);

    padding:
        12px;

    transition:
        0.3s ease;
}


[data-testid="stCameraInput"]:hover {

    border-color:
        rgba(155,120,220,0.55);

    box-shadow:
        0 0 35px rgba(100,60,180,0.14);
}


/* ------------------------------------------------------------
   BUTTONS
------------------------------------------------------------ */

.stButton > button {

    width:
        100%;

    min-height:
        55px;

    border-radius:
        4px;

    border:
        1px solid rgba(170,130,225,0.5);

    background:
        linear-gradient(
            135deg,
            rgba(53,31,75,0.9),
            rgba(20,14,32,0.95)
        );

    color:
        #eee7dc;

    font-family:
        "Cinzel",
        serif;

    font-size:
        0.72rem;

    letter-spacing:
        0.18em;

    transition:
        all 0.3s ease;

    box-shadow:
        0 0 20px rgba(100,60,180,0.08);
}


.stButton > button:hover {

    transform:
        translateY(-3px);

    border-color:
        #c2a2f0;

    background:
        linear-gradient(
            135deg,
            rgba(78,45,110,0.95),
            rgba(31,18,48,0.98)
        );

    box-shadow:
        0 0 25px rgba(150,105,230,0.25),
        0 0 60px rgba(110,70,190,0.12);
}


/* ------------------------------------------------------------
   SELECTBOX
------------------------------------------------------------ */

div[data-baseweb="select"] > div {

    background:
        #0d0a13 !important;

    border:
        1px solid rgba(180,160,205,0.16) !important;

    color:
        #ddd6cb !important;

    border-radius:
        3px !important;
}


div[data-baseweb="select"] > div:hover {

    border-color:
        rgba(165,125,225,0.6) !important;
}


/* ------------------------------------------------------------
   SIDEBAR
------------------------------------------------------------ */

section[data-testid="stSidebar"] {

    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(80,50,120,0.2),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #060509,
            #0b0810
        );

    border-right:
        1px solid rgba(180,160,205,0.10);

    box-shadow:
        15px 0 70px rgba(0,0,0,0.55);
}


section[data-testid="stSidebar"] h3 {

    font-family:
        "Cinzel",
        serif !important;

    color:
        #ddd5ca !important;

    letter-spacing:
        0.08em;
}


section[data-testid="stSidebar"] label {

    color:
        #a9a0ae !important;
}


/* ------------------------------------------------------------
   AUDIO
------------------------------------------------------------ */

audio {

    width:
        100%;

    filter:
        drop-shadow(
            0 0 20px rgba(130,90,210,0.18)
        );
}


/* ------------------------------------------------------------
   DIVIDERS
------------------------------------------------------------ */

hr {

    border:
        none !important;

    height:
        1px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(150,110,210,0.4),
            transparent
        ) !important;

    margin:
        35px 0 !important;
}


/* ------------------------------------------------------------
   MOBILE
------------------------------------------------------------ */

@media (max-width: 768px) {

    .block-container {

        padding-left:
            1rem;

        padding-right:
            1rem;
    }

    h1 {

        font-size:
            3rem !important;

        letter-spacing:
            0.07em;
    }

    .magic-mirror {

        min-height:
            390px;

        padding:
            25px;

        border-radius:
            42% 42% 40% 40% / 15% 15% 42% 42%;
    }

    .mirror-content {

        min-height:
            320px;
    }

    .mirror-message {

        font-size:
            1.2rem;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.title("THE MAGIC MIRROR")

st.markdown(
    '<div class="mirror-subtitle">Recognition · Deciphering · Translation · Voice</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="mirror-divider"></div>',
    unsafe_allow_html=True
)


# ============================================================
# SOURCE
# ============================================================

st.markdown(
    "### The Mirror",
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
# SIDEBAR PROCESSING
# ============================================================

with st.sidebar:

    st.subheader(
        "Procesamiento"
    )

    filtro = st.radio(
        "Filtro para imagen con cámara",
        (
            "Sí",
            "No"
        )
    )


# ============================================================
# FILE UPLOAD
# ============================================================

bg_image = st.file_uploader(
    "Cargar Imagen:",
    type=[
        "png",
        "jpg"
    ]
)


# ============================================================
# UPLOADED IMAGE
# ============================================================

if bg_image is not None:

    uploaded_file = bg_image

    st.image(
        uploaded_file,
        caption="Imagen cargada.",
        use_container_width=True
    )

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
# MIRROR RESULT
# ============================================================

clean_text = text.strip()


if clean_text:

    mirror_message = clean_text

    mirror_status = "Message deciphered"

else:

    mirror_message = "The mirror is waiting for an image."

    mirror_status = "Awaiting input"


# Escape text so OCR content cannot become HTML

safe_text = (
    mirror_message
    .replace("&", "&amp;")
    .replace("<", "&lt;")
    .replace(">", "&gt;")
)


# ============================================================
# PARTICLE HTML
#
# This is ONE complete component.
# Nothing here is placed independently into Streamlit.
# ============================================================

particles = ""

particle_settings = [
    ("5%", "14s", "-4s", "35px"),
    ("11%", "18s", "-10s", "-40px"),
    ("17%", "21s", "-7s", "55px"),
    ("24%", "16s", "-12s", "-30px"),
    ("31%", "23s", "-19s", "45px"),
    ("38%", "17s", "-5s", "-55px"),
    ("45%", "20s", "-15s", "25px"),
    ("52%", "15s", "-8s", "-35px"),
    ("59%", "22s", "-17s", "60px"),
    ("66%", "18s", "-4s", "-45px"),
    ("73%", "24s", "-13s", "35px"),
    ("80%", "16s", "-9s", "-50px"),
    ("87%", "20s", "-18s", "45px"),
    ("93%", "15s", "-6s", "-25px"),
]

for i, (left, duration, delay, drift) in enumerate(
    particle_settings
):

    particles += f"""
        <span style="
            --left:{left};
            --duration:{duration};
            --delay:{delay};
            --drift:{drift};
        "></span>
    """


st.markdown(
    f"""
    <div class="magic-mirror">

        <div class="mirror-particles">
            {particles}
        </div>

        <div class="mirror-content">

            <div class="mirror-eyebrow">
                {mirror_status}
            </div>

            <div class="mirror-message">
                {safe_text}
                <span class="decipher-cursor"></span>
            </div>

            <div class="mirror-status">

                <span class="status-orb"></span>

                <span>
                    Optical recognition active
                </span>

            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OCR INFORMATION
# ============================================================

if clean_text:

    character_count = len(clean_text)

    word_count = len(
        clean_text.split()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Palabras",
            word_count
        )

    with col2:

        st.metric(
            "Caracteres",
            character_count
        )

    with col3:

        processing = (
            "Filtro"
            if filtro == "Sí"
            else "Original"
        )

        st.metric(
            "Procesamiento",
            processing
        )


# ============================================================
# TRANSLATION
# ============================================================

st.markdown("---")

st.markdown(
    "### Translation"
)


with st.sidebar:

    st.markdown("---")

    st.subheader(
        "Parámetros de traducción"
    )

    translator = Translator()


    # --------------------------------------------------------
    # INPUT LANGUAGE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # OUTPUT LANGUAGE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # ACCENT
    # --------------------------------------------------------

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
# TRANSLATION ACTION
# ============================================================

display_output_text = st.checkbox(
    "Mostrar texto traducido"
)


if st.button(
    "DECIPHER AND TRANSLATE"
):

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


        # ----------------------------------------------------
        # TRANSLATED MIRROR
        # ----------------------------------------------------

        safe_output = (
            output_text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )


        st.markdown(
            f"""
            <div class="magic-mirror">

                <div class="mirror-particles">
                    {particles}
                </div>

                <div class="mirror-content">

                    <div class="mirror-eyebrow">
                        Translation complete
                    </div>

                    <div class="mirror-message">
                        {safe_output}
                        <span class="decipher-cursor"></span>
                    </div>

                    <div class="mirror-status">

                        <span class="status-orb"></span>

                        <span>
                            Message translated
                        </span>

                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            "### Voice"
        )


        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )


        if display_output_text:

            st.markdown(
                "### Translated text"
            )

            st.write(
                output_text
            )
