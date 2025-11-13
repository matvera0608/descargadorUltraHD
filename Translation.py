from yt_dlp import YoutubeDL

def listar_lenguas(url): #Esta función se encarga de listar los idiomas de los subtítulos disponibles:  para ello usa yt-dlp, YouTube Downloader Plus
    global info
    ydl_opts_info = {"listsubtitles": True}
    with YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
    return info.get("subtitles", {})