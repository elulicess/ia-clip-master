import streamlit as st
from processor import extraer_mejores_clips, descargar_video_url, limpiar_archivos_antiguos

st.set_page_config(page_title="OpusClone AI", layout="wide")

st.title("🔥 OpusClone Pro")


if st.sidebar.button("🧹 Limpiar Servidor (Borrar temporales)"):
    limpiar_archivos_antiguos()
    st.sidebar.success("Servidor limpio")

metodo = st.radio("Entrada:", ["Link", "Archivo Local"])

video_path = None

if metodo == "Link":
    url = st.text_input("🔗 Link del video (YouTube, TikTok, Instagram):")
    if url:
        if st.button("Descargar y Analizar"):
            with st.spinner("Descargando..."):
                try:
                    video_path = descargar_video_url(url)
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    file = st.file_uploader("Sube video", type=['mp4'])
    if file:
        video_path = "input.mp4"
        with open(video_path, "wb") as f:
            f.write(file.getbuffer())

if video_path:()
