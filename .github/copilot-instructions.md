# Copilot Instructions for DescargadorUltra

## Arquitectura general
- El proyecto consiste en un script principal (`Video downloader from all pages.py`) que descarga videos de diversas páginas usando `yt_dlp`.
- No hay módulos separados ni componentes complejos; toda la lógica está en un solo archivo Python.
- El flujo principal es interactivo: solicita al usuario la cantidad de videos, URLs, muestra las calidades disponibles y descarga según el formato elegido.

## Flujos críticos de desarrollo
- **Ejecución:** Ejecuta el script directamente con Python 3. Se recomienda usar la terminal de Windows PowerShell.
- **Dependencias:**
  - `yt_dlp` para la descarga de videos.
  - `tqdm` para la barra de progreso.
  - `ffmpeg` debe estar instalado y en el PATH para la conversión de formatos.
- **Ruta de descarga:** Los videos se guardan en `C:\Users\veram\Downloads\` con el nombre del título y extensión correspondiente.
- **Formato de salida:** El usuario debe ingresar el código de formato mostrado por `yt_dlp`.

## Convenciones y patrones específicos
- El script utiliza funciones para separar la obtención de URL, listado de calidades y descarga.
- Los errores de conexión y descarga se manejan con mensajes personalizados.
- El script está diseñado para uso interactivo en consola, no para automatización.
- No hay pruebas automatizadas ni integración continua configurada.

## Ejemplo de flujo de uso
1. Ejecuta el script.
2. Ingresa la cantidad de videos a descargar.
3. Para cada video:
   - Ingresa la URL.
   - El script muestra las calidades disponibles.
   - Ingresa el código de formato.
   - El video se descarga y convierte a MP4.

## Integraciones y puntos clave
- `yt_dlp` se usa tanto para listar formatos como para descargar.
- `ffmpeg` se usa internamente por `yt_dlp` para remux a MP4.
- No hay integración con otros servicios ni APIs externas.

## Archivos relevantes
- `Video downloader from all pages.py`: Toda la lógica principal.
- `.github/copilot-instructions.md`: Este archivo de instrucciones para agentes AI.

---

**Sugerencias para agentes AI:**
- Mantén la lógica interactiva y los mensajes claros para el usuario.
- Si agregas nuevas funciones, sigue el patrón de separación por responsabilidad.
- Documenta cualquier cambio relevante en este archivo.
