import streamlit as st
import os
from processor import extraer_mejores_clips, descargar_video_url, limpiar_archivos_antiguos


st.set_page_config(page_title="IA Clip Master", layout="wide")
st.title("🎬 IA Clip Master (Estilo OpusClip)")

opcion = st.sidebar.radio("Fuente del video:", ["Link de YouTube/TikTok", "Archivo MP4"])
video_a_procesar = None

if opcion == "Link de YouTube/TikTok":
    url = st.text_input("Pega el enlace aquí:")
    if url and st.button("Descargar Video"):
        with st.spinner("Descargando..."):
            video_a_procesar = descargar_video_url(url)
            st.success("¡Video listo!")
else:
    archivo = st.file_uploader("Sube tu archivo", type=["mp4"])
    if archivo:
        video_a_procesar = "temp_local.mp4"
        with open(video_a_procesar, "wb") as f:
            f.write(archivo.getbuffer())

if video_a_procesar:
    num = st.sidebar.slider("¿Cuántos clips quieres?", 1, 5, 3)
    tiempo = st.sidebar.select_slider("Duración:", ["30s", "1:00", "1:30"])

    if st.button("🔥 Generar Clips Virales"):
        with st.spinner("Analizando momentos clave..."):
            clips = extraer_mejores_clips(video_a_procesar, tiempo, num)
            
            for c in clips:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.video(c["path"])
                with col2:
                    st.write(f"📍 Inicia en: {c['timestamp']}")
                    with open(c["path"], "rb") as f:
                        st.download_button(f"📥 Descargar {c['path']}", f, file_name=c['path'])
                st.divider()
