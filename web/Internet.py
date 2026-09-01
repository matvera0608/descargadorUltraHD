import urllib.request, urllib.error


def verificar_conexión_a_internet(url="http://www.google.com", timeout=5):
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except urllib.error.URLError:
        return False