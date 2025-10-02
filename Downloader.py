from yt_dlp import YoutubeDL

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
                    ydl.download([url])
                    print("\n Video descargado COMPLETAMENTE, QUE SASTISFACTORIO.\n")

        except Exception as excepción:
            if "Unable to download webpage" in str(excepción):
                print("\n ERROR DE CONEXIÓN en el video")
            else:
                print("\n Error al descargar el video: {}".format(excepción))

descargar()

print(input("\nDescarga completada con audio convertido a AAC compatible."))