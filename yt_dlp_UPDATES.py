import asyncio
import sys
import datetime
from importlib.metadata import version, PackageNotFoundError

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


async def desinstalar_paquete(paquete):
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "pip", "uninstall", "-y", paquete,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    await proc.wait()
    print(f"⛔ {paquete} desinstalado por error en instalación.")
    
async def instalar_paquete(paquete):
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "pip", "install", "-U", paquete,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    await proc.wait()
    print(f"✅ {paquete} reinstalado correctamente.")

async def actualizar_ctk():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "pip", "install", "--upgrade", "customtkinter",
        stdout=asyncio.subprocess.DEVNULL, 
        stderr=asyncio.subprocess.DEVNULL
    )
    await proc.wait()
    
    if proc.returncode != 0:
        print("⚠ Error al actualizar CustomTkinter. Intentando reinstalación limpia...")
        await desinstalar_paquete("customtkinter")
        await instalar_paquete("customtkinter")
    else:
        print("✅ CustomTkinter actualizado correctamente.")

async def actualizar_ytdlp():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "pip", "install", "-U", "yt-dlp",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    await proc.wait()

    if proc.returncode != 0:
        print("⚠ Error al actualizar yt-dlp. Intentando reinstalación limpia...")
        await desinstalar_paquete("yt-dlp")
        await instalar_paquete("yt-dlp")
    else:
        print("✅ yt-dlp actualizado correctamente.")

async def main():
    await asyncio.gather(actualizar_ctk(), actualizar_ytdlp())

if __name__ == "__main__":
    try:
        print("Versión actual de yt-dlp:", version("yt-dlp"))
    except Exception:
        print("⚠ yt-dlp no está instalado, instalando...")
    asyncio.run(main())
    print("🎉 Actualización completada sin salida cargada.")