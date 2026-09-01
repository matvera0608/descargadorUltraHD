import urllib.request, glob, os, sys, zipfile, shutil, stat
from web.Internet import verificar_conexión_a_internet
from Elementos import colors

def limpiar_basura():
     
     """Limpia archivos temporales o residuales de descargas anteriores."""
     base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
     carpeta_ffmpeg = os.path.join(base_path, "ffmpeg")
     # Lista de posibles residuos
     residuos = [
          os.path.join(carpeta_ffmpeg, "ffmpeg.zip"),
          os.path.join(carpeta_ffmpeg, "ffmpeg_temp")
     ]

     def administrar_permisos(func, ruta, _exc):
          """Reintenta la eliminación después de conceder permisos de escritura."""
          try:
               os.chmod(ruta, stat.S_IWRITE)
               func(ruta)
          except Exception as error:
               print(f"⚠️ No se pudo solucionar el problema de '{ruta}'")
               print(f"Motivo: {error}")
     
     
     for r in residuos:
          if not os.path.exists(r):
               continue

          try:
               if os.path.isfile(r):
                    os.remove(r)
               else:
                    shutil.rmtree(r, onexc=administrar_permisos)
               print(f"🧹 Eliminado: {r}")

          except Exception as e:
               print(f"⚠️ No se pudo eliminar '{r}'. Motivo: {e}")
         

def descargar_FFMPEG(progreso, estado):
     
     limpiar_basura()
     
     base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

     carpeta_ffmpeg = os.path.join(base_path, "ffmpeg")
     ruta_exe = os.path.join(carpeta_ffmpeg, "ffmpeg.exe")

     if os.path.exists(ruta_exe):
         print(f"✅ FFmpeg listo en {ruta_exe}")
         return ruta_exe


     os.makedirs(carpeta_ffmpeg, exist_ok=True)

     url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
     zip_name = os.path.join(carpeta_ffmpeg, "ffmpeg.zip")
     temp_dir = os.path.join(carpeta_ffmpeg, "ffmpeg_temp")

     def reportar_avance(bloques_descargados, tamaño_bloque, total_bytes):
          
          if total_bytes <= 0:
               return

          porcentaje = min(int(bloques_descargados * tamaño_bloque * 100 / total_bytes),100)

          if progreso:
               progreso(porcentaje)

     try:
          if estado:
               estado("✨ Preparando todo para tus descargas...")
          
          urllib.request.urlretrieve(url, zip_name, reporthook=reportar_avance)

          if estado:
               estado("📦 Configurando componentes necesarios...")

          with zipfile.ZipFile(zip_name, "r") as zip_ref:
               zip_ref.extractall(temp_dir)

          ruta_encontrada = glob.glob(os.path.join(temp_dir, "**", "ffmpeg.exe"), recursive=True)

          if ruta_encontrada:
                      
               print("✅ Se encontró ffmpeg.exe:")
               print(ruta_encontrada[0])
               shutil.move(ruta_encontrada[0], ruta_exe)
               
               print("✅ FFmpeg movido correctamente.")
               limpiar_basura()
               print("🧹 Limpieza terminada.")

               if estado:
                    print("📢 Enviando mensaje de éxito...")
                    estado("🚀 ¡Todo listo para arrancar!", colors["successfully"])

                    print("Mensaje de éxito enviado")
                    
               exito = True
          else:
               exito = False

     except Exception as e:
          
          print(f"❌ Error descargando FFmpeg: {e}")

          #Se ha colocado una función que verifique la conexión a internet y muestre en la interfaz para una mayor UX.
          if not verificar_conexión_a_internet():
               if estado:
                    estado("No hay conexión a Internet", colors["error"])
               
          else:
               if estado:
                    estado("Error en la descarga", colors["error"])
          
          exito = False
     
     return ruta_exe if exito else None