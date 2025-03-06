from pytube import YouTube 
url = input("Ingresa la URL del video que deseas descargar: \n")
try: 
    video = YouTube(url)
except:
    print("Error de conexión")

download_video = video.streams.get_by_resolution("720p")

try:
    download_video.download('.')
except:
    print("Error al descargar el video")
print("Video descargado con éxito :D!")
