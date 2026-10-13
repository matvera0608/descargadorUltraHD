import os

RUTA_DENO = os.path.join(
    os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages", "DenoLand.Deno_Microsoft.Winget.Source_8wekyb3d8bbwe", "deno.exe"
)

def obtener_opciones_de_deno():
       
       if not os.path.isfile(RUTA_DENO):
              print("No se encontró deno")
              return {}
       
       print("\n✅ Deno y EJS configurados")
       
       return {
              
              "js_runtimes" : {
              "deno" : { 
                     "path": RUTA_DENO
                     }
              },
              "remote_components": ["ejs:github"]
       }