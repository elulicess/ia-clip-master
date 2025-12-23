import numpy as np
from moviepy import VideoFileClip

def detectar_momentos_clave(video_path):
    clip = VideoFileClip(video_path) 
    
    audio = clip.audio
    fps = 44100
    audio_frames = audio.to_soundarray(fps=fps)
    
    volumen = np.sqrt(np.mean(audio_frames**2, axis=1))
    
    segundo_maximo = np.argmax(volumen) / fps
    
    clip.close()
    return segundo_maximo
