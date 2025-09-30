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
    print("2 - Mejor calidad hasta 1080p (evita 4K)")
    print("3 - Descargar sólo el sonido de la mejor calidad")
    print("4 - Elegir manualmente de la lista")
    
    opción = input("\nIntroduce el código de formato deseado: ").strip()
    
    match opción:
        case "1":
            return "bestvideo+bestaudio/best"
        case "2":
            return "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        case "3":
            return "bestaudio/best"
        case "4":
            listarCalidadesSegúnPágina(url)
            formato = input("\nIntroduce el código de formato deseado: ")
            return formato
        case _:
            print("\nOpción inválida, se seleccionará la mejor calidad disponible por defecto.")
            return "bestvideo+bestaudio/best"

def descargar_videos():
    cant_video = input("Introduce la cantidad de videos que deseas descargar: ").strip()
    while not cant_video.isdigit() or int(cant_video) <= 0:
        print("La cantidad debe ser un número positivo.")
        cant_video = input("Introduce la cantidad de videos que deseas descargar: ").strip()
    for cant in range(int(cant_video)):
        url = obtenerURL()
        while "http" not in url or url.strip() == "":
            print("\n URL inválida, por favor introduce una URL válida.")
            url = obtenerURL()
        formato = optar(url)
        print(f"\nDescargando video {cant + 1} de {cant_video}...")
        ydl_opts = {
            "outtmpl": r"C:\Users\veram\Downloads\%(title)s.%(ext)s",
            "format": f"{formato}",
            "merge_output_format": "mp4",
            "noplaylist": True,
            "nooverwrites": True,
            "postprocessors": [{
            "key": "FFmpegVideoRemuxer",
            "preferedformat": "mp4"
            }]
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    print("\n Video descargado COMPLETAMENTE, QUE SASTISFACTORIO.\n")
        except Exception as excepción:
            if "Unable to download webpage" in str(excepción):
                print("\n ERROR DE CONEXIÓN en el video")
            else:
                print("\n Error al descargar el video: {}".format(excepción))

descargar_videos()

print(input("\nDescarga completada con audio convertido a AAC compatible."))