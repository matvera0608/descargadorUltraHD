from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from yt_dlp.utils import sanitize_filename
import os, glob
from Subtitulation import descargar_subtítulos, limpiar_repeticiones
from Cookies import mover_cookies
# from Cookies import obtener_cookies

# Esta función lo que hace es intentar descargar la información de un video, en caso de la falla imprime con un mensaje
# y vuelve a intentar con un proxy chino (esto es útil para BiliBili que a veces falla)
def extraer_info_seguro(url, opciones):
    try:
        with YoutubeDL(opciones) as ydl:
            return ydl.extract_info(url)
    except DownloadError as e:
        if "BiliBili" in str(e) and "No video formats found" in str(e):
            print("⚠ Error con el extractor BiliBili. Reintentando con proxy CN...")
            opciones["proxy"] = "https://cn.bilibili.com"  # redirige a servidor chino
            opciones["skip_download"] = True
            opciones["forcejson"] = True
            try:
                with YoutubeDL(opciones) as ydl:
                    return ydl.extract_info(url)
            except Exception as e2:
                print("❌ Fallback también falló:", e2)
                return None
        else:
            raise e

def obtenerURL():
    return input("\nIntroduce el link del video: ")

def listarCalidadesSegúnPágina(url):
    ydl_opts_info = {
        "listformats": True,
        }
    print("\n LISTA DE CALIDADES DISPONIBLES \n")
    with YoutubeDL(ydl_opts_info) as ydl:
            ydl.extract_info(url, download=False)

def optar(url):
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
        if "bilibili" in url:
            if not os.path.exists(r"C:\Users\veram\AppData\Roaming\yt-dlp\cookies.txt"):
                mover_cookies()
            else:
                print("✅ cookies.txt ya está en la ubicación correcta. Continuando...")
                
                
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
        
        subtítulos = descargar_subtítulos(url)
        
        ydl_opts.update(subtítulos)
        print(f"\nDescargando {cant + 1} de {cant_video}...")
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url)
                if "bilibili" in url:
                    extraer_info_seguro(url, ydl_opts)
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
  
            print("\n Video descargado COMPLETAMENTE, QUE SASTISFACTORIO.\n")   
                
        except DownloadError as excepción:
            if "No video formats found" in str(excepción):
                print("⚠ yt-dlp no pudo extraer el video. Puede estar restringido o requerir autenticación avanzada.")
            elif "Unable to download webpage" in str(excepción):
                print("\n ERROR DE CONEXIÓN en el video")
            else:
                print(f"\n Error: {excepción}")
            
descargar()

print(input("\nDescarga completada con audio convertido a AAC compatible."))