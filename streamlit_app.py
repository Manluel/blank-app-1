import streamlit as st
import random

st.set_page_config(page_title="🎮 Juegos Interactivos", layout="centered", page_icon="🕹️")

# Inicialización de estado global
if "estadisticas" not in st.session_state:
    st.session_state.estadisticas = {
        "victorias": 0,
        "derrotas": 0,
        "racha": 0,
        "intentos": 0
    }
    st.session_state.pagina = "menu"

# ------------------- Trivia -------------------
trivia_preguntas = [
    {"pregunta": "¿Cuál es el océano más grande del mundo?", "opciones": ["Atlántico", "Índico", "Pacífico"], "respuesta": "Pacífico"},
    {"pregunta": "¿Quién pintó la Mona Lisa?", "opciones": ["Picasso", "Leonardo da Vinci", "Van Gogh"], "respuesta": "Leonardo da Vinci"},
    {"pregunta": "¿Cuántos planetas tiene el sistema solar?", "opciones": ["7", "8", "9"], "respuesta": "8"}
]

if "trivia_puntaje" not in st.session_state:
    st.session_state.trivia_puntaje = 0
    st.session_state.trivia_index = 0
    st.session_state.avanzar_trivia = False
    st.session_state.ultima_correcta = False

def jugar_trivia():
    st.markdown("<h1 style='text-align: center; color: #00BFFF;'>🧠 Trivia de Cultura General</h1>", unsafe_allow_html=True)

    idx = st.session_state.trivia_index

    if idx >= len(trivia_preguntas):
        st.success(f"Has terminado la trivia. Puntaje: {st.session_state.trivia_puntaje} / {len(trivia_preguntas)}")
        st.session_state.estadisticas["intentos"] += len(trivia_preguntas)
        st.session_state.trivia_index = 0
        st.session_state.trivia_puntaje = 0
        if st.button("🔙 Volver al menú"):
            st.session_state.pagina = "menu"
        return

    pregunta = trivia_preguntas[idx]
    st.subheader(pregunta["pregunta"])
    opcion = st.radio("Elige una opción:", pregunta["opciones"], key=f"radio_{idx}")

    if st.button("✅ Confirmar") and not st.session_state.avanzar_trivia:
        st.session_state.estadisticas["intentos"] += 1
        st.session_state.avanzar_trivia = True
        st.session_state.ultima_correcta = (opcion == pregunta["respuesta"])

    if st.session_state.avanzar_trivia:
        if st.session_state.ultima_correcta:
            st.success("✔️ Correcto!")
            st.session_state.trivia_puntaje += 1
            st.session_state.estadisticas["victorias"] += 1
            st.session_state.estadisticas["racha"] += 1
        else:
            st.error(f"❌ Incorrecto. La respuesta era: {pregunta['respuesta']}")
            st.session_state.estadisticas["derrotas"] += 1
            st.session_state.estadisticas["racha"] = 0

        if st.button("➡️ Siguiente pregunta"):
            st.session_state.trivia_index += 1
            st.session_state.avanzar_trivia = False
            st.experimental_rerun()

# ------------------- Juego de Memoria Visual -------------------
if "secuencia" not in st.session_state:
    st.session_state.secuencia = []
    st.session_state.usuario = []
    st.session_state.memoria_fase = "mostrar"
    st.session_state.nivel = 1

colores = ["🟥", "🟩", "🟦", "🟨"]

def juego_memoria():
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>🧠 Memoria Visual</h1>", unsafe_allow_html=True)

    if st.session_state.memoria_fase == "mostrar":
        if len(st.session_state.secuencia) < st.session_state.nivel:
            st.session_state.secuencia.append(random.choice(colores))

        st.info(f"Recuerda esta secuencia de colores nivel {st.session_state.nivel}:")
        st.write(" ".join(st.session_state.secuencia))

        if st.button("👉 Estoy listo!"):
            st.session_state.memoria_fase = "ingresar"
            st.experimental_rerun()

    elif st.session_state.memoria_fase == "ingresar":
        st.write("Ingresa la secuencia (uno por uno):")
        for i in range(len(st.session_state.secuencia)):
            col = st.selectbox(f"Color {i+1}", colores, key=f"col{i}")
            if len(st.session_state.usuario) < len(st.session_state.secuencia):
                st.session_state.usuario.append(col)

        if len(st.session_state.usuario) == len(st.session_state.secuencia):
            if st.button("✅ Verificar"):
                st.session_state.estadisticas["intentos"] += 1
                if st.session_state.usuario == st.session_state.secuencia:
                    st.success("¡Correcto! Pasas al siguiente nivel 🎉")
                    st.session_state.estadisticas["victorias"] += 1
                    st.session_state.estadisticas["racha"] += 1
                    st.session_state.usuario = []
                    st.session_state.memoria_fase = "mostrar"
                    st.session_state.nivel += 1
                else:
                    st.error("Fallaste 😢. Se reinicia el juego.")
                    st.session_state.estadisticas["racha"] = 0
                    st.session_state.estadisticas["derrotas"] += 1
                    st.session_state.secuencia = []
                    st.session_state.usuario = []
                    st.session_state.memoria_fase = "mostrar"
                    st.session_state.nivel = 1
                st.experimental_rerun()

    if st.button("🔙 Volver al menú"):
        st.session_state.pagina = "menu"
        st.session_state.secuencia = []
        st.session_state.usuario = []
        st.session_state.memoria_fase = "mostrar"
        st.session_state.nivel = 1

# ------------------- Ver estadísticas -------------------
def mostrar_estadisticas():
    st.markdown("<h1 style='text-align: center; color: #6A5ACD;'>📊 Estadísticas Generales</h1>", unsafe_allow_html=True)
    stats = st.session_state.estadisticas
    col1, col2 = st.columns(2)
    col1.metric("🏆 Ganadas", stats["victorias"])
    col2.metric("💀 Perdidas", stats["derrotas"])
    col1.metric("🔥 Racha", stats["racha"])
    col2.metric("🎮 Intentos", stats["intentos"])

    if st.button("🔙 Volver al menú"):
        st.session_state.pagina = "menu"

# ------------------- Menú principal -------------------
def menu_principal():
    st.markdown("""
        <h1 style='text-align: center; color: #FF8C00;'>🎮 MENÚ DE JUEGOS INTERACTIVOS</h1>
        <div style='text-align: center;'>
            <p>Selecciona una opción:</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Trivia"):
            st.session_state.pagina = "trivia"
    with col2:
        if st.button("🧠 Memoria Visual"):
            st.session_state.pagina = "memoria"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("📊 Ver Estadísticas"):
            st.session_state.pagina = "estadisticas"
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)

# ------------------- Enrutamiento -------------------
pagina = st.session_state.pagina
if pagina == "menu":
    menu_principal()
elif pagina == "trivia":
    jugar_trivia()
elif pagina == "memoria":
    juego_memoria()
elif pagina == "estadisticas":
    mostrar_estadisticas()
