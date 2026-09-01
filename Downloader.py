from tkinter import filedialog as diálogo
import threading
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import os
from Subtitling import procesar_subtítulos
from Encoding import *
from Cookies import *
from Elementos import *
from yt_dlp_UPDATES import *
from FFMPEG import descargar_FFMPEG
from web.Internet import verificar_conexión_a_internet

BASE_YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "retries": 10,
    "fragment_retries": 10,
    "skip_unavailable_fragments": True,
    "concurrent_fragment_downloads": 1,
}


def obtener_ruta_ffmpeg(ventana, color=None):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    
    
    carpeta_ffmpeg = os.path.join(base_path, "ffmpeg")
    
    ffmpeg_path = os.path.join(carpeta_ffmpeg, "ffmpeg.exe")
    
    if os.path.exists(ffmpeg_path):
        return ffmpeg_path

    
    actualizar_progreso, actualizar_estado, frame = mostrar_descarga_FFMPEG(ventana, color) #Acá es donde me está tirando un error
    
    return descargar_FFMPEG(progreso=actualizar_progreso, estado=actualizar_estado)


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


def ydl_opts_descargar_audio_mp3(plantilla, hook_progreso):
           
    opts = BASE_YDL_OPTS.copy()
    
    opts.update({
        "outtmpl": plantilla,
        # "format": "bestvideo+bestaudio/best",
        "progress_hooks": [hook_progreso],
        "merge_output_format": "mp4",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],
    })
    
    return opts


def ydl_opts_descargar_video_mp4(plantilla, hook_progreso):
    
    opts = BASE_YDL_OPTS.copy()

    opts.update({
        "outtmpl": plantilla,
        # "format": "bestvideo+bestaudio/best",
        "progress_hooks": [hook_progreso],
        "merge_output_format": "mp4",
    })
    
    return opts

descarga_en_proceso = False
cancelado = False

def descargar(ventana, url, modo_descarga, subtitulos):
    global cancelado, descarga_en_proceso
    
    if descarga_en_proceso:
        mostrar_aviso(ventana, "Hay una descarga en proceso", colors["alert"])
        return
    
    cancelado = False
    
    print("🟢 NUEVA DESCARGA")
    

    es_de_bilibili = "bilibili" in url.lower()    
    destino = diálogo.askdirectory(title="¿Dónde querés descargar tu video?")
    if not destino:
        return
    
    descarga_en_proceso = True
    
    ventana_de_descarga = None
    
    try:
    
        plantilla = os.path.join(destino, "%(title)s.%(ext)s")
        
        ruta_FFMPEG = obtener_ruta_ffmpeg(ventana)
        
        ydl_opts = (
            ydl_opts_descargar_audio_mp3(plantilla, hook_progreso)
            if modo_descarga == "mp3"
            else ydl_opts_descargar_video_mp4(plantilla, hook_progreso)
        )
        
        print("YDLOPTS:")
        print(ydl_opts)
        
        ##Si tengo así el diccionario ydl_opts arriba del if donde verifica la ruta del FFMPEG, ¿Tirará algún error posible a la hora de ejecutar?
        ydl_opts.update({
            "quiet": True,
            "nopart": False,
            "outtmpl": plantilla,
            "progress_hooks": [hook_progreso],
            # "js_runtimes": {"node": {}}, 
        })
        if ruta_FFMPEG:
            ydl_opts["ffmpeg_location"] = ruta_FFMPEG

        ruta_cookie = None
        
        if es_de_bilibili:
            ruta_cookie = procesar_cookies()
            ydl_opts.update({
                "cookiefile": ruta_cookie if ruta_cookie else None,
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Referer": "https://www.bilibili.com/",
                },
            })
        
        ventana_de_descarga = mostrar_descarga(ventana)
    
    #Errores relacionados a la preparación de descarga
    except Exception as e:
        print("ERROR:", e)
        
        ventana.after(2000, lambda: cerrar_seguro(ventana_de_descarga))
        mostrar_aviso(ventana, "Error al preparar la descarga", colors["error"])
    
    def tarea():
        global descarga_en_proceso
        try:
            with YoutubeDL(ydl_opts) as ydl: #type: ignore
                
                print("🔎 ANTES DE EXTRACT_INFO")
                print("cancelado =", cancelado)
                print("hook activo =", getattr(hook_progreso, "activo", None))
                print("archivo actual =", getattr(hook_progreso, "archivo_actual", None))
                
                # print("▶️ Ejecutando extract_info()")
                
                info = ydl.extract_info(url, download=True)
                
                #La descarga se cancela
                if cancelado:
                    return
                
                # print("✅ extract_info() terminó correctamente")
                
                archivo_final = ydl.prepare_filename(info)
            
            #Post procesamiento
            
            if modo_descarga == "mp3":
                mostrar_aviso(ventana, f"Audio descargado", colors["successfully"])
                
            if necesitar_decodificación(info):
                archivo_final = decodificar_video(archivo_final)
                mostrar_aviso(ventana, "Video decodificado", colors["successfully"])
            else:
                mostrar_aviso(ventana, f"Video descargado", colors["successfully"])
                
            
            # if subtitulos:
            #     procesar_subtítulos(ventana, url, destino, ruta_cookie)
            #     mostrar_aviso(ventana, "Se descargará el video junto con los subtítulos...", colors["text"])
            # else:
            #     mostrar_aviso(ventana, "Se descargará el video...", colors["text"])
        
        # Errores inesperados propios de yt-dlp
        except DownloadError as e:
            print("ERROR DE YT-DLP:", e)

            print("🔴 cancelado =", cancelado)
            print("🔴 hook activo =", getattr(hook_progreso, "activo", None))
            print("🔴 archivo actual =", getattr(hook_progreso, "archivo_actual", None))
            ventana.after(2000, lambda: cerrar_seguro(ventana_de_descarga))
        
            archivo_actual = getattr(hook_progreso, "archivo_actual", None)

            if archivo_actual:
                limpiar_residuales(archivo_actual)
            
            if cancelado:
                mostrar_aviso(ventana, "Descarga cancelada", colors["error"])
                
            elif not verificar_conexión_a_internet():
                mostrar_aviso(ventana, "No hay conexión a Internet", colors["error"])
            else:
                mostrar_aviso(ventana, "Error en la descarga", colors["error"])
        
        #Errores genéricos
        except Exception as e:
            print("ERROR:", e)
            
            print("🔴 cancelado =", cancelado)
            print("🔴 hook activo =", getattr(hook_progreso, "activo", None))
            print("🔴 archivo actual =", getattr(hook_progreso, "archivo_actual", None))
            
            ventana.after(2000, lambda: cerrar_seguro(ventana_de_descarga))
            if cancelado:
                mostrar_aviso(ventana, "Descarga cancelada", colors["error"])
            else:
                mostrar_aviso(ventana, "Ocurrió un error inesperado", colors["error"])
        finally:
            if ventana_de_descarga is not None:
                def finalizar_operación():
                    global descarga_en_proceso
                    cerrar_seguro(ventana_de_descarga)

                    hook_progreso.activo = False
                    hook_progreso.archivo_actual = None

                    descarga_en_proceso = False

                    print("⚪ Descarga finalizada")

                # Le damos tiempo a que termine
                # la limpieza y los callbacks pendientes.

                ventana.after(2000, finalizar_operación)

            else:
                # Seguridad por si nunca llegó a crearse
                # la ventana de descarga.

                descarga_en_proceso = False

                print("⚪ Descarga finalizada")
            
    threading.Thread(target=tarea, daemon=True).start()