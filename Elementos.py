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