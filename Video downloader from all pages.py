from yt_dlp import YoutubeDL

# def navegador_abierto(nombre="chrome"):
#     for proceso in psutil.process_iter(["name"]):
#         if nombre.lower() in proceso.info["name"].lower():
#             return True
#     return False


# ydl_opts_info = {
#     "listformats": True,
# }

# try:
#     print("\n LISTA DE CALIDADES DISPONIBLES \n")
#     with YoutubeDL(ydl_opts_info) as ydl:
#         ydl.extract_info(, download=False)
# except Exception as excepción:
#         if "Unable to download webpage" in str(excepción):
#             print("\n ERROR DE CONEXIÓN")
#         else:
#             print("\n Error al descargar: {}".format(excepción))


def cargar_configuración():
    ydl_opts = {
        "outtmpl": r"C:\Users\veram\Downloads\%(title)s.%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "cookiesfrombrowser": ("chrome",),
        "noplaylist": True,
        "nooverwrites": True,
        "postprocessors": [{
        "key": "FFmpegVideoRemuxer",
        "preferedformat": "mp4"
        }]
    }
    return ydl_opts

def iniciar_descarga():
    opción = cargar_configuración()
    cant_video = int(input("¿Cuántos videos querés descargar? "))
    
    for i in range(cant_video):
    
        url = input("introduce el link del video: ")    
        descargar(url, opción)


def descargar(url, opción):
    try:
        with YoutubeDL(opción) as ydl:
            ydl.download([url])
    except Exception as excepción:
        if "Unable to download webpage" in str(excepción):
            print("\n ERROR DE CONEXIÓN")
        else:
            print("\n Error al descargar: {}".format(excepción))      
            
iniciar_descarga()          
