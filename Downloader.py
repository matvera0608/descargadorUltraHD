from tkinter import filedialog as diálogo
import tkinter as tk
import customtkinter as ctk
import threading as subproceso
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import re, os
from Subtitling import descargar_subtítulos
from Cookies import *
from Elementos import *
from yt_dlp_UPDATES import *

def limpiar_ansi(texto):
    """Elimina los códigos ANSI (colores de consola) del texto."""
    if not texto:
        return texto
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', texto)

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

def descargar(ventana, url, formato, subtitulos):
    es_de_bilibili = "bilibili" in url.lower()    
    destino = diálogo.askdirectory(title="¿Dónde querés descargar tu video?")
    if not destino:
        return
    
    plantilla = os.path.join(destino, "%(title)s.mp4")
    
    formatoYDL, procesoCodificación = optar(formato)
    
    mostrar_descarga()
    
    # --- Hook de progreso (definido dentro) --- El hook es una función que se llama periódicamente
    # durante la descarga para actualizar la interfaz de usuario
    def hook_progreso(d):
        try:
            temp_file = d.get('filename')
            velocidad = limpiar_ansi(d.get('_speed_str', 'N/A')) #Esto ayuda a mejorar la precisión de la velocidad con la que se descarga
            eta = limpiar_ansi(d.get('_eta_str', 'N/A'))
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                porcentaje = (d['downloaded_bytes'] / total) * 100 if total else 0
                descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_estado.configure(text=f"Velocidad: {velocidad} | ETA: {eta}"))
                if porcentaje >= 50:
                    descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_estado.configure(text=f"Más de la mitad descargada | Velocidad: {velocidad}")) #Imprimimos la velocidad cuando está mayor que 50, porque es la mitad de 100
                descarga_segura_resistente_a_fallos(barra, lambda: barra.set(porcentaje / 100))
                descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_porcentaje.configure(text=f"{porcentaje:.1f}%"))
            elif d['status'] == 'finished':
                descarga_segura_resistente_a_fallos(barra, lambda: barra.set(1))
                descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_porcentaje.configure(text="100%"))
                descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_estado.configure(text="✅ Descarga completada."))
                if ventanaProgreso and ventanaProgreso.winfo_exists(): #Ahora ejecuta el cierre de la ventana de progreso cuando la descarga se completa o cancela
                    ventanaProgreso.after(1500, ventanaProgreso.destroy)
            else:
                descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_estado.configure(text="❌ Descarga fallida."))
                if ventanaProgreso and ventanaProgreso.winfo_exists():
                    ventanaProgreso.after(1500, ventanaProgreso.destroy)
                    if temp_file and os.path.exists(temp_file) and temp_file.endswith('.part'):
                        try:
                            os.remove(temp_file)
                        except Exception as e:
                            print(f"No se pudo eliminar el archivo temporal: {e}")
                            
        except Exception as e:
            print(f"Error en el hook de progreso: {e}")
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"No se pudo eliminar el archivo temporal: {e}")

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
        
    if os.path.exists(nombre_prueba):
        archivo_existe = True
        
        if subtitulos:
            mensaje = "El archivo ya existe.\nSe descargarán los subtítulos..."
        else:
            mensaje = "El archivo ya existe.\nNo se descargará nada."

        mostrar_aviso(ventana, mensaje, colors["alert"])
        
        try:
            if ventanaProgreso and ventanaProgreso.winfo_exists():
                ventanaProgreso.after(100, ventanaProgreso.destroy)
        except tk.TclError:
            pass


        
        if not subtitulos: # este not es para que si el archivo ya existe pero se quieren descargar subtítulos, lo permita.
            return
    
    ydl_opts = {
        "outtmpl": plantilla,
        "format": formatoYDL,
        "quiet": True,
        "logger": None,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "progress_hooks": [hook_progreso],
        "show_progress": False,
        "noplaylist": True,
        "nooverwrites": True,
        "postprocessors": procesoCodificación,
        "keepvideo": False,
        "postprocessor_args": [
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k" 
            ],
        }
    
    if es_de_bilibili: #Este es para bilibili, porque la plataforma requiere cookies para descargar subtítulos.
        ydl_opts.update({
            "cookiefile": carpeta_destino_cookies,
            "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://www.bilibili.com/",
            }
        })
    
    if subtitulos:
        try:
            descarga_exitosa = descargar_subtítulos(ventana, url, destino)
            if descarga_exitosa:
                mostrar_aviso(ventana, "SUBTÍTULO DESCARGADO CORRECTAMENTE", colors["successfully"])
            elif descarga_exitosa is None:
                pass
            else:
                mostrar_aviso(ventana, "ERROR AL DESCARGAR SUBTÍTULO", colors["danger"])
        except Exception as e:
            ventanaProgreso.after(100, ventanaProgreso.destroy)
            print(f"Error al descargar subtítulos: {e}")
            return False
    
    if archivo_existe:
        try:
            ventanaProgreso.destroy()
        except tk.TclError:
            pass
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
            except tk.TclError:
                pass
            
    subproceso.Thread(target=tarea, daemon=True).start()