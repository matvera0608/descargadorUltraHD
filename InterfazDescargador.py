import tkinter as tk, threading
from Downloader import *
from Widgets import *
from ImagenesImportadas import *
from Elementos import *
from Subtitling import obtener_subtítulos_disponibles
from yt_dlp_UPDATES import *
from FFMPEG import limpiar_basura

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
               entry_Link.configure(text_color=colors["error"])
            
          if evento and evento.type == "FocusOut":
               if not urlHTTP.match(link_valor):
                    entry_Link.delete(0, tk.END)
    except tk.TclError:
        pass


def cargar_subtitulos(evento=None):
     url = entry_Link.get().replace(" ", "").strip()

     if not urlHTTP.match(url):
          return

     ruta_de_cookie = None

     if "bilibili" in url.lower():
          ruta_de_cookie = procesar_cookies()
     
     print("🔎 URL para buscar subtítulos:", url)
     
     idiomas, info = obtener_subtítulos_disponibles(url, ruta_de_cookie)

     print("📝 IDIOMAS ENCONTRADOS:", idiomas)

     cbBox_subtitulos.configure(values=idiomas)

     if idiomas:
          cbBox_subtitulos.set(idiomas[0])
     else:
          cbBox_subtitulos.set("")

interfaz = ctk.CTk()
interfaz.title("aTube Ramiro")
interfaz.geometry("500x500")
interfaz.iconbitmap(ícono)

def cerrar_app(evento=None):
     try:
          limpiar_basura()
     except Exception:
          pass

     interfaz.destroy()

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
menu_ayuda.add_command(label="Salir", command=cerrar_app)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)


crearEtiqueta(interfaz, "Elige el formato: ", ("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
cbBox_formatos = crearListaDesplegable(interfaz)
cbBox_formatos.set("mp4")
cbBox_formatos.place(relx=0.45, rely=0.2, relwidth=0.2)
cbBox_formatos.configure(command = lambda e: habilitar())

crearEtiqueta(interfaz, "Introduce el link de video. Apto para cualquier plataforma: ").place(relx=0.5, rely=0.35, anchor="center")
entry_Link = crearEntradaLink(interfaz)
entry_Link.place(relx=0.15, rely=0.45, relwidth=0.65)
entry_Link.bind("<KeyRelease>", habilitar)
entry_Link.bind("<FocusOut>", cargar_subtitulos)


bool_subtitular = ctk.BooleanVar(value=False)
bool_traducir = ctk.BooleanVar(value=False)

chBox_traducir = crearBotónChequeo(interfaz, "Traducir\nSubtítulos", bool_traducir)
chBox_traducir.place(relx=0.825, rely=0.6)

chBox_subtitular = crearBotónChequeo(interfaz, "Descargar\nSubtítulos", bool_subtitular)
chBox_subtitular.place(relx=0.825, rely=0.7)

crearEtiqueta(interfaz, "Subtítulos disponibles: ", ("Arial", 10)).place(relx=0.9, rely=0.35, anchor="center")
cbBox_subtitulos = crearListaDesplegable(interfaz, [])
cbBox_subtitulos.place(relx=0.82, rely=0.45, relwidth=0.10)


imagenDescargar = cargar_imagen("imágen", "download.png")


btnDescargar = ctk.CTkButton(interfaz, text="", command=lambda: descargar(interfaz, entry_Link.get(), cbBox_formatos.get(), chBox_subtitular.get(), cbBox_subtitulos.get()),
image=imagenDescargar, width=50, height=50, fg_color=colors["background"],
hover_color=colors["background"], corner_radius=0, cursor="hand2", state="disabled")
btnDescargar.place(relx=0.5, rely=0.7, anchor="center")

def actualizar_ytdlp_background():
     asyncio.run(actualizar_ytdlp())

def actualizar_python():
    asyncio.run(actualizar_pip())

def iniciar_preparación_FFMPEG():
     
     actualizar_progreso, actualizar_estado, frame = mostrar_descarga_FFMPEG(interfaz)
     
     def tarea():
          ruta = descargar_FFMPEG(progreso=actualizar_progreso, estado=actualizar_estado)
          
          if ruta:
               interfaz.after(100, frame.destroy)
               
     threading.Thread(target = tarea, daemon=True).start()

interfaz.protocol("WM_DELETE_WINDOW", cerrar_app)

if __name__ == "__main__":
     
     limpiar_basura()
     
     interfaz.after(0, iniciar_preparación_FFMPEG)
     
     if not getattr(sys, "frozen", False):
          threading.Thread(target = actualizar_ytdlp_background, daemon = True).start()
          threading.Thread(target = actualizar_python, daemon = True).start()
     
     
     interfaz.mainloop()