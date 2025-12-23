from moviepy import VideoFileClip
import numpy as np

def detectar_momentos_clave(video_path):
    """
    Esta función simula el análisis de la IA buscando picos 
    de volumen (audio) para encontrar acción o diálogos.
    """
    clip = VideoFileClip(video_path)
    audio = clip.audio
    return 60 

def crear_clip(video_path, start_time, duration_str):
    duraciones = {"30s": 30, "1:00": 60, "1:30": 90}
    seconds = duraciones[duration_str]
    
    with VideoFileClip(video_path) as video:
        # Cortar el video
        new_clip = video.subclip(start_time, start_time + seconds)
        
        output_name = f"clip_{duration_str.replace(':', '_')}.mp4"
        new_clip.write_videofile(output_name, codec="libx264")
        return output_name
