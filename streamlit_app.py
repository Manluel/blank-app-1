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

# Dibujos del ahorcado
ahorcado_dibujos = [
    """<pre style='color:red;'>
.____.
|    |
|     
|     
|     
|     
|     
|     
</pre>""",
    """<pre style='color:red;'>
.____.
|    |
|    o
|     
|     
|     
|     
|     
</pre>""",
    """<pre style='color:orange;'>
.____.
|    |
|    O
|    |
|    |
|     
|     
|     
</pre>""",
    """<pre style='color:orange;'>
.____.
|    |
|    O
| ---|---
|    |
|     
|     
|     
</pre>""",
    """<pre style='color:green;'>
.____.
|    |
|    O
| ---|---
|    |
|   | 
|   | 
|     
</pre>""",
    """<pre style='color:green;'>
.____.
|    |
|    O
| ---|---
|    |
|   | |
|   | |
|     
</pre>"""
]

# ------------------- Juego del Ahorcado -------------------
def jugar_ahorcado():
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🔠 Juego del Ahorcado</h1>", unsafe_allow_html=True)

    if "palabra" not in st.session_state:
        st.session_state.palabra = random.choice(["zapallo", "tarta", "banana", "maiz", "pileta", "ajo"])
        st.session_state.errores = 0
        st.session_state.terminado = False
        st.session_state.pista = f"Tiene {len(st.session_state.palabra)} letras y {sum(1 for c in st.session_state.palabra if c in 'aeiou')} vocales."

    palabra = st.session_state.palabra
    errores = st.session_state.errores

    st.info(f"💡 Pista: {st.session_state.pista}")
    st.markdown(ahorcado_dibujos[min(errores, len(ahorcado_dibujos)-1)], unsafe_allow_html=True)

    if not st.session_state.terminado:
        intento = st.text_input("Adivina la palabra:")
        if st.button("✅ Enviar Respuesta"):
            st.session_state.estadisticas["intentos"] += 1
            if intento.lower() == palabra:
                st.success(f"🎉 ¡Ganaste! La palabra era: {palabra}")
                st.session_state.estadisticas["victorias"] += 1
                st.session_state.estadisticas["racha"] += 1
                st.session_state.terminado = True
            else:
                st.session_state.errores += 1
                if st.session_state.errores >= len(ahorcado_dibujos) - 1:
                    st.error(f"💀 Perdiste. La palabra era: {palabra}")
                    st.session_state.estadisticas["derrotas"] += 1
                    st.session_state.estadisticas["racha"] = 0
                    st.session_state.terminado = True

    if st.button("🔙 Volver al menú"):
        for key in ["palabra", "errores", "terminado", "pista"]:
            st.session_state.pop(key, None)
        st.session_state.pagina = "menu"

# ------------------- Juego Adivina el Número -------------------
def adivina_numero():
    st.markdown("<h1 style='text-align: center; color: #33C3F0;'>🔢 Adivina el Número</h1>", unsafe_allow_html=True)

    if "numero" not in st.session_state:
        st.session_state.numero = random.randint(1, 20)
        st.session_state.intentos_num = 0

    guess = st.number_input("Estoy pensando en un número del 1 al 20:", 1, 20, step=1)
    if st.button("🎯 Adivinar"):
        st.session_state.intentos_num += 1
        st.session_state.estadisticas["intentos"] += 1

        if guess < st.session_state.numero:
            st.warning("📉 Muy bajo.")
        elif guess > st.session_state.numero:
            st.warning("📈 Muy alto.")
        else:
            st.success(f"🎯 ¡Correcto! Era el {st.session_state.numero} en {st.session_state.intentos_num} intentos.")
            st.session_state.estadisticas["victorias"] += 1
            st.session_state.estadisticas["racha"] += 1
            del st.session_state["numero"]
            del st.session_state["intentos_num"]

    if st.button("🔙 Volver al menú"):
        st.session_state.pagina = "menu"
        st.session_state.pop("numero", None)
        st.session_state.pop("intentos_num", None)

# ------------------- Juego Piedra Papel o Tijera -------------------
def piedra_papel_tijera():
    st.markdown("<h1 style='text-align: center; color: #2ECC71;'>✊ Piedra, Papel o Tijera</h1>", unsafe_allow_html=True)
    opciones = ["piedra", "papel", "tijera"]
    jugador = st.selectbox("Elige tu jugada:", opciones)

    if st.button("🕹️ Jugar" ):
        pc = random.choice(opciones)
        st.write(f"🤖 La computadora eligió: {pc}")
        st.session_state.estadisticas["intentos"] += 1

        if jugador == pc:
            st.info("🟰 Empate.")
        elif (jugador == "piedra" and pc == "tijera") or (jugador == "papel" and pc == "piedra") or (jugador == "tijera" and pc == "papel"):
            st.success("🏆 ¡Ganaste!")
            st.session_state.estadisticas["victorias"] += 1
            st.session_state.estadisticas["racha"] += 1
        else:
            st.error("💥 Perdiste.")
            st.session_state.estadisticas["derrotas"] += 1
            st.session_state.estadisticas["racha"] = 0

    if st.button("🔙 Volver al menú"):
        st.session_state.pagina = "menu"

# ------------------- Estadísticas -------------------
def mostrar_estadisticas():
    st.markdown("<h1 style='text-align: center; color: #9B59B6;'>📊 Estadísticas Generales</h1>", unsafe_allow_html=True)
    stats = st.session_state.estadisticas
    st.success(f"🏆 Ganadas: {stats['victorias']}")
    st.error(f"💀 Perdidas: {stats['derrotas']}")
    st.info(f"🔥 Racha: {stats['racha']}")
    st.warning(f"🎮 Intentos totales: {stats['intentos']}")

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
        if st.button("🔠 Ahorcado"):
            st.session_state.pagina = "ahorcado"
    with col2:
        if st.button("🔢 Adivina el Número"):
            st.session_state.pagina = "numero"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("✊ Piedra, Papel o Tijera"):
            st.session_state.pagina = "ppt"
    with col4:
        if st.button("📊 Ver Estadísticas"):
            st.session_state.pagina = "estadisticas"

# ------------------- Enrutamiento -------------------
pagina = st.session_state.pagina
if pagina == "menu":
    menu_principal()
elif pagina == "ahorcado":
    jugar_ahorcado()
elif pagina == "numero":
    adivina_numero()
elif pagina == "ppt":
    piedra_papel_tijera()
elif pagina == "estadisticas":
    mostrar_estadisticas()
