def listar_lenguas(url):
    global info
    ydl_opts_info = {"listsubtitles": True}
    with YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
   