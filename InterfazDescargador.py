import tkinter as tk
from Downloader import *
from Widgets import *
from ImagenesImportadas import *
from Elementos import *
from yt_dlp_UPDATES import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def habilitar(evento=None):
    try:
          entry_Link.configure(state="normal")
          link_valor = entry_Link.get().replace(" ", "").strip()

          # Si está vacío: deshabilitar todo
          if not link_valor:
               chBox_subtitular.configure(state="disabled")
               btnDescargar.configure(state="disabled")
               return

          # Validar URL sin borrar texto
          if urlHTTP.match(link_valor):
               chBox_subtitular.configure(state="normal")
               btnDescargar.configure(state="normal")
               entry_Link.configure(text_color=colors["successfully"])
          else:
          # URL inválida → deshabilitar botones, pero NO borrar el texto
               chBox_subtitular.configure(state="disabled")
               btnDescargar.configure(state="disabled")
               entry_Link.configure(text_color=colors["danger"])
            
          if evento and evento.type == "FocusOut":
               if not urlHTTP.match(link_valor):
                    entry_Link.delete(0, tk.END)
    except tk.TclError:
        pass

interfaz = ctk.CTk()
interfaz.title("aTube Ramiro")
interfaz.geometry("500x500")
interfaz.iconbitmap(ícono)

# Crear la barra de menú con tk.Menu
barra_menu = crearMenú(interfaz)
interfaz.config(menu=barra_menu)

menu_opciones = crearMenú(barra_menu)
menu_opciones.add_command(label="Traducir", command=lambda: print("Traduciendo..."))
menu_opciones.add_command(label="Importar", command=lambda: print("Importando..."))
menu_opciones.add_command(label="Exportar", command=lambda: print("Exportando..."))
barra_menu.add_cascade(label="Opciones", menu=menu_opciones)

# Menú Ayuda
menu_ayuda = crearMenú(barra_menu)
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
bool_traducir = ctk.BooleanVar(value=False)

chBox_subtitular = crearBotónChequeo(interfaz, "Descargar\nSubtítulos", bool_subtitular)
chBox_subtitular.place(relx=0.825, rely=0.5)

chBox_traducir = crearBotónChequeo(interfaz, "Traducir\nSubtítulos", bool_traducir)
chBox_traducir.place(relx=0.825, rely=0.375)

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