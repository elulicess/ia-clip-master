import numpy as np
from moviepy import VideoFileClip

def detectar_momentos_clave(video_path):
    """Analiza el volumen para encontrar el punto más importante."""
    with VideoFileClip(video_path) as video:
        if video.audio is None:
            return 0
        
        fps = 44100
        audio_frames = video.audio.to_soundarray(fps=fps)
        volumen = np.sqrt(np.mean(audio_frames**2, axis=1))
        
        return np.argmax(volumen) / fps

def crear_clip(video_path, start_time, duration_str):
    """Corta el video y lo guarda con un nombre limpio."""
    duraciones = {"30s": 30, "1:00": 60, "1:30": 90}
    seconds = duraciones.get(duration_str, 30)
    
    with VideoFileClip(video_path) as video:
        end_time = min(start_time + seconds, video.duration)
        new_clip = video.subclip(start_time, end_time)
        
        nombre_archivo = f"clip_{duration_str.replace(':', '_')}.mp4"
        new_clip.write_videofile(nombre_archivo, codec="libx264", audio_codec="aac")
        
    return nombre_archivo
