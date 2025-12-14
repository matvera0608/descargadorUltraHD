from tkinter import filedialog as diálogo
import threading as subproceso
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import os
from Subtitling import procesar_subtítulos
from Cookies import *
from Elementos import *
from yt_dlp_UPDATES import *

def clasificar_calidad(info):
    formato = info.get("formats", [])
    mejor = None
    
    for f in formato:
        if f.get("vcodec") != "none":
            if not mejor or (f.get("tbr", 0) or 0) > (mejor.get("tbr", 0) or 0):
                mejor = f
                
    if not mejor:
        return "Desconocido"
    
    anchura = mejor.get("width") or 0
    altura = mejor.get("height") or 0

    es_vertical = altura > anchura
    tbr = mejor.get("tbr") or 0
    
    if es_vertical:
        resolución_base_real = min(anchura, altura)
    else:
        resolución_base_real = max(anchura, altura)
    
    
    if resolución_base_real >= 2160:
        perfil = CALIDAD_DE_VIDEO[2160]
    elif resolución_base_real >= 1440:
        perfil = CALIDAD_DE_VIDEO[1440]
    elif resolución_base_real >= 1080:
        perfil = CALIDAD_DE_VIDEO[1080]
    elif resolución_base_real >= 720:
        perfil = CALIDAD_DE_VIDEO[720]
    else:
        perfil = CALIDAD_DE_VIDEO[480]

    # Clasificación dinámica
    if tbr >= perfil["excelente"]:
        return "Excelente"
    elif tbr >= perfil["buena"]:
        return "Buena"
    elif tbr >= perfil["regular"]:
        return "Regular"
    elif tbr >= perfil["mala"]:
        return "Mala"
    else:
        return "Muy mala"
      
def imprimir_calidad_real(info):
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

    print("=== CALIDAD REAL DETECTADA CON LA PLATAFORMA ===")
    print(f"Resolución : {width} x {height}")
    print(f"Códec      : {vcodec}")
    print(f"Bitrate    : {tbr} kbps")
    print(f"FPS        : {fps}")
    print(f"Formato ID : {fid}")

    if tbr and height:
        if height >= 1080 and tbr < 500:
            print("⚠️ Advertencia: 1080p con bitrate muy bajo (calidad pobre)")
        elif height >= 720 and tbr < 1000:
            print("⚠️ Advertencia: bitrate bajo para HD")

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
        with YoutubeDL({"skip_download": True, "quiet": True, "logger": None, "no_warnings": True, "outtmpl": plantilla}) as ydl:
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
                calidad = clasificar_calidad(info)
                mostrar_aviso(ventana, f"Descarga completada exitosamente\n con {calidad} calidad", colors["successfully"])
                imprimir_calidad_real(info)
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