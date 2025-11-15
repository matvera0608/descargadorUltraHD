from yt_dlp import YoutubeDL
import string, re
from Cookies import *
from Elementos import *
from yt_dlp_UPDATES import *
# yt-dlp --cookies C:\Users\veram\AppData\Roaming\yt-dlp\cookies.txt --list-subs https://www.bilibili.com/video/BV185HtzAEGX"

def obtener_subtítulos_disponibles(url):
    subt_ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "logger": None,
        "skip_download": True,
    }
    with YoutubeDL(subt_ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        subs = info.get("subtitles") or info.get("automatic_captions") or {}
        if not subs:
            print("No hay subtítulos disponibles para el video")
            return
        
        return list(subs.keys())
    
def descargar_subtítulos(ventana, url, destino):
    try:
        idiomas = obtener_subtítulos_disponibles(url) or []
        if not idiomas:
            print("⚠ No hay subtítulos disponibles.")
            return None

        idioma_original_con_terminación_orig = [idioma for idioma in idiomas if idioma.endswith("-orig")]
        
        idioma_seleccionado = idioma_original_con_terminación_orig[0] if idioma_original_con_terminación_orig else idiomas[0]
        
        base_opts = {
                "logger": None,
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitlesformat": "srt",
                "writeautomaticsub": True,
                "outtmpl": os.path.join(destino, "%(title)s.%(ext)s"),
                "extractor_args": {"youtube": {"player_client": ["web"]}},
                "merge_output_format": "mp4",
                }
    
        es_de_bilibili = "bilibili" in url.lower()

        if es_de_bilibili: #Este es para bilibili, porque la plataforma requiere cookies para descargar subtítulos.
            if not contiene_sessdata(destino_cookies):
                print("⛔ No se detectó sesión activa. Exportá cookies nuevamente desde Chrome.")
                return []
            base_opts.update({
                "cookiefile": destino_cookies,
                "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": "https://www.bilibili.com/",
                }
            })
        
        base_opts.update({"subtitleslangs": [idioma_seleccionado]})
        
        with YoutubeDL(base_opts) as ydl:
            ydl.download([url])
 
    except Exception as e:
        print(f"Error: {e}")
        return None
    

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
    