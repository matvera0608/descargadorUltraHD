import customtkinter as ctk
from Elementos import *

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

def crearBotón(contenedor, texto, comando, imagen,  ancho=50, alto=25, fuente=("Arial", 10), colorFondo=colors["background"], colorLetra=colors["background"], hover=colors["background"], estado="disabled"):
     return ctk.CTkButton(contenedor, text=texto, command= lambda: comando(), image=imagen, compound="top", width=ancho, height=alto,
     corner_radius=8, font=fuente, fg_color=colorFondo, hover_color=hover, text_color=colorLetra, cursor="hand2", state=estado)
     
def crearMenú(barra_menu):
     return tk.Menu(barra_menu, tearoff=0)