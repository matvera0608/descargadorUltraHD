from yt_dlp import YoutubeDL
import pysrt
from deep_translator import GoogleTranslator

def listar_lenguas(url): #Esta función se encarga de listar los idiomas de los subtítulos disponibles:  para ello usa yt-dlp, YouTube Downloader Plus
    global info
    ydl_opts_info = {"listsubtitles": True}
    with YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
        
    subtítulos = info.get("subtitles", {})
    subtítulos_automáticos = info.get("automatic_captions", {})
    
    
    idiomas_disponibles = {}
    
    for lang in subtítulos:
        idiomas_disponibles[lang] = "Manual"
    
    for lang in subtítulos_automáticos:
        if lang not in idiomas_disponibles:
            idiomas_disponibles[lang] = "Automatico"
    
    return idiomas_disponibles