import urllib.request, glob, os, zipfile, shutil


def descargar_FFMPEG(destino="ffmpeg.exe"):
     if os.path.exists(destino):
          print("✅ FFmpeg ya se encuentra disponible.")
          return True

     url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
     zip_name = "ffmpeg.zip"
     temp_dir = "ffmpeg_temp"

     try:
          print("⏳ Descargando FFmpeg automáticamente (esto puede tardar unos segundos)...")
          urllib.request.urlretrieve(url, zip_name)

          print("📦 Descomprimiendo archivos...")
          with zipfile.ZipFile(zip_name, "r") as zip_ref:
               zip_ref.extractall(temp_dir)

          # Buscamos de forma inteligente el ffmpeg.exe dentro de la carpeta extraída
          # sin importar el nombre exacto de la versión que descargó la web.
          ruta_encontrada = glob.glob(os.path.join(temp_dir, "**", "ffmpeg.exe"), recursive=True) ##¿Qué almacena ruta_encontrada y que tipo de dato es?

          if ruta_encontrada:
               os.rename(ruta_encontrada[0], destino) 
               print("🚀 ¡FFmpeg se configuró y quedó listo con éxito!")
               exito = True
          else:
               print("⚠ No se pudo encontrar el binario de FFmpeg dentro del archivo descargado.")
               exito = False

     except Exception as e:
          print(f"❌ Ocurrió un error al descargar FFmpeg: {e}")
          exito = False

     # Limpieza de archivos temporales sobrantes
     if os.path.exists(zip_name):
          os.remove(zip_name)

     if os.path.exists(temp_dir):
          # Borra la carpeta temporal y su contenido de forma limpia
          shutil.rmtree(temp_dir, ignore_errors=True)
     return exito