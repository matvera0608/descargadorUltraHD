from tkinter import filedialog as diálogo
import threading as subproceso
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import os
from Subtitling import procesar_subtítulos
from Cookies import *
from Elementos import *
from yt_dlp_UPDATES import *

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

def optar(tipoFormato, plataforma):
    match tipoFormato:
        case "mp4":
            if plataforma == "bilibili":
                return {
                    "format": "bestvideo+bestaudio/best",
                    "postprocessors": [],
                    "merge": False
                }
            else:
                return {
                    "format": (
                        "bestvideo+bestaudio/"
                        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"
                    ),
                    "postprocessors": [],
                    "merge": False
                }

        case "mp3":
            return {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192"
                    }
                ],
                "merge": False
            }

def descargar(ventana, url, formato, subtitulos):
    es_de_bilibili = "bilibili" in url.lower()    
    destino = diálogo.askdirectory(title="¿Dónde querés descargar tu video?")
    if not destino:
        return

    plantilla = os.path.join(destino, "%(title)s.mp4")
    
    configuración = optar(formato, "bilibili" if es_de_bilibili else "otra") # Obtener configuración según formato y plataforma, Bilibili cambia constantemente de backend, por eso se detecta especialmente cuando descargo un stream de alta calidad.
    formatoYDL = configuración["format"]
    proceso_de_codificación = configuración["postprocessors"]
    merge_output = configuración["merge"]
    
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

    ydl_opts = {
                "outtmpl": plantilla,
                "format": formatoYDL,
                "quiet": True,
                "no_warnings": True,
                "show_progress": False,
                "progress_hooks": [hook_progreso],
                "noplaylist": True,
                "nooverwrites": True,
                "postprocessors": proceso_de_codificación if merge_output else [],
                }

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
                ydl.download([url])
                info = ydl.extract_info(url, download=True)  # ✅ ahora sí devuelve info
                plataforma = detectar_plataforma(url)
                calidad = clasificar_calidad(info, plataforma)
                mostrar_aviso(ventana, f"Descarga completada exitosamente\n con {calidad} calidad", colors["successfully"])
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