import os, shutil

def contiene_sessdata(ruta="cookies.txt"):
    with open(os.path.abspath(ruta), encoding="utf-8") as f:
        contenido = f.read()
    if "SESSDATA" in contenido:
        print("✅ Cookie SESSDATA detectada. Sesión activa confirmada.")
        return True
    else:
        print("⚠ No se encontró SESSDATA. Puede que no estés logueado o que la cookie esté vencida.")
        return False

#Mover cookies mueve los cookies al destino de la carpeta.
def mover_cookies(origen=r"C:\Users\veram\Downloads\cookies.txt", destino=r"C:\Users\veram\AppData\Roaming\yt-dlp\cookies.txt"):
    if os.path.exists(origen):
        shutil.move(origen, destino)
        print(f"✅ Archivo cookies.txt movido a:\n{destino}")
    else:
        print("⚠ No se encontró cookies.txt en la ubicación actual. Exportalo desde Chrome primero.")