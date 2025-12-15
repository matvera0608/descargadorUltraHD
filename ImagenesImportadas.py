import os
from PIL import Image, ImageTk
import customtkinter as ctk

directorio = os.path.dirname(__file__)
ícono = os.path.join(directorio, "imágen", "descargador.ico")
ícono_en_png = os.path.join(directorio, "imágen", "descargador.gif")

# --- FUNCIÓN PARA CARGAR IMAGENES ---
def cargar_imagen(ruta_subcarpeta_imagen, nombre_imagen, tamaño=(100, 100)):
    ruta = os.path.join(directorio, ruta_subcarpeta_imagen, nombre_imagen)
    if not os.path.exists(ruta):
        print(f"Imagen no encontrada: {ruta}")
        return None
    try:
        imagen = Image.open(ruta)
        imagen = imagen.resize(tamaño, Image.Resampling.LANCZOS)

        try:
            ctk_image = ctk.CTkImage(light_image=imagen, size=tamaño)
            return ctk_image
        except Exception:
            # Fallback: devolver PhotoImage si CTkImage no funciona
            return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"❌ Error al cargar imagen {nombre_imagen}: {e}")
        return None
