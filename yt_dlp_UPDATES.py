import asyncio
import sys
import datetime, importlib.util
from importlib.metadata import version, PackageNotFoundError

def paquete_instalado(paquete):
    try:
        version_actual = version(paquete)
        return True, version_actual
    except PackageNotFoundError:
        return False, None

def registrar_version(paquete, archivo_log="paquetes_log.txt"):
    try:
        version_actual = version(paquete)
    except PackageNotFoundError:
        version_actual = "No instalado"

    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{fecha}] {paquete}: {version_actual}\n"

    with open(archivo_log, "a", encoding="utf-8") as f:
        f.write(linea)

    print(f"📜 Registro guardado en {archivo_log}")

### FUNCIONES ASÍNCRONAS

async def comprobar_Pillow():
    existe, ver = paquete_instalado("Pillow")
    if existe:
        print(f"✅ Pillow está instalado (versión {ver})")
        return existe
    else:
        print("❌ Pillow no está instalado")
        ok = await instalar_paquete("Pillow")
        return ok
    

async def comprobar_pip():
    existe, ver = paquete_instalado("pip")
    if existe:
        print(f"✅ pip está instalado (versión {ver})")
        return existe
    else:
        print("❌ pip no está instalado")
        ok = await instalar_paquete("pip")
        return ok


async def desinstalar_paquete(paquete):
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "pip", "uninstall", "-y", paquete,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode == 0:
        print(f"⛔ {paquete} desinstalado correctamente.")
        return True

    print(f"⚠ Error al desinstalar {paquete}.")
    if stderr:
        print(stderr.decode(errors="replace"))

    return False
    
async def instalar_paquete(paquete):
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "pip", "install", "-U", paquete,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode == 0:
        print(f"✅ {paquete} instalado correctamente.")
        return True

    print(f"⚠ Error al instalar {paquete}.")
    if stderr:
        print(stderr.decode(errors="replace"))

    return False

async def actualizar_ctk():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "pip", "install", "--upgrade", "customtkinter",
        stdout=asyncio.subprocess.DEVNULL, 
        stderr=asyncio.subprocess.PIPE
    )
    await proc.wait()
    
    if proc.returncode != 0:
        print("⚠ Error al actualizar CustomTkinter. Intentando reinstalación limpia...")
        await desinstalar_paquete("customtkinter")
        await instalar_paquete("customtkinter")
    else:
        print("✅ CustomTkinter actualizado correctamente.")


    await proc.wait()

    return proc.returncode == 0


async def actualizar_ytdlp():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE
    )

    _, stderr = await proc.communicate()

    if proc.returncode != 0:
        print("⚠ Error al actualizar yt-dlp. Intentando reinstalación limpia...")
        await desinstalar_paquete("yt-dlp")
        await instalar_paquete("yt-dlp")
        return False

    print("✅ yt-dlp actualizado correctamente.")
    return True

async def actualizar_pip():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "pip", "install", "--upgrade", "pip",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await proc.communicate()

    if proc.returncode != 0:
        print("⚠ Error al actualizar pip.")
        if stderr:
            print(stderr.decode(errors="replace"))
        return False

    print("✅ pip actualizado correctamente.")
    return True
    
    
async def main():
    

    await comprobar_Pillow()
    await comprobar_pip()
    
    await actualizar_pip()
    await actualizar_ctk()
    await actualizar_ytdlp()



if __name__ == "__main__":
    asyncio.run(main())
    
    try:
        print("Versión actual de yt-dlp:", version("yt-dlp"))
    except PackageNotFoundError:
        print("⚠ yt-dlp todavía no está instalado.")