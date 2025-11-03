from tkinter import ttk as tkModerno
import os, customtkinter as ctk
from Downloader import descargar
from ImagenesImportadas import ícono, cargar_imagen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


os.system('pip install --upgrade customtkinter >nul 2>&1')
os.system('python -m yt_dlp -U >nul 2>&1')

def crearPestaña(contenedor, ancho=500, alto=500):
     return ctk.CTkTabview(contenedor, width=ancho, height=alto)

def crearListaDesplegable(contenedor, valor=["mp4", "mp3"], ancho=10, estado="readonly"):
     return tkModerno.Combobox(contenedor, values=valor, width=ancho, state=estado)

def crearEtiqueta(contenedor, texto, fuente=("Arial", 10)):
     return ctk.CTkLabel(contenedor, text=texto, font=fuente)

def crearEntradaLink(contenedor, ancho=40, fuente=("Arial", 10)):
     return ctk.CTkEntry(contenedor, width=ancho, font=fuente, state="disabled")

def crearBotón(contenedor, texto, comando, imagen, ancho=10, fuente=("Arial", 10), colorFondo="blue", colorLetra="white", estado="disabled"):
     return ctk.CTkButton(contenedor, text=texto, command= lambda: comando(),image=imagen, width=ancho, font=fuente, fg_color=colorFondo, text_color=colorLetra, cursor="hand2", state=estado)


def habilitar(evento=None):
     entry_Link.configure(state="normal")
     
     if entry_Link.get().strip():
          btnDescargar.configure(state="normal")
     else:
          btnDescargar.configure(state="disabled")



interfaz = ctk.CTk()
interfaz.title("aTube Ramiro")
interfaz.geometry("500x500")
interfaz.iconbitmap(ícono)

pestaña = crearPestaña(interfaz)
pestaña.pack(expand=True, fill="both")

pestaña.add("Opciones")
pestaña.add("Ayuda")

crearEtiqueta(interfaz, "Elige el formato: ").place(relx=0.5, rely=0.1, anchor="center")
cbBox_formatos = crearListaDesplegable(interfaz)
cbBox_formatos.current(0)
cbBox_formatos.place(relx=0.45, rely=0.2, relwidth=0.2)
cbBox_formatos.bind("<<ComboboxSelected>>", habilitar)

crearEtiqueta(interfaz, "Introduce el link de video. Apto para cualquier plataforma: ").place(relx=0.5, rely=0.35, anchor="center")
entry_Link = crearEntradaLink(interfaz)
entry_Link.place(relx=0.15, rely=0.45, relwidth=0.8)
entry_Link.bind("<KeyRelease>", habilitar)

imagenDescargar = cargar_imagen("imágen", "download.png")

btnDescargar = crearBotón(interfaz, "DESCARGAR", lambda: descargar(entry_Link.get(), cbBox_formatos.get()), imagenDescargar)
btnDescargar.place(relx=0.5, rely=0.7, anchor="center")
btnDescargar.configure(state="disabled")

interfaz.mainloop()