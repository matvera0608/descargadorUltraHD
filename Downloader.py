from tkinter import filedialog as diálogo
import threading as subproceso
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import os
from Subtitling import procesar_subtítulos
from Cookies import *
from Elementos import *
from yt_dlp_UPDATES import *

def optar(tipoFormato):
    match tipoFormato:

        case "mp4":
            return {
                "format": (
                    "bestvideo+bestaudio/"
                    "bestvideo[ext=mp4]+bestaudio[ext=m4a]/"
                    "best"
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
    
    configuración = optar(formato)
    formatoYDL = configuración["format"]
    proceso_de_codificación = configuración["postprocessors"]
    merge_output = configuración["merge"]
    
    mostrar_descarga()
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
        if subtitulos:
            mostrar_aviso(ventana, "Se descargará el video junto con los subtítulos...", colors["text"])
        else:
            mostrar_aviso(ventana, "Se descargará el video...", colors["text"])

    ydl_opts = {
                "outtmpl": plantilla,
                "format": formatoYDL,
                "quiet": True,
                "no_warnings": True,
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
                mostrar_aviso(ventana, "Descarga completada con éxito.", colors["successfully"])
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