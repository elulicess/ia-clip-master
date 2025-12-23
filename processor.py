import yt_dlp
import os
import time
import glob
from moviepy import VideoFileClip
import numpy as np

def limpiar_archivos_antiguos():
    """Borra archivos mp4 creados hace más de 15 minutos para liberar espacio."""
    ahora = time.time()
    archivos = glob.glob("*.mp4")
    for archivo in archivos:
        if os.stat(archivo).st_mtime < ahora - 900:
            try:
                os.remove(archivo)
            except:
                pass

def descargar_video_url(url):
    limpiar_archivos_antiguos()
    output_path = f"video_{int(time.time())}.mp4"
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return output_path
