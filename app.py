# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
"""
<style>

/* ============================================================
   FONDO PRINCIPAL
   ============================================================ */

.stApp {

    background:
        radial-gradient(
            circle at 20% 20%,
            rgba(90, 55, 170, 0.20),
            transparent 30%
        ),
        radial-gradient(
            circle at 80% 30%,
            rgba(40, 100, 170, 0.16),
            transparent 28%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(150, 45, 130, 0.16),
            transparent 35%
        ),
        linear-gradient(
            120deg,
            #030207,
            #0a0612,
            #050713,
            #090510,
            #030207
        );

    background-size:
        250% 250%;

    animation:
        backgroundFlow 18s ease infinite;

}


/* Movimiento del fondo */

@keyframes backgroundFlow {

    0% {
        background-position: 0% 50%;
    }

    25% {
        background-position: 70% 20%;
    }

    50% {
        background-position: 100% 70%;
    }

    75% {
        background-position: 30% 100%;
    }

    100% {
        background-position: 0% 50%;
    }

}


/* ============================================================
   PARTÍCULAS DE FONDO
   ============================================================ */

/*
   Se utilizan pseudo-elementos del propio contenedor.
   No se crean <span>, <div> ni elementos HTML adicionales.
*/

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
            rgba(210,190,255,0.9) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle,
            rgba(130,180,255,0.7) 0 1px,
            transparent 2px
        ),

        radial-gradient(
            circle,
            rgba(235,190,255,0.6) 0 1.5px,
            transparent 2.5px
        );

    background-size:
        83px 97px,
        137px 151px,
        211px 193px;

    background-position:
        10px 20px,
        50px 80px,
        100px 30px;

    animation:
        particlesDrift 35s linear infinite;

}


@keyframes particlesDrift {

    from {
        transform:
            translate3d(0, 0, 0);
    }

    50% {
        transform:
            translate3d(25px, -40px, 0);
    }

    to {
        transform:
            translate3d(-10px, -80px, 0);
    }

}


/* Segunda capa de partículas */

.stApp::after {

    content: "";

    position: fixed;

    inset: -20%;

    pointer-events: none;

    z-index: 0;

    background:

        radial-gradient(
            circle at 20% 30%,
            rgba(110,70,220,0.08),
            transparent 12%
        ),

        radial-gradient(
            circle at 75% 25%,
            rgba(70,130,230,0.08),
            transparent 15%
        ),

        radial-gradient(
            circle at 45% 80%,
            rgba(180,60,180,0.08),
            transparent 17%
        );

    filter:
        blur(25px);

    animation:
        atmosphericMovement 14s ease-in-out infinite alternate;

}


@keyframes atmosphericMovement {

    from {
        transform:
            translate(-2%, -2%)
            scale(1);
    }

    to {
        transform:
            translate(3%, 2%)
            scale(1.08);
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
        #f0e9df !important;

    text-shadow:

        0 0 8px
        rgba(230,215,255,0.55),

        0 0 25px
        rgba(150,100,240,0.45),

        0 0 60px
        rgba(90,50,180,0.35);

    animation:
        titleGlow 4s ease-in-out infinite;

}


@keyframes titleGlow {

    0%, 100% {

        text-shadow:

            0 0 8px
            rgba(230,215,255,0.45),

            0 0 25px
            rgba(150,100,240,0.35),

            0 0 60px
            rgba(90,50,180,0.25);

    }

    50% {

        text-shadow:

            0 0 12px
            rgba(240,225,255,0.75),

            0 0 40px
            rgba(165,115,255,0.60),

            0 0 90px
            rgba(100,55,210,0.40);

    }

}


/* ============================================================
   INSTRUCCIONES
   ============================================================ */

[data-testid="stAlert"] {

    background:
        rgba(10,8,17,0.80) !important;

    border:
        1px solid
        rgba(170,140,220,0.20) !important;

    box-shadow:
        0 10px 40px rgba(0,0,0,0.30);

}


/* ============================================================
   TARJETAS
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        linear-gradient(
            145deg,
            rgba(20,14,30,0.90),
            rgba(7,6,12,0.90)
        );

    border:
        1px solid
        rgba(170,140,215,0.22);

    border-radius:
        10px;

    box-shadow:

        inset 0 0 30px
        rgba(130,80,200,0.05),

        0 15px 50px
        rgba(0,0,0,0.35);

    transition:
        transform 0.35s ease,
        box-shadow 0.35s ease,
        border-color 0.35s ease;

}


div[data-testid="stVerticalBlockBorderWrapper"]:hover {

    transform:
        translateY(-7px)
        scale(1.01);

    border-color:
        rgba(195,165,240,0.55);

    box-shadow:

        inset 0 0 40px
        rgba(140,90,220,0.08),

        0 20px 70px
        rgba(80,45,150,0.30),

        0 0 30px
        rgba(140,100,220,0.12);

}


/* ============================================================
   ESPEJO
   ============================================================ */

div[data-testid="stVerticalBlock"]:has(
    [data-testid="stMetric"]
) {

    transition:
        transform 0.3s ease;

}


/* ============================================================
   BOTONES
   ============================================================ */

.stButton > button {

    min-height:
        58px;

    border-radius:
        5px;

    border:
        1px solid
        rgba(180,145,225,0.55);

    background:

        linear-gradient(
            120deg,
            rgba(48,30,70,0.95),
            rgba(16,11,25,0.98),
            rgba(43,26,68,0.95)
        );

    background-size:
        200% 200%;

    color:
        #f1eae1;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        1rem;

    letter-spacing:
        0.16em;

    box-shadow:
        0 0 20px
        rgba(110,70,180,0.10);

    transition:
        all 0.25s ease;

}


.stButton > button:hover {

    transform:
        translateY(-3px);

    background-position:
        100% 50%;

    border-color:
        rgba(225,205,250,0.85);

    box-shadow:

        0 0 20px
        rgba(170,120,245,0.35),

        0 0 55px
        rgba(100,60,190,0.20);

}


/* ============================================================
   SELECTORES
   ============================================================ */

div[data-baseweb="select"] > div {

    background:
        rgba(10,8,16,0.92) !important;

    border:
        1px solid
        rgba(175,145,215,0.22) !important;

    transition:
        border-color 0.25s ease,
        box-shadow 0.25s ease;

}


div[data-baseweb="select"] > div:hover {

    border-color:
        rgba(190,155,235,0.60) !important;

    box-shadow:
        0 0 20px
        rgba(130,85,200,0.16);

}


/* ============================================================
   SUBIDA DE ARCHIVOS
   ============================================================ */

[data-testid="stFileUploader"] {

    background:
        rgba(7,6,12,0.55);

    border:
        1px dashed
        rgba(170,140,215,0.30);

    border-radius:
        6px;

    transition:
        all 0.3s ease;

}


[data-testid="stFileUploader"]:hover {

    border-color:
        rgba(205,175,245,0.70);

    box-shadow:
        0 0 35px
        rgba(110,65,190,0.18);

}


/* ============================================================
   CÁMARA
   ============================================================ */

[data-testid="stCameraInput"] {

    background:
        rgba(7,6,12,0.60);

    border:
        1px solid
        rgba(170,140,215,0.20);

    border-radius:
        6px;

}


/* ============================================================
   IMÁGENES
   ============================================================ */

[data-testid="stImage"] img {

    border-radius:
        8px;

    box-shadow:

        0 0 20px
        rgba(120,80,200,0.15),

        0 15px 45px
        rgba(0,0,0,0.40);

}


/* ============================================================
   MÉTRICAS
   ============================================================ */

[data-testid="stMetric"] {

    background:
        rgba(12,9,20,0.72);

    border:
        1px solid
        rgba(170,145,205,0.15);

    border-radius:
        6px;

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
            rgba(85,50,135,0.15),
            transparent 35%
        ),

        linear-gradient(
            180deg,
            #050409,
            #0a0710
        );

    border-right:
        1px solid
        rgba(175,145,210,0.12);

    box-shadow:
        15px 0 70px
        rgba(0,0,0,0.55);

}


/* ============================================================
   AUDIO
   ============================================================ */

audio {

    width:
        100%;

    filter:
        drop-shadow(
            0 0 18px
            rgba(130,85,210,0.25)
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
            rgba(220,200,250,0.30),
            rgba(170,130,230,0.50),
            transparent
        ) !important;

    box-shadow:
        0 0 12px
        rgba(130,80,200,0.25);

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

st.subheader("Cómo funciona")

st.info(
    """
    **1. Elige cámara o imagen.**
    
    **2. Introduce una imagen con texto.**
    
    **3. Selecciona idioma original y destino en el panel lateral.**
    
    **4. Pulsa "DECIFRAR Y TRADUCIR".**
    
    **5. Lee o escucha el resultado.**
    """
)


# ============================================================
# FUENTE
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
# ESPEJO VISUAL
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

    st.markdown(
        """
        <style>

        /*
        Este bloque solamente modifica el fondo del
        contenedor visual mediante CSS.
        No contiene texto HTML visible.
        */

        [data-testid="stVerticalBlock"]:has(
            .mirror-trigger
        ) {
            position: relative;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "Esperando una imagen..."
    )
