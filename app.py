import streamlit as st
from groq import Groq
from gtts import gTTS
import time

# --- 1. CONFIGURACIÓN Y ESTILO eDEX-UI ---
st.set_page_config(page_title="TERMINAL_CORE", layout="wide")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp, [data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    * {
        color: #00ff41 !important;
        font-family: 'Courier New', monospace !important;
    }
    .stChatMessage {
        background-color: #000 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 0px !important;
        margin: 10px auto !important;
        width: 80% !important;
    }
    .stChatInputContainer { border-top: 1px solid #00ff41 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN SEGURA (Usa secrets de Streamlit) ---
# En Streamlit Cloud, pondrás tu llave en 'Settings > Secrets'
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Configura la GROQ_API_KEY en los Secrets de Streamlit.")

# --- 3. SECUENCIA DE ARRANQUE ---
if "boot" not in st.session_state:
    boot_log = st.empty()
    log = ""
    for line in ["> LOADING CORE...", "> SYMMETRY OK...", "> ACCESS GRANTED"]:
        log += line + "\n"
        boot_log.code(log)
        time.sleep(0.4)
    boot_log.empty()
    st.session_state.boot = True

# --- 4. INTERFAZ SIMÉTRICA ---
st.title("📟 DEV-MASTER // WEB_CONSOLE")
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.write("SYS: ONLINE")
with col3:
    if st.button("RESET"):
        st.session_state.mensajes = []
        st.rerun()

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

with col2:
    for m in st.session_state.mensajes:
        with st.chat_message(m["role"]):
            st.write(f"{m['role'].upper()} > {m['content']}")

    if prompt := st.chat_input("Escribe comando..."):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(f"USER > {prompt}")

        with st.chat_message("assistant"):
            res_placeholder = st.empty()
            full_res = ""
            
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "IA Tactica. Responde corto."}] + st.session_state.mensajes,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    res_placeholder.markdown(full_res + "█")
            
            res_placeholder.markdown(full_res)
            
            # Voz
            tts = gTTS(text=full_res[:200], lang='es')
            tts.save("voz.mp3")
            st.audio("voz.mp3", format="audio/mp3", autoplay=True)

            st.session_state.mensajes.append({"role": "assistant", "content": full_res})
