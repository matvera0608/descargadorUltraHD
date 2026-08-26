import urllib.request, glob, os, sys, zipfile, shutil


def descargar_FFMPEG(callback_progreso=None, callback_estado=None):
     if getattr(sys, 'frozen', False):
          base_path = os.path.dirname(sys.executable)
     else:
          base_path = os.path.dirname(os.path.abspath(__file__))

     carpeta_ffmpeg = os.path.join(base_path, "ffmpeg")
     ruta_exe = os.path.join(carpeta_ffmpeg, "ffmpeg.exe")

     if os.path.exists(ruta_exe):
          return ruta_exe

     os.makedirs(carpeta_ffmpeg, exist_ok=True)

     url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
     zip_name = os.path.join(base_path, "ffmpeg.zip")
     temp_dir = os.path.join(base_path, "ffmpeg_temp")

     def reportar_avance(bloques_descargados, tamaño_bloque, total_bytes):
          if total_bytes > 0:
               porcentaje = min(int(bloques_descargados * tamaño_bloque * 100 / total_bytes), 100)
          if callback_progreso:
               callback_progreso(porcentaje)

     try:
          if callback_estado:
               callback_estado("✨ Preparando todo para tus descargas...")
          
          urllib.request.urlretrieve(url, zip_name, reporthook=reportar_avance)

          if callback_estado:
               callback_estado("📦 Configurando componentes necesarios...")

          with zipfile.ZipFile(zip_name, "r") as zip_ref:
               zip_ref.extractall(temp_dir)

          ruta_encontrada = glob.glob(os.path.join(temp_dir, "**", "ffmpeg.exe"), recursive=True)

          if ruta_encontrada:
               shutil.move(ruta_encontrada[0], ruta_exe)
               if callback_estado:
                    callback_estado("🚀 ¡Todo listo para arrancar!")
               exito = True
          else:
               exito = False

     except Exception as e:
          print(f"La descarga se interrumpió o falló: {e}")
          exito = False
     
     finally:
          if os.path.exists(zip_name):
               try:
                    os.remove(zip_name)
               except:
                    pass
               
          if os.path.exists(temp_dir):
               try:
                  shutil.rmtree(temp_dir, ignore_errors=True)  
               except:
                    pass
               
     return ruta_exe if exito else "ffmpeg"