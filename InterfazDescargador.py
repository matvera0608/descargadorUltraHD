import customtkinter as ctk
import tkinter as tk
from Downloader import *
from ImagenesImportadas import *
from Elementos import *
from yt_dlp_UPDATES import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def crearMarco(contenedor, ancho=500, alto=500):
     return ctk.CTkFrame(contenedor, width=ancho, height=alto)

def crearBotónChequeo(contenedor, texto, variable_de_selección, fuente=("Arial", 10), estado="disabled"):
     return ctk.CTkCheckBox(contenedor, text=texto, font=fuente, variable=variable_de_selección, state=estado)

def crearListaDesplegable(contenedor, valor=["mp4", "mp3"], ancho=10, estado="readonly"):
     return ctk.CTkComboBox(contenedor, values=valor, width=ancho, state=estado)

def crearEtiqueta(contenedor, texto, fuente=("Arial", 10)):
     return ctk.CTkLabel(contenedor, text=texto, font=fuente)

def crearEntradaLink(contenedor, ancho=40, fuente=("Arial", 10), estado="disabled"):
     return ctk.CTkEntry(contenedor, width=ancho, font=fuente, state=estado)

def crearBotón(contenedor, texto, comando, imagen,  ancho=50, alto=25, fuente=("Arial", 10), colorFondo="blue", colorLetra="white", hover="#1d4ed8", estado="disabled"):
     return ctk.CTkButton(contenedor, text=texto, command= lambda: comando(), image=imagen, compound="top", width=ancho, height=alto,
                          corner_radius=8, font=fuente, fg_color=colorFondo, hover_color=hover, text_color=colorLetra, cursor="hand2", state=estado)

def habilitar(evento=None):
     entry_Link.configure(state="normal")

     link_valor = entry_Link.get().strip()
     
     if link_valor:
          chBox_subtitular.configure(state="normal")
          btnDescargar.configure(state="normal")
     else:
          chBox_subtitular.configure(state="disabled")
          btnDescargar.configure(state="disabled")


interfaz = ctk.CTk()
interfaz.title("aTube Ramiro")
interfaz.geometry("500x500")
interfaz.iconbitmap(ícono)

# Crear la barra de menú con tk.Menu
barra_menu = tk.Menu(interfaz)
interfaz.config(menu=barra_menu)

menu_opciones = tk.Menu(barra_menu, tearoff=0)
menu_opciones.add_command(label="Traducir", command=lambda: print("Traduciendo..."))
menu_opciones.add_command(label="Importar", command=lambda: print("Importando..."))
menu_opciones.add_command(label="Exportar", command=lambda: print("Exportando..."))
barra_menu.add_cascade(label="Opciones", menu=menu_opciones)

# Menú Ayuda
menu_ayuda = tk.Menu(barra_menu, tearoff=0)
menu_ayuda.add_command(label="Manual", command=lambda: print("Mostrar manual"))
menu_ayuda.add_command(label="Métodos abreviados", command=lambda: print("Mostrar atajos"))
menu_ayuda.add_separator()
menu_ayuda.add_command(label="Salir", command=interfaz.quit)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)


crearEtiqueta(interfaz, "Elige el formato: ", ("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
cbBox_formatos = crearListaDesplegable(interfaz)
cbBox_formatos.set("mp4")
cbBox_formatos.place(relx=0.45, rely=0.2, relwidth=0.2)
cbBox_formatos.configure(command = lambda e: habilitar())
#Para mí es mucho más práctico usar configure que command habilitar porque la diferencia es que este tira un error de que las variables no están definidas.

bool_subtitular = ctk.BooleanVar(value=False)

chBox_subtitular = crearBotónChequeo(interfaz, "Descargar\nSubtítulos", bool_subtitular)
chBox_subtitular.place(relx=0.825, rely=0.45)

crearEtiqueta(interfaz, "Introduce el link de video. Apto para cualquier plataforma: ").place(relx=0.5, rely=0.35, anchor="center")
entry_Link = crearEntradaLink(interfaz)
entry_Link.place(relx=0.15, rely=0.45, relwidth=0.65)
entry_Link.bind("<KeyRelease>", habilitar)

imagenDescargar = cargar_imagen("imágen", "download.png")

btnDescargar = ctk.CTkButton(interfaz, text="", command=lambda: descargar(interfaz, entry_Link.get(), cbBox_formatos.get(), chBox_subtitular.get()),
               image=imagenDescargar, width=50, height=50, fg_color=colors["background"],
               hover_color=colors["background"], corner_radius=0, cursor="hand2", state="disabled")
btnDescargar.place(relx=0.5, rely=0.7, anchor="center")

interfaz.mainloop()