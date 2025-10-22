from tkinter import messagebox as mensajeDeTexto, filedialog as diálogo, ttk as tkModerno
import tkinter as tk
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import re
from Subtitulation import descargar_subtítulos, limpiar_repeticiones
from Cookies import mover_cookies

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



##from tkinter import ttk as tkModerno. tkModerno se llama porque está aliasado con ttk
##Esta función mostrar se enfocará de hacer lo siguiente:
#A la hora de presionar descargar tirará un diálogo de descargando el video
#Pero usando el time.sleep() con un número variable del tipo de video que se descargará

def mostrar_descarga(url, formato):
    global barra, lbl_porcentaje, lbl_estado, ventanaProgreso
    if not all([barra, lbl_porcentaje, lbl_estado, ventanaProgreso]):
        print("⚠ La ventana de progreso no está inicializada.")
        return
    # --- Ventana de progreso ---
    ventanaProgreso = tk.Toplevel()
    ventanaProgreso.title("En proceso")
    ventanaProgreso.geometry("350x180")
    ventanaProgreso.resizable(False, False)

    lbl_estado = tk.Label(ventanaProgreso, text="Descargando video...", font=("Segoe UI", 11))
    lbl_estado.pack(pady=10)

    barra = tkModerno.Progressbar(ventanaProgreso, orient="horizontal", length=250, mode="determinate", maximum=100)
    barra.pack(pady=10)

    lbl_porcentaje = tk.Label(ventanaProgreso, text="0%", font=("Segoe UI", 10))
    lbl_porcentaje.pack(pady=5)


def descargar(url, formato):
    urlHTTP = re.compile(r'^https?://([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?$')
    
    if not url.strip() or not urlHTTP.match(url):
        return
    
    destino = diálogo.askdirectory(title="¿Dónde querés descargar tu video?")
    if not destino:
        return
    
    mostrar_descarga(url, formato)
    
    formatoYDL, procesoCodificación = optar(formato)
    
    
    # --- Hook de progreso (definido dentro) ---
    def hook_progreso(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total:
                porcentaje = d['downloaded_bytes'] / total * 100
                barra['value'] = porcentaje
                lbl_porcentaje.config(text=f"{porcentaje:.1f}%")
                ventanaProgreso.update_idletasks()
        elif d['status'] == 'finished':
            barra['value'] = 100
            lbl_porcentaje.config(text="100%")
            lbl_estado.config(text="✅ Descarga completada.")
            ventanaProgreso.update_idletasks()

    
    ydl_opts = {
        "outtmpl": destino + "/%(title)s.%(ext)s",
        "format": formatoYDL,
        "merge_output_format": "mp4",
        "progress_hooks": [hook_progreso],
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