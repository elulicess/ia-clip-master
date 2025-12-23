import streamlit as st

st.set_page_config(page_title="AI Clip Master", layout="wide")

st.title("🎬 AI Clip Master: Recortes Automáticos")
st.markdown("Sube tu archivo y nuestra IA encontrará los mejores momentos por ti.")

tab1, tab2 = st.tabs(["🎥 Clips para Videos (RRSS/Youtube)", "🍿 Clips para Películas"])

with tab1:
    st.header("Procesador de Videos Cortos")
    video_file = st.file_uploader("Sube tu video aquí", type=['mp4', 'mov', 'avi'], key="video_up")
    
    duration = st.select_slider(
        "Selecciona la duración del clip:",
        options=["30s", "1:00", "1:30"],
        key="dur_video"
    )
    
    if st.button("Generar Clips de Video"):
        st.info("Analizando los momentos más virales...")

with tab2:
    st.header("Procesador de Películas")
    movie_file = st.file_uploader("Sube la película", type=['mp4', 'mkv'], key="movie_up")
    
    movie_duration = st.select_slider(
        "Selecciona la duración del clip:",
        options=["30s", "1:00", "1:30"],
        key="dur_movie"
    )
    
    intensity = st.slider("Nivel de 'importancia' (Detección de acción/clímax)", 0, 100, 80)

    if st.button("Extraer Mejores Momentos"):
        st.info("Escaneando banda sonora y cambios de escena...")

st.sidebar.markdown("### Configuración de IA")
st.sidebar.write("Modelo: GPT-4o / Whisper / MoviePy")
