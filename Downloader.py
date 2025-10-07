from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from yt_dlp.utils import sanitize_filename
import os, glob, string, re
from Subtitulation import descargar_subtítulos, limpiar_repeticiones
from Cookies import obtener_cookies

def obtenerURL():
    return input("\nIntroduce el link del video: ")

def optar(url):
    def listarCalidadesSegúnPágina(url):
        ydl_opts_info = {
            "listformats": True,
            }
        print("\n LISTA DE CALIDADES DISPONIBLES \n")
        with YoutubeDL(ydl_opts_info) as ydl:
                ydl.extract_info(url, download=False)
    
    print("\nOpciones de calidad: \n")
    print("1 - Mejor calidad disponible (video + audio)")
    print("2 - Descargar sólo el sonido de la mejor calidad")
    print("3 - Elegir manualmente de la lista")
    
    opción = input("\nIntroduce el código de formato deseado: ").strip()

    match opción:
        case "1":
            return (
                "bestvideo+bestaudio/best",
                [
                    {"key": "FFmpegVideoRemuxer", "preferedformat": "mp4"},
                ],
            )
        case "2":
            return (
                "bestaudio/best",
                [
                    {"key": "FFmpegExtractAudio", "preferredcodec": "aac", "preferredquality": "192"},
                ],
            )
        case "3":
            listarCalidadesSegúnPágina(url)
            formato = input("\nIntroduce el código de formato deseado: ")
            return formato, []
        case _:
            print("\nOpción inválida, se seleccionará la mejor calidad disponible por defecto.")
            return (
                "bestvideo+bestaudio/best",
                [
                    {"key": "FFmpegVideoConvertor", "preferedformat": "mp4" }
                ],
            )


def descargar():
    cant_video = input("Introduce la cantidad que deseas descargar: ").strip()
    while not cant_video.isdigit() or int(cant_video) <= 0:
        print("La cantidad debe ser un número positivo.")
        cant_video = input("Introduce la cantidad que deseas descargar: ").strip()
    for cant in range(int(cant_video)):
        url = obtenerURL()
        while "http" not in url or url.strip() == "":
            print("\n URL inválida, por favor introduce una URL válida.")
            url = obtenerURL()
        formato , procesoCodificación = optar(url)
        
        ydl_opts = {
            "outtmpl": r"C:\Users\veram\Downloads\%(title)s.%(ext)s",
            "format": formato,
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
        
        ydl_opts.update(obtener_cookies()) #Acá obtengo los cookies de cualquier video, esta función está modularizada.
        
        subtítulos = descargar_subtítulos(url)
        
        ydl_opts.update(subtítulos)
        try:
            print(f"\nDescargando {cant + 1} de {cant_video}...")
            with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url)
                    print("\n Video descargado COMPLETAMENTE, QUE SASTISFACTORIO.\n")
            
            if subtítulos:
                
                título = info.get("title", "video")
                patrón = sanitize_filename(título) + "*.srt"
                ubicación = os.path.join(r"C:\Users\veram\Downloads", patrón)
                
                archivo_srt = glob.glob(ubicación)
                                
                if archivo_srt:
                    limpiar_repeticiones(archivo_srt[0])
                    os.remove(archivo_srt[0])
                    print("Subtitulo limpio descargado exitosamente")
                else:
                    print("No se encontró el subtítulo")
                
        except DownloadError as excepción:
            if "No video formats found" in str(excepción):
                print("\n⚠ No se pudo descargar el video.")
                print("👉 Posibles causas:")
                print("   - Necesitás actualizar yt-dlp (ejecutá: yt-dlp -U o pip install -U yt-dlp).")
                print("   - El video puede requerir iniciar sesión (usa cookiesfrombrowser).")
                print("   - El video puede estar restringido (VIP o bloqueado por región).")
            elif "Unable to download webpage" in str(excepción):
                print("\n ERROR DE CONEXIÓN en el video")
            else:
                print(f"\n Error: {excepción}")
            
descargar()

print(input("\nDescarga completada con audio convertido a AAC compatible."))