import subprocess as subproceso, os


def decodificar_video(ruta_entrada, ruta_salida=None, ffmpeg_exe="ffmpeg"):
    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(f"No existe el archivo de entrada: {ruta_entrada}")

    if ruta_salida is None:
        base, ext = os.path.splitext(ruta_entrada)
        ruta_salida = f"{base}_temp{ext}"
    
    comando = [
      ffmpeg_exe,
      "-y",
      "-i",
      ruta_entrada,
      "-map",
      "0:v:0",
      "-map",
      "0:a:0?",
      "-c:v",
      "libx264",
      "-profile:v",
      "high",
      "-pix_fmt",
      "yuv420p",
      "-c:a",
      "aac",
      "-b:a",
      "192k",
      "-movflags",
      "+faststart",
      "-map_metadata",
      "-1",
      ruta_salida,
  ]

    subproceso.run(
        comando,
        stdout=subproceso.DEVNULL,
        stderr=subproceso.DEVNULL
    )


    resultado = subproceso.run(
      comando, stdout=subproceso.PIPE, stderr=subproceso.PIPE, text=True
  )

    if resultado.returncode != 0 or not os.path.exists(ruta_salida):
        raise RuntimeError(f"FFmpeg falló (código {resultado.returncode}): {resultado.stderr}")

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