import subprocess as subproceso, os


def decodificar_video(ruta_entrada, ruta_salida=None):
    if ruta_salida is None:
        base, ext = os.path.splitext(ruta_entrada)
        ruta_salida = base + "_temp" + ext  # archivo temporal

    comando = [
        "ffmpeg",
        "-y",
        "-i", ruta_entrada,
        "-c:v", "libx264",
        "-profile:v", "high",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        "-map_metadata", "-1",   # 🔥 elimina metadatos
        ruta_salida
    ]

    subproceso.run(comando, check=True)

    # 🔄 reemplazar original por el convertido
    os.replace(ruta_salida, ruta_entrada)

    return ruta_entrada

#Esto verifica 2 veces antes de hacer la recodificación para poder ver videos.
def necesitar_decodificación(info):
    vcodec = info.get("vcodec", "")
    acodec = info.get("acodec", "")
    ext = info.get("ext", "")

    if ext != "mp4":
        return True
    if not vcodec.startswith("avc1"):
        return True
    if acodec not in ("mp4a", "aac"):
        return True

    return False
