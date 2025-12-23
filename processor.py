import numpy as np
from moviepy import VideoFileClip

def detectar_varios_momentos(video_path, num_clips=3):
    """Busca los N momentos con más volumen que no estén pegados entre sí."""
    with VideoFileClip(video_path) as video:
        if video.audio is None:
            return [0]
        
        fps_audio = 44100
        audio_frames = video.audio.to_soundarray(fps=fps_audio)
        volumen = np.sqrt(np.mean(audio_frames**2, axis=1))
        
        duracion_total = video.duration
        puntos_inicio = []
        
        segmento = len(volumen) // num_clips
        for i in range(num_clips):
            inicio_seg = i * segmento
            fin_seg = (i + 1) * segmento
            punto_max = np.argmax(volumen[inicio_seg:fin_seg]) + inicio_seg
            puntos_inicio.append(punto_max / fps_audio)
            
        return puntos_inicio

def crear_clips_lote(video_path, puntos_inicio, duration_str):
    """Genera varios archivos de video basados en los puntos de inicio."""
    duraciones = {"30s": 30, "1:00": 60, "1:30": 90}
    seconds = duraciones.get(duration_str, 30)
    archivos_creados = []
    
    with VideoFileClip(video_path) as video:
        for i, start_time in enumerate(puntos_inicio):
            end_time = min(start_time + seconds, video.duration)
            new_clip = video.subclipped(start_time, end_time)
            
            output_name = f"clip_{i+1}_{duration_str.replace(':', '_')}.mp4"
            new_clip.write_videofile(output_name, codec="libx264", audio_codec="aac")
            archivos_creados.append(output_name)
            
    return archivos_creados
