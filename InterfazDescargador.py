from tkinter import ttk as tkModerno
import tkinter as tk
import os, customtkinter
from Downloader import descargar
from ImagenesImportadas import ícono


os.system('python -m yt_dlp -U >nul 2>&1')

def crearListaDesplegable(contenedor, valor=["mp4", "mp3"], ancho=10, estado="readonly"):
     return tkModerno.Combobox(contenedor, values=valor, width=ancho, state=estado)

def crearEtiqueta(contenedor, texto, fuente=("Arial", 10)):
     return tk.Label(contenedor, text=texto, font=fuente)

def crearEntradaLink(contenedor, ancho=40, fuente=("Arial", 10)):
     return tk.Entry(contenedor, width=ancho, font=fuente, state="disabled")

def crearBotón(contenedor, texto, comando, ancho=10, fuente=("Arial", 10), colorFondo="blue", colorLetra="white", estado="disabled"):
     return tk.Button(contenedor, text=texto, command= lambda: comando(), width=ancho, font=fuente, bg=colorFondo, fg=colorLetra, cursor="hand2", state=estado)


def habilitar(evento=None):
     entry_Link.config(state="normal")
     
     if entry_Link.get().strip():
          btnDescargar.config(state="normal")
     else:
          btnDescargar.config(state="disabled")



interfaz = tk.Tk()
interfaz.title("aTube Ramiro")
interfaz.geometry("500x500")
interfaz.iconbitmap(ícono)

crearEtiqueta(interfaz, "Elige el formato: ").place(relx=0.5, rely=0.1, anchor="center")
cbBox_formatos = crearListaDesplegable(interfaz)
cbBox_formatos.current(0)
cbBox_formatos.place(relx=0.45, rely=0.2, relwidth=0.2)
cbBox_formatos.bind("<<ComboboxSelected>>", habilitar)

crearEtiqueta(interfaz, "Introduce el link de video. Apto para cualquier plataforma: ").place(relx=0.5, rely=0.35, anchor="center")
entry_Link = crearEntradaLink(interfaz)
entry_Link.place(relx=0.15, rely=0.45, relwidth=0.8)
entry_Link.bind("<KeyRelease>", habilitar)



btnDescargar = crearBotón(interfaz, "DESCARGAR", lambda: descargar(entry_Link.get(), cbBox_formatos.get()))
btnDescargar.place(relx=0.5, rely=0.7, anchor="center")
btnDescargar.config(state="disabled")

interfaz.mainloop()