import customtkinter as ctk
import re
import tkinter as tk

# Paleta personalizada (usa tus hex o nombres preferidos)
colors = {
    "background": "#0f1724",
    "surface": "#111827",
    "primary": "#2563eb",
    "primary_hover": "#1d4ed8",
    "accent": "#06b6d4",
    "danger": "#ef4444",
    "text": "#ffffff",
    "successfully": "#12c23b",
    "alert": "#f5bb0b"
}

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