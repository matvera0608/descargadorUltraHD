from yt_dlp import YoutubeDL
import string, re
from Cookies import *
from Elementos import *
from yt_dlp_UPDATES import *


def procesar_subtítulos(ventana, url, destino, progreso):
  try:
    descarga_exitosa = descargar_subtítulos(ventana, url, destino)
    if descarga_exitosa:
        mostrar_aviso(ventana, "SUBTÍTULO DESCARGADO CORRECTAMENTE", colors["successfully"])
    elif descarga_exitosa is None:
        pass
    else:
        mostrar_aviso(ventana, "ERROR AL DESCARGAR SUBTÍTULO", colors["danger"])
  except Exception as e:
    cerrar_seguro(progreso)
    print(f"Error al descargar subtítulos: {e}")
    return False


#¿Igual este sirve para determinar los subtítulos disponibles?
def obtener_subtítulos_disponibles(url): #Obtiene los idiomas de subtítulos disponibles para un video dado su URL pero no los descarga.
    subt_ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "logger": None,
        "skip_download": True,
    }
    try:
        with YoutubeDL(subt_ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            subs = info.get("subtitles") or info.get("automatic_captions") or info.get("requested_subtitles") or {}
            return list(subs.keys()) if subs else []
    except Exception as e:
        print(f"Error al obtener subtítulos: {e}")
        return []
    
def descargar_subtítulos(ventana, url, destino):
    try:
        base_opts = {
                "logger": None,
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitlesformat": "srt",
                "writeautomaticsub": True,
                "outtmpl": os.path.join(destino, "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",
                }
    
        es_de_bilibili = "bilibili" in url.lower()
        if es_de_bilibili: #Este es para bilibili, porque la plataforma requiere cookies para descargar subtítulos.
            ruta_cookie = procesar_cookies()
            if ruta_cookie:  # ejecuta la función y asegura que la cookie esté lista
                base_opts.update({
                    "cookiefile": carpeta_destino_cookies,
                    "logger": None,
                    "quiet": True,
                    "no_warnings": True,
                    "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Referer": "https://www.bilibili.com/",
                    }
                })
            else:
                print("⚠ No se pudo preparar cookies para BiliBili, porque tuvo un problema.")

            with YoutubeDL({**base_opts, "skip_download": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
            subs = info.get("subtitles") or info.get("automatic_captions") or info.get("requested_subtitles") or {}
            idiomas = [i for i in subs.keys() if i != "danmaku"]
            if not idiomas and "subtitles" in info:
                mostrar_aviso(ventana, "Es necesario procesar tus cookies.", colors["alert"])
                return None
            elif not idiomas:
                mostrar_aviso(ventana, "No hay subtítulos disponibles", colors["danger"])
                return None
            
            idioma_original = idiomas[0]
        else:
            idiomas = obtener_subtítulos_disponibles(url)
            if not idiomas:
                mostrar_aviso(ventana, "No hay subtítulos disponibles", colors["danger"])
                return None
            idioma_original = next((i for i in idiomas if i.endswith("-orig")), idiomas[0])   
        base_opts.update({"subtitleslangs": [idioma_original]})
        with YoutubeDL(base_opts) as ydl:
            ydl.download([url])
            
        info = ydl.extract_info(url, download=False) 
        archivo_sub = os.path.join(destino, f"{info['title']}.{idioma_original}.srt")
        
        if os.path.exists(archivo_sub):
            mostrar_aviso(ventana, f"Subtítulo guardado", colors["successfully"])
        else:
            mostrar_aviso(ventana, "No se generó archivo de subtítulos", colors["danger"])
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    

def limpiar_repeticiones(ruta_srt):
    def normalizar_texto(texto):
        return texto.lower().translate(str.maketrans("", "", string.punctuation))
    
    with open(ruta_srt, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
    
       
    bloques = re.split(r"\n\s*\n", contenido.strip())
    bloques_limpios = []
    tiempo_anterior = ""
    texto_anterior = ""
    repeticiónEliminada = 0
    for bloque in bloques:
        lineas = bloque.splitlines()
        if len(lineas) < 3:
            bloques_limpios.append(bloque)
            continue
        
        tiempo = lineas[1].strip()
        texto = " ".join(lineas[2:]).strip()
        textoNormalizado = normalizar_texto(texto)

        repetición = False
        if texto_anterior:
            # Si más del 70% del texto anterior está incluido en el actual, se considera repetición
            interseccion = len(set(texto_anterior.split()) & set(textoNormalizado.split()))
            proporcion = interseccion / max(len(texto.split()), 1)
            
            #Se creó una variable para tener más control de los segmentos de la oración, esto es para que
            #a la hora de limpiar subtítulos se pueda garantizar que dice con el fin de traducir a otro idioma
            fin_anterior = tiempo_anterior.split(" --> ")[1].strip()
            inicio_actual = tiempo.split(" --> ")[0].strip()

            if proporcion > 0.8 and fin_anterior == inicio_actual:
                repetición = True
        
        if repetición:
            repeticiónEliminada += 1
            print(f"Total de repeticiones eliminadas: {lineas[0]}")
        else:
            bloques_limpios.append(bloque)
            texto_anterior = textoNormalizado
            tiempo_anterior = tiempo
    
    print(f"✔ Limpieza completada. Repeticiones eliminadas: {repeticiónEliminada}")
    
    contenido_final = "\n\n".join(bloques_limpios)
    ruta_limpia = ruta_srt.replace(".srt", "_limpio.srt")
    with open(ruta_limpia, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_final)