from yt_dlp import YoutubeDL
import os, string, re
from Cookies import contiene_sessdata

os.system("yt-dlp -U")
# yt-dlp --cookies C:\Users\veram\AppData\Roaming\yt-dlp\cookies.txt --list-subs https://www.bilibili.com/video/BV185HtzAEGX"


def listar_lenguas(url):
    global info
    ydl_opts_info = {"listsubtitles": True}
    with YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
                
#Descargar subtítulos se modificó:
#1. La condición if bilibili tiene cookiefile para leer cookies del video y subtitular.
#2. Contiene sessdata lo que hace es vertificar si cookies tiene sessdata.
def descargar_subtítulos(url):
    opción = input("¿Querés descargar los subtítulos? ").lower().strip()
    if opción in ["si", "s", "sí"]:
        listar_lenguas(url) if url not in "bilibili" else True
        if "bilibili" in url.lower():
            if not contiene_sessdata(r"C:\Users\veram\AppData\Roaming\yt-dlp\cookies.txt"):
                print("⛔ No se detectó sesión activa. Exportá cookies nuevamente desde Chrome.")
                return []
            idioma = input("¿En qué idioma está el video? ").lower().strip() or "ai-zh"
            base_opts = {
                        "cookiefile": r"C:\Users\veram\AppData\Roaming\yt-dlp\cookies.txt",
                        "extractor_args": {"bilibili": {"lang": ["ai-zh", "zh-Hans"], "allow_ep": ["True"]}},
                        "writesubtitles": True,
                        #"format": "bv*+ba/b",
                        "subtitleslangs": [idioma],
                        "writeautomaticsub": True,
                        "subtitlesformat": "srt",
                        "outtmpl": r"C:\Users\veram\Downloads\%(title)s.%(ext)s",
                        "merge_output_format": "mp4",
                        "http_headers": {
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                                        "Referer": "https://www.bilibili.com/",
                                        },
                        }
            return base_opts
        else:
            idioma = input("¿En qué idioma está el video? ").lower().strip() or "es"
            return {
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": [idioma],
            "subtitlesformat": "srt",
            }
    else:
        return {}

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
    # Guardar el nuevo archivo limpio
    contenido_final = "\n\n".join(bloques_limpios)
    ruta_limpia = ruta_srt.replace(".srt", "_limpio.srt")
    with open(ruta_limpia, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_final)
    