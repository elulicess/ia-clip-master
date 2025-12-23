import streamlit as st
import os
from processor import crear_clips_lote, detectar_varios_momentos

st.set_page_config(page_title="AI Clip Master", layout="wide")

st.title("🎬 AI Clip Master: Multi-Clips")

uploaded_file = st.file_uploader("Sube tu video", type=['mp4', 'mov'])

num_clips = st.slider("¿Cuántos clips quieres generar?", 1, 5, 3)

duration = st.select_slider(
    "Duración de cada clip:",
    options=["30s", "1:00", "1:30"]
)

if st.button("🚀 Generar Fragmentos"):
    if uploaded_file is not None:
        temp_path = "temp_video.mp4"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner(f"🤖 Generando {num_clips} clips con los mejores momentos..."):
            try:
                puntos = detectar_varios_momentos(temp_path, num_clips)
                
                archivos = crear_clips_lote(temp_path, puntos, duration)
                
                st.success(f"✅ ¡Se han generado {len(archivos)} clips!")
                
                cols = st.columns(len(archivos))
                for idx, clip_path in enumerate(archivos):
                    with cols[idx]:
                        st.write(f"Fragmento {idx+1}")
                        st.video(clip_path)
                        with open(clip_path, "rb") as f:
                            st.download_button(f"📥 Bajar Clip {idx+1}", f, file_name=clip_path)
                            
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("⚠️ Sube un video primero.")
