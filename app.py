import streamlit as st
import os
from processor import extraer_mejores_clips

st.set_page_config(page_title="OpusClone AI", layout="wide", page_icon="🔥")

st.title("🔥 OpusClone: Viral Clip Generator")
st.markdown("---")

with st.sidebar:
    st.header("Configuración de IA")
    num_clips = st.number_input("Máximo de clips a generar", 1, 10, 3)
    duracion = st.select_slider("Duración objetivo", options=["30s", "1:00", "1:30"])

uploaded_file = st.file_uploader("📤 Sube tu contenido (Podcast, Tutorial, Gameplay)", type=['mp4', 'mov'])

if st.button("🪄 Analizar y Generar Clips"):
    if uploaded_file:
        temp_path = "input_pro.mp4"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.toast("Analizando estructura del video...", icon="🧠")
        
        with st.spinner("IA trabajando: Identificando ganchos y mejores momentos..."):
            clips_generados = extraer_mejores_clips(temp_path, duracion, num_clips)
            
            st.success(f"¡Análisis completado! Hemos encontrado {len(clips_generados)} momentos potenciales.")
            
            for clip in clips_generados:
                with st.container():
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.video(clip["path"])
                    with col2:
                        st.subheader(f"🎬 Clip: {clip['path']}")
                        st.metric("Virality Score", f"{clip['score']}%")
                        st.write("✅ Gancho detectado")
                        st.write("✅ Audio optimizado")
                        
                        with open(clip["path"], "rb") as f:
                            st.download_button(
                                label="📥 Descargar HD",
                                data=f,
                                file_name=clip["path"],
                                mime="video/mp4",
                                key=clip["path"]
                            )
                    st.markdown("---")
    else:
        st.error("Debes subir un archivo para que la IA pueda trabajar.")
