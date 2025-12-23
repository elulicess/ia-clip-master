import numpy as np
from moviepy import VideoFileClip

def analizar_puntuacion_viral(video):
    """Simula el algoritmo de OpusClip puntuando segmentos del video."""
    if video.audio is None:
        return np.zeros(int(video.duration))
        
    fps_audio = 44100
    audio_frames = video.audio.to_soundarray(fps=fps_audio)
    
    energia = np.sqrt(np.mean(audio_frames**2, axis=1))
    
    puntuaciones = []
    for i in range(0, len(energia), fps_audio):
        bloque = energia[i : i + fps_audio]
        if len(bloque) > 0:
            puntuaciones.append(np.max(bloque))
            
    return np.array(puntuaciones)

def extraer_mejores_clips(video_path, duracion_str, max_clips=5):
    duraciones = {"30s": 30, "1:00": 60, "1:30": 90}
    duracion_seg = duraciones.get(duracion_str, 30)
    
    archivos_finales = []
    
    with VideoFileClip(video_path) as video:
        puntuaciones = analizar_puntuacion_viral(video)
        
        indices_top = np.argsort(puntuaciones)[::-1]
        
        tiempos_seleccionados = []
        for idx in indices_top:
            if len(tiempos_seleccionados) >= max_clips:
                break
            
            if all(abs(idx - t) > duracion_seg for t in tiempos_seleccionados):
                if idx + duracion_seg <= video.duration:
                    tiempos_seleccionados.append(idx)
        
        for i, t_inicio in enumerate(sorted(tiempos_seleccionados)):
            t_fin = t_inicio + duracion_seg
            
            clip = video.subclipped(t_inicio, t_fin)
            
            score_viral = min(int((puntuaciones[t_inicio] / (puntuaciones.max() + 0.0001)) * 100 + 20), 100)
            
            nombre = f"Viral_Clip_{i+1}_Score_{score_viral}.mp4"
            
            clip.write_videofile(nombre, codec="libx264", audio_codec="aac", fps=24, logger=None)
            
            archivos_finales.append({
                "path": nombre, 
                "score": score_viral,
                "timestamp": f"{int(t_inicio // 60)}:{int(t_inicio % 60):02d}"
            })
            
    return archivos_finales
