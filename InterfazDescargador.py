from tkinter import ttk as tkModerno
import tkinter as tk
import os
from Downloader import descargar

dirección = os.path.dirname(__file__)
ícono = os.path.join(dirección, "descargador.ico")

os.system("yt-dlp -U")


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
     btnDescargar.config(state="normal")


interfaz = tk.Tk()
interfaz.title("aTube Ramiro")
interfaz.resizable(False, False)
interfaz.iconbitmap(ícono)

crearEtiqueta(interfaz, "Elige el formato: ").grid(row=0, column=0)
cbBox_formatos = crearListaDesplegable(interfaz)
cbBox_formatos.current(0)
cbBox_formatos.grid(row=1, column=0, pady=20)
cbBox_formatos.bind("<<ComboboxSelected>>", habilitar)

entry_Link = crearEntradaLink(interfaz)
entry_Link.grid(row=3, column=0, pady=20)

crearEtiqueta(interfaz, "Introduce el link de video. Apto para cualquier plataforma: ").grid(row=2, column=0)
btnDescargar = crearBotón(interfaz, "DESCARGAR", lambda: descargar(entry_Link.get(), cbBox_formatos.get()))
btnDescargar.grid(pady=30)

interfaz.mainloop()