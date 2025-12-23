import streamlit as st
import os
from processor import crear_clip, detectar_momentos_clave

st.set_page_config(page_title="AI Clip Master", page_icon="🎬")

st.title("🎬 AI Clip Master")
st.subheader("Recortes automáticos por volumen de audio")

uploaded_file = st.file_uploader("Sube tu video (MP4 o MOV)", type=['mp4', 'mov'])

duration = st.select_slider(
    "Selecciona la duración del clip:",
    options=["30s", "1:00", "1:30"]
)

if st.button("🚀 Generar Clip"):
    if uploaded_file is not None:
        temp_path = "temp_video.mp4"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("🤖 Analizando audio y recortando..."):
            try:
                inicio = detectar_momentos_clave(temp_path)
                final_file = crear_clip(temp_path, inicio, duration)
                
                st.success(f"✅ ¡Hecho! Clip generado desde el segundo {int(inicio)}.")
                st.video(final_file)
                
                with open(final_file, "rb") as f:
                    st.download_button("📥 Descargar Clip", f, file_name=final_file)
            except Exception as e:
                st.error(f"Error procesando video: {e}")
    else:
        st.error("⚠️ Por favor, sube un video primero.")
