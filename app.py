import streamlit as st
import os
from processor import crear_clip, detectar_momentos_clave

st.set_page_config(page_title="AI Clip Master", page_icon="🎬", layout="centered")

st.title("🎬 AI Clip Master")
st.subheader("Crea clips virales automáticamente con IA")

tab_videos, tab_pelis = st.tabs(["🎥 Videos Cortos", "🍿 Películas"])

with tab_videos:
    uploaded_file = st.file_uploader("Elige un video para procesar", type=['mp4', 'mov'])
    
    duracion_elegida = st.select_slider(
        "Duración del resultado:",
        options=["30s", "1:00", "1:30"]
    )

    if st.button("🚀 Iniciar Proceso de IA"):
        if uploaded_file:
            temp_name = "input_ia_temp.mp4"
            with open(temp_name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("La IA está buscando el mejor momento..."):
                try:
                    inicio = detectar_momentos_clave(temp_name)
                    resultado = crear_clip(temp_name, inicio, duracion_elegida)
                    
                    st.success("¡Clip generado con éxito!")
                    st.video(resultado)
                    
                    with open(resultado, "rb") as file:
                        st.download_button("📥 Descargar mi Clip", file, file_name=resultado)
                
                except Exception as e:
                    st.error(f"Hubo un problema procesando el video: {e}")
        else:
            st.warning("Primero debes subir un archivo de video.")

with tab_pelis:
    st.info("Esta partición usará algoritmos avanzados para detectar cambios de escena cinematográficos.")
