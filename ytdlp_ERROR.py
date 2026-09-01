def mostrar_mensajes_de_errores_específicos(error):
       mensaje = str(error).lower()
       
       if "not available in your region" in mensaje:
              return "🚫 El contenido no está disponible en tu región."

       if "may be deleted or geo-restricted" in mensaje:
              return "🗑️ El video puede haber sido eliminado o estar restringido geográficamente."

       if "private" in mensaje:
              return "El contenido es privado."

       if "login" in mensaje or "authentication" in mensaje:
              return "Este contenido requiere autenticación."

       if "video unavailable" in mensaje:
              return "El video no está disponible."

       if "unable to download" in mensaje:
              return "No se pudo descargar el contenido."

       return "yt-dlp no pudo procesar este contenido."