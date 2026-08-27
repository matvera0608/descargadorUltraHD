from ImagenesImportadas import *
from FFMPEG import descargar_FFMPEG
import customtkinter as ctk
import re, os
import tkinter as tk

CALIDAD_DE_VIDEO = {
    "youtube": {
        2160: {"excelente": 15000.0, "buena": 8000.0, "regular": 4000.0, "mala": 2000.0},
        1440: {"excelente": 8000.0, "buena": 5000.0, "regular": 3000.0, "mala": 1500.0},
        1080: {"excelente": 4500.0, "buena": 2500.0, "regular": 1500.0, "mala": 800.0},
        720:  {"excelente": 2500.0, "buena": 1500.0, "regular": 900.0, "mala": 500.0},
        480:  {"excelente": 1200.6, "buena": 8500.0, "regular": 5300.0, "mala": 3300.0},
    },

    "bilibili": {
        1080: {"excelente": 1500.0, "buena": 1000.0, "regular": 700.0, "mala": 400.0},
        720:  {"excelente": 900.0,  "buena": 600.0,  "regular": 400.0, "mala": 250.0},
        540:  {"excelente": 700.0,  "buena": 450.0,  "regular": 300.0, "mala": 180.0},
        480:  {"excelente": 600.0,  "buena": 400.0,  "regular": 250.0, "mala": 150.0},
    },

    "tiktok": {
        1080: {"excelente": 600, "buena": 350, "regular": 200, "mala": 150},
        720:  {"excelente": 400, "buena": 250, "regular": 180, "mala": 120},
        540:  {"excelente": 300, "buena": 200, "regular": 150, "mala": 100},
    },

    "douyin": {  # TikTok chino, similar pero un poco más agresivo
        1080: {"excelente": 1800.0, "buena": 1100.0, "regular": 700.0, "mala": 350.0},
        720:  {"excelente": 1000.0, "buena": 700.0,  "regular": 450.0, "mala": 250.0},
        540:  {"excelente": 800.0,  "buena": 500.0,  "regular": 300.0, "mala": 180.0},
        480:  {"excelente": 600.0,  "buena": 400.0,  "regular": 250.0, "mala": 150.0},
    },

    "instagram": {
        1080: {"excelente": 2500.0, "buena": 1500.0, "regular": 900.0, "mala": 500.0},
        720:  {"excelente": 1500.0, "buena": 900.0,  "regular": 600.0, "mala": 300.0},
        540:  {"excelente": 900.0,  "buena": 600.0,  "regular": 350.0, "mala": 200.0},
        480:  {"excelente": 700.0,  "buena": 450.0,  "regular": 300.0, "mala": 150.0},
    },

    "twitter": {
        1080: {"excelente": 2000.0, "buena": 1200.0, "regular": 800.0, "mala": 400.0},
        720:  {"excelente": 1200.0, "buena": 800.0,  "regular": 500.0, "mala": 250.0},
        480:  {"excelente": 700.0,  "buena": 450.0,  "regular": 300.0, "mala": 150.0},
    },

    "facebook": {
        1080: {"excelente": 2500.0, "buena": 1500.0, "regular": 900.0, "mala": 500.0},
        720:  {"excelente": 1500.0, "buena": 900.0,  "regular": 600.0, "mala": 300.0},
        480:  {"excelente": 700.0,  "buena": 450.0,  "regular": 300.0, "mala": 150.0},
    },

    "vimeo": {
        2160: {"excelente": 12000.0, "buena": 8000.0, "regular": 5000.0, "mala": 2500.0},
        1440: {"excelente": 7000.0,  "buena": 4500.0, "regular": 3000.0, "mala": 1500.0},
        1080: {"excelente": 4000.0,  "buena": 2500.0, "regular": 1500.0, "mala": 800.0},
        720:  {"excelente": 2000.0,  "buena": 1200.0, "regular": 800.0,  "mala": 400.0},
    },

    "twitch": {
        1080: {"excelente": 6000.0, "buena": 4500.0, "regular": 3000.0, "mala": 1500.0},
        720:  {"excelente": 4500.0, "buena": 3000.0, "regular": 2000.0, "mala": 1000.0},
        480:  {"excelente": 1500.0, "buena": 900.0,  "regular": 500.0,  "mala": 300.0},
    },
    
    "default": {
        2160: {"excelente": 12000, "buena": 8000, "regular": 5000, "mala": 2500},
        1080: {"excelente": 3000, "buena": 2000, "regular": 1200, "mala": 600},
        720:  {"excelente": 1500, "buena": 900,  "regular": 600,  "mala": 300},
        480:  {"excelente": 800,  "buena": 500,  "regular": 300,  "mala": 150},
    }
}

PESO_CODEC = {
    "av01": 1.45,   # AV1 → muy eficiente
    "vp9":  1.30,   # VP9 → muy bueno
    "hev1": 1.25,   # HEVC / H.265
    "hvc1": 1.25,
    "avc1": 1.00,   # H.264 base
}

TOLERANCIA_PLATAFORMA = {
    "tiktok":     0.12,  # compresión muy agresiva
    "douyin":     0.12,  # es el TikTok chino, misma compresión
    "instagram":  0.10,  # reels muy comprimidos
    "facebook":   0.10,  # similar a instagram, pero un poco más variable
    "twitter":    0.09,  # X comprime fuerte pero no tanto como IG
    "x":          0.09,  # alias
    "bilibili":   0.06,  # buena calidad, pero no tan alta como YouTube
    "youtube":    0.05,  # la más estable y generosa en bitrate
    "default":    0.08   # punto medio para cualquier otra
}

# Paleta personalizada (usa tus hex o nombres preferidos)
colors = {
    "background": "#242424",
    "primary": "#2563eb",
    "primary_hover": "#1d4ed8",
    "accent": "#06b6d4",
    "danger": "#ef4444",
    "text": "#ffffff",
    "successfully": "#12c23b",
    "alert": "#f5bb0b"
}


ventanaProgreso = None


urlHTTP = re.compile(r'^https?://([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?$')

def cerrar_seguro(ventana):
  hook_progreso.activo = False
  ventana.destroy()


def mostrar_seguro(ventana):
  try:
    if ventana and ventana.winfo_exists():
      ventana.deiconify()
  except tk.TclError:
    pass


def limpiar_ansi(texto):
  """Elimina los códigos ANSI (colores de consola) del texto."""
  if not texto:
    return texto
  return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', texto)


def mostrar_descarga_FFMPEG(ventana):
  
  barra = ctk.CTkProgressBar(ventana, width=250)
  barra.pack(pady=10)
  barra.set(0)

  fuente_letra = ("Arial", 15)

  lbl_porcentaje = ctk.CTkLabel(ventana, text="0%", font=fuente_letra)
  lbl_porcentaje.pack(pady=5)
  
  lbl_estado = ctk.CTkLabel(ventana, text="Preparando FFmpeg...", font=fuente_letra)
  lbl_estado.pack(pady=2)
  
  def actualizar_progreso(valor):
    if ventana is None:
      return
    
    def actualizar():
      barra.set(valor/100)
      lbl_porcentaje.configure(text=f"{valor}%")
    
    ventana.after(0, actualizar)
         
  def actualizar_estado(texto):
    if ventana is None:
      return
    ventana.after(0, lambda: lbl_estado.configure(text=texto))
    
    
    
  return actualizar_progreso, actualizar_estado




def mostrar_descarga(ventana):

  icono_img = tk.PhotoImage(file=ícono_en_png)

  fuente_letra = ("Arial", 15)

  # --- Ventana de progreso ---
  ventanaProgreso = ctk.CTkToplevel()
  ventanaProgreso.title("En proceso")
  ventanaProgreso.geometry("600x100")
  ventanaProgreso.resizable(False, False)
  ventanaProgreso.configure(fg_color=colors["background"])
    # Cargar el ícono como PhotoImage


  # Asignar el ícono a la ventana
  ventanaProgreso.iconphoto(False, icono_img)

  # Guardar referencia para que no se borre
  ventanaProgreso.icono_img = icono_img #type: ignore

  ventanaProgreso.attributes("-topmost", True)
  ventanaProgreso.after(100, lambda: ventanaProgreso.attributes("-topmost", False))
  lbl_estado = ctk.CTkLabel(ventanaProgreso, text="Descargando video...", font=fuente_letra)
  lbl_estado.pack(pady=10)

  barra = ctk.CTkProgressBar(ventanaProgreso, width=250)
  barra.pack(pady=10)
  barra.set(0)

  lbl_porcentaje = ctk.CTkLabel(ventanaProgreso, text="0%", font=fuente_letra)
  lbl_porcentaje.pack(pady=5)

  #Acá le cambié para que la interfaz sea más flexible y menos frustrante para el usuario
  ventanaProgreso.transient(ventana)
  ventanaProgreso.lift()
  ventanaProgreso.focus_force()

  # --- Inyección de widgets al hook ---
  hook_progreso.activo = True
  hook_progreso.ventanaProgreso = ventanaProgreso
  hook_progreso.lbl_estado = lbl_estado
  hook_progreso.barra = barra
  hook_progreso.lbl_porcentaje = lbl_porcentaje

  # --- Manejo seguro de cierre ---
  def on_close():
      hook_progreso.activo = False
      ventanaProgreso.destroy()

  ventanaProgreso.protocol("WM_DELETE_WINDOW", on_close)
  
  return ventanaProgreso


# --- Hook de progreso (definido dentro) --- El hook es una función que se llama periódicamente
# durante la descarga para actualizar la interfaz de usuario
def hook_progreso(d):
  if not getattr(hook_progreso, "activo", True):
    return
  try:
    velocidad = limpiar_ansi(d.get('_speed_str', 'N/A'))
    eta = limpiar_ansi(d.get('_eta_str', 'N/A'))
    total = d.get('total_bytes') or d.get('total_bytes_estimate')
    porcentaje = (d['downloaded_bytes'] / total) * 100 if total else 0
    
    if d['status'] == 'downloading':
      if hasattr(hook_progreso, "lbl_estado") and hook_progreso.lbl_estado.winfo_exists():
        hook_progreso.lbl_estado.configure(text=f"Velocidad: {velocidad} | ETA: {eta}")
      if hasattr(hook_progreso, "barra"):
        hook_progreso.barra.set(porcentaje / 100)
      if hasattr(hook_progreso, "lbl_porcentaje"):
        hook_progreso.lbl_porcentaje.configure(text=f"{porcentaje:.1f}%")

    elif d['status'] == 'finished':
      if hasattr(hook_progreso, "barra") and hook_progreso.barra.winfo_exists(): #Controla la barra de progreso
        hook_progreso.barra.set(1)
      if hasattr(hook_progreso, "lbl_porcentaje") and hook_progreso.barra.winfo_exists(): #Calcula el porcentaje actual
        hook_progreso.lbl_porcentaje.configure(text=f"100%")
      if hasattr(hook_progreso, "lbl_estado") and hook_progreso.barra.winfo_exists():
        hook_progreso.lbl_estado.configure(text="✅ Descarga completada.")
      if getattr(hook_progreso, "ventanaProgreso", None):
        hook_progreso.ventanaProgreso.after(5000, lambda: cerrar_seguro(hook_progreso.ventanaProgreso))
        
    else:
      if hasattr(hook_progreso, "lbl_estado"):
        hook_progreso.lbl_estado.configure(text=f"Falló la descarga")
                      
  except Exception as e:
    print(f"Error en el hook de progreso: {e}")
    # try:
    #   os.remove(temp_file)
    # except Exception as e:
    #   print(f"No se pudo eliminar el archivo temporal: {e}")


def mostrar_aviso(contenedor, texto, color=None, milisegundos=5000):
  # Asegúrate de que las indentaciones coincidan EXACTAMENTE con este ejemplo:
  for widget in contenedor.winfo_children():
    if isinstance(widget, ctk.CTkLabel) and str(widget) == "aviso_temporal":
      if widget.winfo_exists():
        widget.destroy()
      break

  if not texto:
    return
  
  color_actual = contenedor.cget("fg_color")  # color de fondo del contenedor

  aviso = ctk.CTkLabel(contenedor, text=texto, text_color=color, font=("Arial", 10, "bold"))
  aviso.configure(fg_color=color_actual)
  aviso.place(relx=0.5, rely=0.9, anchor="center")
  contenedor.after(milisegundos, aviso.destroy)