from yt_dlp import YoutubeDL
from yt_dlp.utils import sanitize_filename
import os, glob, difflib, re

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

def descargar_subtítulos(url):
    opción = input("¿Querés descargar los subtítulos? ").lower().strip()
    def listar_lenguas(url):
        ydl_opts_info = {"listsubtitles": True}
        with YoutubeDL(ydl_opts_info) as ydl:
            ydl.extract_info(url, download=False)
    if opción in ["si", "s", "sí"]:
        listar_lenguas(url)
        if "bilibili" in url:
            idioma = "zh-Hans"
        else:
            idioma = input("¿En qué idioma está el video? ").lower().strip() or "es"

        return {
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": [idioma],
        "subtitlesformat": "srt",
    }
    else:
        return {}

def limpiar_repeticiones(ruta_srt):
    with open(ruta_srt, "r", encoding="utf-8") as archivo:
        contenido = archivo.readlines()
          
    bloques = re.split(r"\n\s\n", contenido.strip())
    bloques_limpios = []
    texto_anterior = ""
    
    for bloque in bloques:
        lineas = bloque.splitlines()

        # Si el bloque tiene menos de 3 líneas, lo saltamos (no parece válido)
        if len(lineas) < 3:
            bloques_limpios.append(bloque)
            continue

        texto = " ".join(lineas[2:]).strip()

        # Limpieza de repeticiones parciales (más tolerante)
        if texto_anterior:
            # Si más del 70% del texto anterior está incluido en el actual, se considera repetición
            interseccion = len(set(texto_anterior.split()) & set(texto.split()))
            proporcion = interseccion / max(len(texto.split()), 1)

            if proporcion > 0.7:
                # fusionar con el texto anterior
                texto = texto_anterior + " " + " ".join([palabra for palabra in texto.split() if palabra not in texto_anterior.split()])

    
    bloque_nuevo = ""
    bloques_limpios.append(bloque_nuevo)
    texto_anterior = ""
    
    # Guardar el nuevo archivo limpio
    contenido_final = "\n\n".join(bloques_limpios)
    with open(ruta_srt, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_final)
    
def descargar():
    cant_video = input("Introduce la cantidad de videos que deseas descargar: ").strip()
    while not cant_video.isdigit() or int(cant_video) <= 0:
        print("La cantidad debe ser un número positivo.")
        cant_video = input("Introduce la cantidad de videos que deseas descargar: ").strip()
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
        subtítulos = descargar_subtítulos(url)
        if isinstance(subtítulos, dict):
            ydl_opts.update(subtítulos)
        try:
            print(f"\nDescargando video {cant + 1} de {cant_video}...")
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
                    print("Subtitulo limpio descargado exitosamente")
                else:
                    print("No se encontró el subtítulo")
                
        except Exception as excepción:
            if "Unable to download webpage" in str(excepción):
                print("\n ERROR DE CONEXIÓN en el video")
            else:
                print(f"\n Error al descargar el video: {excepción}")

descargar()

print(input("\nDescarga completada con audio convertido a AAC compatible."))