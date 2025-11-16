import os, shutil, glob

carpeta_de_cookies = os.path.join(os.path.expanduser("~"), "Downloads")
carpeta_destino_cookies = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "yt-dlp", "cookies.txt")

def procesar_cookies():
    archivos_de_cookies = glob.glob(os.path.join(carpeta_de_cookies, "*.txt"))
    if not archivos_de_cookies:
        print("No se encontraron archivos de cookies en la carpeta de descargas.")
        return False
    
    print(f"Archivos de cookies encontrados: {archivos_de_cookies}")
    
    mejor_archivo = None
    mejor_puntaje = -1

    for archivo in archivos_de_cookies:
        try:
            with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
                contenido = f.read()
        except Exception:
            continue

        puntaje = 0

        # +100 si contiene SESSDATA
        if "SESSDATA" in contenido:
            puntaje += 100

        # + tamaño del archivo (más grande = mejor)
        puntaje += os.path.getsize(archivo)

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_archivo = archivo

    if not mejor_archivo:
        print("⚠ No se encontró ninguna cookie válida.")
        return

    print(f"✅ Mejor cookie seleccionada: {os.path.basename(mejor_archivo)}")

    # Mover archivo
    os.makedirs(os.path.dirname(carpeta_destino_cookies), exist_ok=True)

    if os.path.exists(carpeta_destino_cookies):
        os.remove(carpeta_destino_cookies)

    shutil.move(mejor_archivo, carpeta_destino_cookies)
    print(f"📦 Cookie movida a: {carpeta_destino_cookies}")
    print("🎉 Listo para usar BiliBili con login.")