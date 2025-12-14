from ImagenesImportadas import *
import customtkinter as ctk
import re, os
import tkinter as tk

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
        1080: {"excelente": 2000.0, "buena": 1200.0, "regular": 800.0, "mala": 400.0},
        720:  {"excelente": 1200.0, "buena": 800.0,  "regular": 500.0, "mala": 250.0},
        540:  {"excelente": 900.0,  "buena": 600.0,  "regular": 350.0, "mala": 200.0},
        480:  {"excelente": 700.0,  "buena": 450.0,  "regular": 300.0, "mala": 150.0},
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


ventanaProgreso = None

urlHTTP = re.compile(r'^https?://([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?$')

def cerrar_seguro(ventana):
  try:
    if ventana and ventana.winfo_exists():
      ventana.destroy()
  except tk.TclError:
    pass

def mostrar_seguro(ventana):
  try:
    if ventana and ventana.winfo_exists():
      ventana.deiconify()
  except tk.TclError:
    pass

def descarga_segura_resistente_a_fallos(widget, acción):
  if widget.winfo_exists():
    widget.after(0, acción)

def limpiar_ansi(texto):
    """Elimina los códigos ANSI (colores de consola) del texto."""
    if not texto:
        return texto
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', texto)

def mostrar_descarga():
  global barra, lbl_porcentaje, lbl_estado, ventanaProgreso
  
  fuente_letra = ("Arial", 15)
  
  # --- Ventana de progreso ---
  ventanaProgreso = ctk.CTkToplevel()
  ventanaProgreso.title("En proceso")
  ventanaProgreso.geometry("600x100")
  ventanaProgreso.resizable(False, False)
  ventanaProgreso.configure(fg_color=colors["background"])
  ventanaProgreso.iconbitmap(ícono)
  
  ventanaProgreso.lift()
  ventanaProgreso.focus_force()
  ventanaProgreso.attributes("-topmost", True)
  ventanaProgreso.after(100, lambda: ventanaProgreso.attributes("-topmost", False))
  lbl_estado = ctk.CTkLabel(ventanaProgreso, text="Descargando video...", font=fuente_letra)
  lbl_estado.pack(pady=10)

  barra = ctk.CTkProgressBar(ventanaProgreso, width=250)
  barra.pack(pady=10)
  barra.set(0)

  lbl_porcentaje = ctk.CTkLabel(ventanaProgreso, text="0%", font=fuente_letra)
  lbl_porcentaje.pack(pady=5)
  
  ventanaProgreso.grab_set()
  
  if not all([barra, lbl_porcentaje, lbl_estado, ventanaProgreso]):
    print("⚠ La ventana de progreso no está inicializada.")
    return

# --- Hook de progreso (definido dentro) --- El hook es una función que se llama periódicamente
# durante la descarga para actualizar la interfaz de usuario
def hook_progreso(d):
  try:
    temp_file = d.get('filename')
    velocidad = limpiar_ansi(d.get('_speed_str', 'N/A')) #Esto ayuda a mejorar la precisión de la velocidad con la que se descarga
    eta = limpiar_ansi(d.get('_eta_str', 'N/A'))
    if d['status'] == 'downloading':
      total = d.get('total_bytes') or d.get('total_bytes_estimate')
      porcentaje = (d['downloaded_bytes'] / total) * 100 if total else 0
      descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_estado.configure(text=f"Velocidad: {velocidad} | ETA: {eta}"))
      if porcentaje >= 50:
        descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_estado.configure(text=f"Más de la mitad descargada | Velocidad: {velocidad}")) #Imprimimos la velocidad cuando está mayor que 50, porque es la mitad de 100
      descarga_segura_resistente_a_fallos(barra, lambda: barra.set(porcentaje / 100))
      descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_porcentaje.configure(text=f"{porcentaje:.1f}%"))
    elif d['status'] == 'finished':
      descarga_segura_resistente_a_fallos(barra, lambda: barra.set(1))
      descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_porcentaje.configure(text="100%"))
      descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_estado.configure(text="✅ Descarga completada."))
      if ventanaProgreso and ventanaProgreso.winfo_exists(): #Ahora ejecuta el cierre de la ventana de progreso cuando la descarga se completa o cancela
        ventanaProgreso.after(1500, ventanaProgreso.destroy)
        ventanaProgreso.attributes("-topmost", False)
    else:
      descarga_segura_resistente_a_fallos(lbl_estado, lambda: lbl_estado.configure(text="❌ Descarga fallida."))
      if ventanaProgreso and ventanaProgreso.winfo_exists():
        ventanaProgreso.after(1500, ventanaProgreso.destroy)
        if temp_file and os.path.exists(temp_file) and temp_file.endswith('.part'):
          try:
            os.remove(temp_file)
          except Exception as e:
            print(f"No se pudo eliminar el archivo temporal: {e}")
                      
  except Exception as e:
    print(f"Error en el hook de progreso: {e}")
    try:
      os.remove(temp_file)
    except Exception as e:
      print(f"No se pudo eliminar el archivo temporal: {e}")


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