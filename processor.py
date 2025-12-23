import numpy as np
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import whisper
import os

model = whisper.load_model("base")

def detectar_momentos_clave(video_path):
    with VideoFileClip(video_path) as video:
        if video.audio is None: return 0
        audio_frames = video.audio.to_soundarray(fps=44100)
        volumen = np.sqrt(np.mean(audio_frames**2, axis=1))
        return np.argmax(volumen) / 44100

def crear_clip(video_path, start_time, duration_str):
    duraciones = {"30s": 30, "1:00": 60, "1:30": 90}
    seconds = duraciones.get(duration_str, 30)
    
    with VideoFileClip(video_path) as video:
        end_time = min(start_time + seconds, video.duration)
        clip = video.subclip(start_time, end_time)
        
        temp_clip_name = "temp_for_whisper.mp4"
        clip.write_videofile(temp_clip_name, codec="libx264", audio_codec="aac")
        
        print("Escuchando diálogos...")
        result = model.transcribe(temp_clip_name)
        texto_detectado = result['text'].strip()

        if texto_detectado:
            txt_clip = TextClip(
                txt=texto_detectado,
                fontsize=70,
                color='yellow',
                method='caption',
                size=(clip.w*0.8, None)
            ).set_start(0).set_duration(clip.duration).set_position(('center', 'bottom'))
            

            final_clip = CompositeVideoClip([clip, txt_clip])
        else:
            final_clip = clip

        output_name = f"clip_con_ia_{duration_str.replace(':', '_')}.mp4"
        final_clip.write_videofile(output_name, codec="libx264")
        
    return output_name
