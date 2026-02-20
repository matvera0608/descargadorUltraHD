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
def obtener_subtítulos_disponibles(url, archivos_de_cookie=None): #Obtiene los idiomas de subtítulos disponibles para un video dado su URL pero no los descarga.
    subt_ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }
    
    if archivos_de_cookie:
        subt_ydl_opts.update({
            "cookiefile": archivos_de_cookie
        })
    try:
        with YoutubeDL(subt_ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        subs = {}
        
        for key in ["subtitles", "automatic_captions", "requested_subtitles"]:
            if info.get(key):
                subs.update(info[key])
                
        idiomas = [i for i in subs.keys() if i != "danmaku"] #Idiomas guarda una lista de idiomas disponibles, pero se excluye "danmaku" que es un aluvión de mensajes de BiliBili y en Nico Nico Ni.
        return idiomas, info
    except Exception as e:
        print(f"Error al obtener subtítulos: {e}")
        return [], []
    
def descargar_subtítulos(ventana, url, destino, archivos_de_cookie=None):
    try:
        
        idiomas, info = obtener_subtítulos_disponibles(url, archivos_de_cookie)
        
        if not idiomas:
            mostrar_aviso(ventana, "No hay subtítulos", colors["danger"])
            return False, None
        
        idioma = next((i for i in idiomas if i.endswith("-orig")), idiomas[0]) #Cuál es la diferencia entre este y el otro?
        
        idioma = [i for i in idiomas if i.endswith("-original") or i.endswith("-auto")][0] if any(i.endswith("-original") or i.endswith("-auto") for i in idiomas) else idiomas[0] #Si hay subtítulos originales o automáticos, se selecciona el primero de esos, de lo contrario se selecciona el primer idioma disponible. Pero lo más probable es que en YouTube aparezca como -orig.
        
        
        
        
        base_opts = {
                "logger": None,
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "writesubtitles": True,
                "subtitlesformat": "srt",
                "writeautomaticsub": True,
                "outtmpl": os.path.join(destino, "%(title)s.%(ext)s")
                }
        
        if archivos_de_cookie:
            base_opts.update({
            "cookiefile": archivos_de_cookie
            })
        
        with YoutubeDL(base_opts) as ydl:
            info = ydl.download([base_opts])
            
            # Obtener nombre real generado
            archivo_base = ydl.prepare_filename(info)
            archivo_sub = archivo_base.rsplit(".", 1)[0] + f".{idioma}.srt"
            
        if os.path.exists(archivo_sub):
            mostrar_aviso(ventana, f"Subtítulo guardado", colors["successfully"])
            return True, None #Los Trues o Falses especifican verdadero o falso para los colores
        else:
            mostrar_aviso(ventana, "No se generó archivo de subtítulos", colors["danger"])
            return False, None
        
    except Exception as e:
        print(f"Error: {e}")
        return False, None
    

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