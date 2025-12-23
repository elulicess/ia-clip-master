import yt_dlp
import os
import time
import glob
from moviepy import VideoFileClip
import numpy as np

def limpiar_archivos_antiguos():
    ahora = time.time()
    for f in glob.glob("*.mp4"):
        if os.stat(f).st_mtime < ahora - 600: # 10 minutos
            try:
                os.remove(f)
            except:
                pass

def descargar_video_url(url):
    limpiar_archivos_antiguos()
    id_video = int(time.time())
    output_path = f"video_{id_video}.mp4"
    
    ydl_opts = {
        'format': 'b[ext=mp4]/w[ext=mp4]/5/best', 
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        if "ffmpeg" in str(e).lower():
            print("Reintentando con formato de emergencia...")
            ydl_opts['format'] = 'worst'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return output_path
        raise e

def extraer_mejores_clips(video_path, duracion_str, max_clips=3):
    duraciones = {"30s": 30, "1:00": 60, "1:30": 90}
    segundos = duraciones.get(duracion_str, 30)
    clips_info = []

    with VideoFileClip(video_path) as video:
        fps_audio = 44100
        audio = video.audio.to_soundarray(fps=fps_audio)
        energia = np.sqrt(np.mean(audio**2, axis=1))
        
        puntos_inicio = []
        segmento = len(energia) // max_clips
        for i in range(max_clips):
            inicio = i * segmento
            fin = (i + 1) * segmento
            pico = np.argmax(energia[inicio:fin]) + inicio
            puntos_inicio.append(pico / fps_audio)

        for i, t_start in enumerate(puntos_inicio):
            t_end = min(t_start + segundos, video.duration)
            nombre_clip = f"clip_viral_{i+1}.mp4"
            
            nuevo_clip = video.subclipped(t_start, t_end)
            nuevo_clip.write_videofile(nombre_clip, codec="libx264", audio_codec="aac", logger=None)
            
            clips_info.append({
                "path": nombre_clip,
                "timestamp": f"{int(t_start//60)}:{int(t_start%60):02d}"
            })
            
    return clips_info
