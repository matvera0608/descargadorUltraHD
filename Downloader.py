from tkinter import filedialog as diálogo
import threading as subproceso
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import os
from Subtitling import procesar_subtítulos
from Cookies import *
from Elementos import *
from yt_dlp_UPDATES import *

def ydl_opts_descargar_audio_mp3(plantilla, hook_progreso):
    return {
        "outtmpl": plantilla,
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "show_progress": False,
        "progress_hooks": [hook_progreso],
        "noplaylist": True,
        "nooverwrites": True,

        # 🎧 MP3 SIEMPRE
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

def ydl_opts_descargar_video_mp4(plantilla, hook_progreso):
    return {
            "outtmpl": plantilla,
            "format": "bestvideo+bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "show_progress": False,
            "progress_hooks": [hook_progreso],
            "noplaylist": True,
            "nooverwrites": True,

            # 🔥 CLAVE DEL DESCARGADOR CONSISTENTE
            "merge_output_format": "mp4",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
        }



def detectar_plataforma(link_de_archivo):
    link_de_archivo = link_de_archivo.lower()

    if "youtube.com" in link_de_archivo or "youtu.be" in link_de_archivo:
        return "youtube"
    if "bilibili.com" in link_de_archivo or "b23.tv" in link_de_archivo:
        return "bilibili"
    if "douyin.com" in link_de_archivo or "iesdouyin.com" in link_de_archivo:
        return "douyin"
    if "tiktok.com" in link_de_archivo:
        return "tiktok"
    if "instagram.com" in link_de_archivo or "instagr.am" in link_de_archivo:
        return "instagram"
    if "facebook.com" in link_de_archivo or "fb.watch" in link_de_archivo:
        return "facebook"
    if "twitter.com" in link_de_archivo or "x.com" in link_de_archivo:
        return "twitter"

    return "default"

def clasificar_calidad(info, plataforma="default"):
    formato = info.get("formats", [])
    mejor = None
    

    for f in formato:
        if f.get("vcodec") != "none":
            if not mejor or (f.get("tbr", 0) or 0) > (mejor.get("tbr", 0) or 0):
                mejor = f
                
    if not mejor:
        return "Desconocido"
    
    
    altura = mejor.get("height") or 0
    tbr = mejor.get("tbr") or 0
    fps = mejor.get("fps") or 30

    if fps >= 50:
        peso_fps = 1.08
    elif fps >= 30:
        peso_fps = 1.00
    else:
        peso_fps = 0.92

    
    resolución_base_real = altura
    
    perfil_plataforma = CALIDAD_DE_VIDEO.get(plataforma, CALIDAD_DE_VIDEO["default"])

    
    if resolución_base_real >= 2160:
       resultado_en_texto = "2160"
    elif resolución_base_real >= 1440:
        resultado_en_texto = "1440"
    elif resolución_base_real >= 1080:
        resultado_en_texto = "1080"
    elif resolución_base_real >= 720:
        resultado_en_texto = "720"
    elif resolución_base_real >= 540:
        resultado_en_texto = "540"
    else:
        resultado_en_texto = "480"
        
        
    print("tbr:", tbr)
    print("resolución_base_real:", resolución_base_real)
    

    codec = mejor.get("vcodec", "")
    peso_codec = 1.0

    for clave, peso in PESO_CODEC.items():
        if codec.startswith(clave):
            peso_codec = peso
            break

    tbr_perceptual = tbr * peso_codec * peso_fps #Ahora puse que considere el fps para que detecte la calidad real sin falsear mensajes

    
    perfil = perfil_plataforma.get(int(resultado_en_texto))
    
    # Clasificación dinámica
    if tbr_perceptual >= perfil["excelente"]:
        return "Excelente"
    elif tbr_perceptual >= perfil["buena"]:
        return "Buena"
    elif tbr_perceptual >= perfil["regular"]:
        return "Regular"
    elif tbr_perceptual >= perfil["mala"]:
        return "Mala"
    else:
        return "Muy mala"
    
def imprimir_calidad_real(info, url):
    formato = info.get("formats", [])

    mejor = None
    for f in formato:
        if f.get("vcodec") != "none":
            if not mejor or (f.get("tbr", 0) or 0) > (mejor.get("tbr", 0) or 0):
                mejor = f

    if not mejor:
        print("No se encontró stream de video válido.")
        return


    width = mejor.get("width")
    height = mejor.get("height")
    vcodec = mejor.get("vcodec")
    tbr = mejor.get("tbr") or 0
    fps = mejor.get("fps")
    fid = mejor.get("format_id")
    
    plataforma = detectar_plataforma(url)

    print("=== CALIDAD REAL DETECTADA CON LA PLATAFORMA ===")
    print(f"Plataforma : {plataforma}")
    print(f"Resolución : {width} x {height}")
    print(f"Códec      : {vcodec}")
    print(f"Bitrate    : {tbr} kbps")
    print(f"FPS        : {fps}")
    print(f"Formato ID : {fid}")


def descargar(ventana, url, modo_descarga, subtitulos):
    es_de_bilibili = "bilibili" in url.lower()    
    destino = diálogo.askdirectory(title="¿Dónde querés descargar tu video?")
    if not destino:
        return
    
    if modo_descarga == "audio":
        plantilla = os.path.join(destino, "%(title)s.mp3")
    else:
        plantilla = os.path.join(destino, "%(title)s.mp4")

    
    # ------------------------------------------
    # Verificar si el archivo ya existe antes de descargar
    archivo_existe = False
    try:
        with YoutubeDL({"skip_download": True, "quiet": True, "logger": None, "no_warnings": True, "outtmpl": plantilla, "show_progress": False}) as ydl:
            info = ydl.extract_info(url, download=False)
            nombre_prueba = ydl.prepare_filename(info)
    except Exception as e:
        print(f"No se pudo extraer info: {e}")
        nombre_prueba = os.path.join(destino, "video.mp4")


    if os.path.exists(nombre_prueba): #Este es verdadero cuando intento de descargar un arachivo existente
        archivo_existe = True
        
        if subtitulos:
            mostrar_aviso(ventana, "El archivo ya existe.\nSe descargarán los subtítulos si están disponibles...", colors["alert"])
            ventana.update_idletasks()
        else:
            mostrar_aviso(ventana, "El archivo ya existe.\nNo se descargará nada.", colors["alert"])
            print("El archivo ya existe. No se descargará nada.")
            cerrar_seguro(ventanaProgreso)
            return
    else:
        mostrar_descarga()
        if subtitulos:
            mostrar_aviso(ventana, "Se descargará el video junto con los subtítulos...", colors["text"])
        else:
            mostrar_aviso(ventana, "Se descargará el video...", colors["text"])
    
    if modo_descarga == "audio":
        ydl_opts = ydl_opts_descargar_audio_mp3(plantilla, hook_progreso)
    else:
        ydl_opts = ydl_opts_descargar_video_mp4(plantilla, hook_progreso)
    
    if es_de_bilibili: #Este es para bilibili, porque la plataforma requiere cookies para descargar subtítulos.
        ydl_opts.update({
            "cookiefile": carpeta_destino_cookies,
            "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://www.bilibili.com/",
                            },
                        })

    if subtitulos:
        procesar_subtítulos(ventana, url, destino, ventanaProgreso)

    if archivo_existe:
        cerrar_seguro(ventanaProgreso)
        return
            
    def tarea():
        try:
            with YoutubeDL(ydl_opts) as ydl:
                
                info = ydl.extract_info(url, download=True)  # ✅ ahora sí devuelve info
                plataforma = detectar_plataforma(url)
                calidad = clasificar_calidad(info, plataforma)
                if modo_descarga == "audio":
                    mostrar_aviso(ventana, "Descarga de audio completada (MP3)", colors["successfully"])
                else:
                    mostrar_aviso(ventana, f"Descarga completada con {calidad} calidad", colors["successfully"])
                imprimir_calidad_real(info, url)
        except DownloadError:
            print(f"\n Error")
        finally:
            try:
                if ventanaProgreso and ventanaProgreso.winfo_exists():
                    ventanaProgreso.after(100, ventanaProgreso.destroy)
                    # print("ventanaProgreso:", ventanaProgreso, "existe:", ventanaProgreso.winfo_exists() if ventanaProgreso else None)
            except tk.TclError:
                pass
            
    subproceso.Thread(target=tarea, daemon=True).start()