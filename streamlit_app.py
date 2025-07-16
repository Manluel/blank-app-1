import streamlit as st
import random

st.set_page_config(page_title="🎮 Juegos Web", layout="centered")

# Estadísticas globales
def init_session():
    if "estadisticas" not in st.session_state:
        st.session_state.estadisticas = {
            "victorias": 0,
            "derrotas": 0,
            "racha": 0,
            "intentos": 0
        }
        st.session_state.pagina = "menu"
init_session()

# Dibujos del ahorcado
dibujos = [
    ".____.\n|    |\n|    \n|    \n|    \n|    \n|    \n|    ",
    ".____.\n|    |\n|    o\n|    \n|    \n|    \n|    \n|    ",
    ".____.\n|    |\n|    O\n|    |\n|    |\n|    \n|    \n|    ",
    ".____.\n|    |\n|    O\n| ---|---\n|    |\n|    \n|    \n|    ",
    ".____.\n|    |\n|    O\n| ---|---\n|    |\n|   | \n|   | \n|    ",
    ".____.\n|    |\n|    O\n| ---|---\n|    |\n|   | |\n|   | |\n|    "
]

# -------------------
# Juego 1: Ahorcado
# -------------------
def jugar_ahorcado():
    st.subheader("🔠 Juego del Ahorcado")
    if "palabra" not in st.session_state:
        st.session_state.palabra = random.choice(["zapallo", "tarta", "banana", "maiz", "pileta", "ajo"])
        st.session_state.errores = 0
        st.session_state.max_errores = len(dibujos) - 1
        st.session_state.pista = f"Tiene {len(st.session_state.palabra)} letras y {sum(1 for c in st.session_state.palabra if c in 'aeiou')} vocales."
        st.session_state.gano = False

    palabra = st.session_state.palabra
    errores = st.session_state.errores

    st.info(f"Pista: {st.session_state.pista}")
    st.text(dibujos[errores])
    intento = st.text_input("Adivina la palabra:").lower()
    if st.button("Enviar"):
        st.session_state.estadisticas["intentos"] += 1
        if intento == palabra:
            st.success(f"🎉 ¡Ganaste! La palabra era: {palabra}")
            st.session_state.estadisticas["victorias"] += 1
            st.session_state.estadisticas["racha"] += 1
            st.session_state.gano = True
        else:
            st.session_state.errores += 1
            st.warning("❌ Incorrecto.")
            if st.session_state.errores == st.session_state.max_errores:
                st.error(f"💀 Perdiste. La palabra era: {palabra}")
                st.session_state.estadisticas["derrotas"] += 1
                st.session_state.estadisticas["racha"] = 0

    if st.button("🔙 Volver al menú"):
        st.session_state.pagina = "menu"
        for key in ["palabra", "errores", "max_errores", "pista", "gano"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()

# -------------------
# Juego 2: Adivina el número
# -------------------
def adivina_numero():
    st.subheader("🔢 Adivina el número")
    if "numero" not in st.session_state:
        st.session_state.numero = random.randint(1, 20)
        st.session_state.intentos = 0

    guess = st.number_input("Estoy pensando en un número del 1 al 20", min_value=1, max_value=20, step=1)
    if st.button("Adivinar"):
        st.session_state.intentos += 1
        st.session_state.estadisticas["intentos"] += 1
        if guess < st.session_state.numero:
            st.warning("📉 Demasiado bajo.")
        elif guess > st.session_state.numero:
            st.warning("📈 Demasiado alto.")
        else:
            st.success(f"🎯 ¡Correcto! El número era {st.session_state.numero}. Lo lograste en {st.session_state.intentos} intentos.")
            st.session_state.estadisticas["victorias"] += 1
            st.session_state.estadisticas["racha"] += 1
            del st.session_state["numero"]
            del st.session_state["intentos"]

    if st.button("🔙 Volver al menú"):
        st.session_state.pagina = "menu"
        if "numero" in st.session_state:
            del st.session_state["numero"]
        st.experimental_rerun()

# -------------------
# Juego 3: Piedra, Papel o Tijera
# -------------------
def piedra_papel_tijera():
    st.subheader("✊🖐✌ Piedra, Papel o Tijera")
    opciones = ["piedra", "papel", "tijera"]
    jugador = st.selectbox("Elige:", opciones)
    if st.button("Jugar"):
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
        st.experimental_rerun()

# -------------------
# Ver estadísticas
# -------------------
def mostrar_estadisticas():
    st.subheader("📊 Estadísticas Generales")
    stats = st.session_state.estadisticas
    st.write(f"🏆 Partidas ganadas: {stats['victorias']}")
    st.write(f"💀 Partidas perdidas: {stats['derrotas']}")
    st.write(f"🔥 Racha actual: {stats['racha']}")
    st.write(f"🎮 Total de intentos: {stats['intentos']}")

    if st.button("🔙 Volver al menú"):
        st.session_state.pagina = "menu"
        st.experimental_rerun()

# -------------------
# Menú principal
# -------------------
def menu_principal():
    st.title("🕹 MENÚ PRINCIPAL DE JUEGOS")
    st.write("1. 🎯 Juego del Ahorcado")
    st.write("2. 🔢 Adivina el Número")
    st.write("3. ✊ Piedra, Papel o Tijera")
    st.write("4. 📊 Ver Estadísticas")
    opcion = st.selectbox("Selecciona un juego:", ["--", "Ahorcado", "Adivina el Número", "Piedra, Papel o Tijera", "Ver Estadísticas"])

    if opcion == "Ahorcado":
        st.session_state.pagina = "ahorcado"
    elif opcion == "Adivina el Número":
        st.session_state.pagina = "numero"
    elif opcion == "Piedra, Papel o Tijera":
        st.session_state.pagina = "ppt"
    elif opcion == "Ver Estadísticas":
        st.session_state.pagina = "estadisticas"

    st.write("\nHecho por Manuel ✨")

# Enrutamiento de páginas
if st.session_state.pagina == "menu":
    menu_principal()
elif st.session_state.pagina == "ahorcado":
    jugar_ahorcado()
elif st.session_state.pagina == "numero":
    adivina_numero()
elif st.session_state.pagina == "ppt":
    piedra_papel_tijera()
elif st.session_state.pagina == "estadisticas":
    mostrar_estadisticas()

