from tqdm import tqdm
import time
from yt_dlp import YoutubeDL

def obtenerURL():
    return input("\nIntroduce el link del video: ")

# def listarCalidadesSegúnPágina(url):
#     ydl_opts_info = {
#         "listformats": True,
#         }
#     print("\n LISTA DE CALIDADES DISPONIBLES \n")
#     with YoutubeDL(ydl_opts_info) as ydl:
#             ydl.extract_info(url, download=False)

def optar(url):
    print("\nOpciones de calidad: \n")
    print("1 - Mejor calidad disponible (video + audio)")
    print("2 - Mejor calidad hasta 1080p (evita 4K)")
    print("3 - Elegir manualmente de la lista")
    return input("\nIntroduce el código de formato deseado: ").strip()

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
        # listarCalidadesSegúnPágina(url)
        # formato = input("\nIntroduce el código de formato deseado: ")
        ydl_opts = {
            "outtmpl": r"C:\Users\veram\Downloads\%(title)s.%(ext)s",
            "format": "",
            "merge_output_format": "mp4",
            "noplaylist": True,
            "nooverwrites": True,
            "postprocessors": [{
            "key": "FFmpegVideoRemuxer",
            "preferedformat": "mp4"
            }]
        }
        print("\n⏳ Preparando descarga...")

        for i in tqdm(range(100), desc="Descargando"):
            time.sleep(0.025)
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