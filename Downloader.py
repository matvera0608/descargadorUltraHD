from tkinter import messagebox as mensajeDeTexto
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import re
from Subtitulation import descargar_subtítulos, limpiar_repeticiones
from Cookies import mover_cookies
# from Cookies import obtener_cookies

# Esta función lo que hace es intentar descargar la información de un video, en caso de la falla imprime con un mensaje
# y vuelve a intentar con un proxy chino (esto es útil para BiliBili que a veces falla)
# def extraer_info_seguro(url, opciones):
#     try:
#         with YoutubeDL(opciones) as ydl:
#             return ydl.extract_info(url)
#     except DownloadError as e:
#         if "BiliBili" in str(e) and "No video formats found" in str(e):
#             print("⚠ Error con el extractor BiliBili. Reintentando con proxy CN...")
#             opciones["proxy"] = "https://cn.bilibili.com"  # redirige a servidor chino
#             opciones["skip_download"] = True
#             opciones["forcejson"] = True
#             try:
#                 with YoutubeDL(opciones) as ydl:
#                     return ydl.extract_info(url)
#             except Exception as e2:
#                 print("❌ Fallback también falló:", e2)
#                 return None
#         else:
#             raise e

def optar(tipoFormato):
    match tipoFormato:
        case "mp4":
            return (
                "bestvideo+bestaudio/best",
                [
                    {"key": "FFmpegVideoRemuxer", "preferedformat": "mp4"},
                ],
            )
        case "mp3":
            return (
                    "bestaudio/best",
                    [
                        {"key": "FFmpegExtractAudio", "preferredcodec": "aac", "preferredquality": "192"},
                    ],
                )

def descargar(url, formato):
    urlHTTP = re.compile(r'^https?://([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?$')
    
    if not url.strip() or not urlHTTP.match(url):
        mensajeDeTexto.showerror("Error", "❌ URL no válida. Por favor, ingresá un enlace correcto.")
        return
    
    formatoYDL, procesoCodificación = optar(formato)
    
    ydl_opts = {
        "outtmpl": r"C:\Users\veram\Downloads\%(title)s.%(ext)s",
        "format": formatoYDL,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "nooverwrites": True,
        "postprocessors": procesoCodificación,
        "postprocessor_args": [
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k" 
            ],
        }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            mensajeDeTexto.showinfo("ÉXITO", "LA DESCARGA FUE EXITOSA")
            return {"estado": "ok", "detalle": "Descargado EXITOSAMENTE"}
    except DownloadError as excepción:
        if "No video formats found" in str(excepción):
            print("⚠ yt-dlp no pudo extraer el video. Puede estar restringido o requerir autenticación avanzada.")
        elif "Unable to download webpage" in str(excepción):
            print("\n ERROR DE CONEXIÓN en el video")
        else:
            print(f"\n Error: {excepción}")