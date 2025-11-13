from tkinter import messagebox as mensajeDeTexto, filedialog as diálogo
import customtkinter as ctk
import threading as subproceso
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import re
from Subtitling import descargar_subtítulos

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


def mostrar_descarga():
    global barra, lbl_porcentaje, lbl_estado, ventanaProgreso
    
    # --- Ventana de progreso ---
    ventanaProgreso = ctk.CTkToplevel()
    ventanaProgreso.title("En proceso")
    ventanaProgreso.resizable(False, False)

    lbl_estado = ctk.CTkLabel(ventanaProgreso, text="Descargando video...", font=("Segoe UI", 20))
    lbl_estado.pack(pady=10)

    barra = ctk.CTkProgressBar(ventanaProgreso, width=250)
    barra.pack(pady=10)
    barra.set(0)

    lbl_porcentaje = ctk.CTkLabel(ventanaProgreso, text="0%", font=("Segoe UI", 10))
    lbl_porcentaje.pack(pady=5)
    
    if not all([barra, lbl_porcentaje, lbl_estado, ventanaProgreso]):
        print("⚠ La ventana de progreso no está inicializada.")
        return
    
def descargar(url, formato, subtitulos):
    urlHTTP = re.compile(r'^https?://([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?$')
    
    if not url.strip() or not urlHTTP.match(url):
        return
    
    destino = diálogo.askdirectory(title="¿Dónde querés descargar tu video?")
    if not destino:
        return
    
    
    
    formatoYDL, procesoCodificación = optar(formato)
    
    # --- Hook de progreso (definido dentro) ---
    def hook_progreso(d):
        velocidad = d.get('_speed_str', 'N/A') #Esto ayuda a mejorar la precisión de la velocidad con la que se descarga
        eta = d.get('_eta_str', 'N/A')
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            porcentaje = d['downloaded_bytes'] / total * 100 if total else 0
            tamaño_total = f"{total/1024/1024:.2f} MB"
            lbl_estado.configure(text=f"Velocidad: {velocidad} | ETA: {eta} | Total: {tamaño_total}")
            if porcentaje > 50:
                lbl_estado.configure(text=f"Más de la mitad descargada | Velocidad: {velocidad}") #Imprimimos la velocidad cuando está mayor que 50, porque es la mitad de 100
            barra.set(porcentaje / 100)
            lbl_porcentaje.configure(text=f"{porcentaje:.1f}%")
            ventanaProgreso.update_idletasks()
        elif d['status'] == 'finished':
            barra.set(1)
            lbl_porcentaje.configure(text="100%")
            lbl_estado.configure(text="✅ Descarga completada.")
            ventanaProgreso.update_idletasks()
            ventanaProgreso.after(3000, ventanaProgreso.destroy)  # cierra la ventana en 3 segundos


            
    mostrar_descarga()
    
    ydl_opts = {
        "outtmpl": destino + "/%(title)s.%(ext)s",
        "format": formatoYDL,
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [hook_progreso],
        "show_progress": False,
        "noplaylist": True,
        "nooverwrites": True,
        "postprocessors": procesoCodificación,
        "postprocessor_args": [
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k" 
            ],
        }
    
  

    if subtitulos:
        try:
            print("DESCARGANDO SUBTÍTULOS")
            descargar_subtítulos(destino)
        except Exception as e:
            print(f"ERROR INESPERADO AL DESCARGAR SUBTÍTULOS: {e}")
            
    def tarea():
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                mensajeDeTexto.showinfo("ÉXITO", "LA DESCARGA FUE EXITOSA")
        except DownloadError as excepción:
            if "No video formats found" in str(excepción):
                print("⚠ yt-dlp no pudo extraer el video. Puede estar restringido o requerir autenticación avanzada.")
            elif "Unable to download webpage" in str(excepción):
                print("\n ERROR DE CONEXIÓN en el video")
            else:
                print(f"\n Error: {excepción}")
    
    subproceso.Thread(target=tarea, daemon=True)
            