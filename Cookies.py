import os, shutil

destino_cookies = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "yt-dlp", "cookies.txt") #Esta variable es la ruta que usa yt-dlp para las cookies.
#Además es más flexible que hardcodearla.

origen_cookies=os.path.join(os.path.expanduser("~"), "Downloads", "cookies.txt"),


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
def mover_cookies(origen=origen_cookies, destino=destino_cookies):
    if os.path.exists(origen):
        if os.path.getsize(origen) < 100: #Si el archivo es menor a 100 bytes, probablemente esté vacío o incompleto. Es mejor avisar al usuario.
            print("⚠ El archivo de cookies parece estar vacío o incompleto.")
            return
        if os.path.exists(destino):
            os.remove(destino)
        shutil.move(origen, destino)
        print(f"✅ Archivo cookies.txt movido a:\n{destino}")
    else:
        print("⚠ No se encontró cookies.txt en la ubicación actual. Exportalo desde Chrome primero.")
        return