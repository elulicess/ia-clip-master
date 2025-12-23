import numpy as np
from moviepy import VideoFileClip

def detectar_momentos_clave(video_path):
    """Analiza el volumen para encontrar el punto con más sonido."""
    with VideoFileClip(video_path) as video:
        if video.audio is None:
            return 0
        
        fps_audio = 44100
        audio_frames = video.audio.to_soundarray(fps=fps_audio)
        
        volumen = np.sqrt(np.mean(audio_frames**2, axis=1))
        
        return np.argmax(volumen) / fps_audio

def crear_clip(video_path, start_time, duration_str):
    """Recorta el video basándose en el tiempo de inicio y la duración elegida."""
    duraciones = {"30s": 30, "1:00": 60, "1:30": 90}
    seconds = duraciones.get(duration_str, 30)
    
    with VideoFileClip(video_path) as video:
        end_time = min(start_time + seconds, video.duration)
        new_clip = video.subclip(start_time, end_time)
        
        output_name = f"clip_{duration_str.replace(':', '_')}.mp4"
        
        new_clip.write_videofile(output_name, codec="libx264", audio_codec="aac")
        
    return output_name
