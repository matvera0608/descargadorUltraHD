import os
from PIL import Image, ImageTk
import customtkinter as ctk

directorio = os.path.dirname(__file__)
ícono = os.path.join(directorio, "imágen", "descargador.ico")


# --- FUNCIÓN PARA CARGAR IMAGENES ---
def cargar_imagen(ruta_subcarpeta_imagen, nombre_imagen, tamaño=(25, 25)):
    """Carga una imagen y devuelve preferiblemente un `CTkImage` (recomendado para customtkinter).

    - Devuelve `customtkinter.CTkImage(light_image=..., size=...)` cuando sea posible.
    - Si no se puede crear `CTkImage` (por ejemplo, versión antigua), hace fallback a `ImageTk.PhotoImage`.
    """
    ruta = os.path.join(directorio, ruta_subcarpeta_imagen, nombre_imagen)
    if not os.path.exists(ruta):
        print(f"Imagen no encontrada: {ruta}")
        return None
    try:
        imagen = Image.open(ruta)
        imagen = imagen.resize(tamaño, Image.Resampling.LANCZOS)

        # Intentar devolver CTkImage (para evitar la advertencia de CTkButton)
        try:
            ctk_image = ctk.CTkImage(light_image=imagen, size=tamaño)
            return ctk_image
        except Exception:
            # Fallback: devolver PhotoImage si CTkImage no funciona
            return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"❌ Error al cargar imagen {nombre_imagen}: {e}")
        return None
