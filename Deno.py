import os, shutil, subprocess, glob

RUTA_DENO = os.path.join(
    os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages", "DenoLand.Deno_Microsoft.Winget.Source_8wekyb3d8bbwe", "deno.exe"
)

def buscar_deno():

       patron_winget = os.path.join(os.environ.get("LOCALAPPDATA", ""),
              "Microsoft",
              "WinGet",
              "Packages",
              "DenoLand.Deno*",
              "deno.exe",
              )

       archivos = glob.glob(patron_winget)
       return archivos[0] if archivos else None


def instalar_deno():
    winget = shutil.which("winget")
    if not winget:
       print("⚠️ No se encontró winget.")
       return None

    print("📦 Instalando Deno...")
    try:
       resultado = subprocess.run(
       [
              winget,
              "install",
              "--id",
              "DenoLand.Deno",
              "--exact",
              "--silent",
              "--accept-package-agreements",
              "--accept-source-agreements",
       ],
       capture_output=True,
       text=True,
       timeout=300,
       )
       if resultado.returncode != 0:
              print("⚠️ No se pudo instalar Deno:", resultado.stderr)
              return None

       print("✅ Deno instalado.")
       return buscar_deno()
    except Exception as e:
        print(f"⚠️ Error al instalar Deno: {e}")
        return None
       

def obtener_opciones_de_deno():

       ruta_deno = buscar_deno() or instalar_deno()
       
       if not ruta_deno:
            print("No se encontró Deno, se instalará")
            return {}
       
       print("\n✅ Deno y EJS configurados")
       
       return {
        "js_runtimes": {"deno": {"path": ruta_deno}},
        "remote_components": ["ejs:github"],
    }