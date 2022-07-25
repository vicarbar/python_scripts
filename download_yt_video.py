# Descargar vídeo de Youtube desde python en formato mp4. En el ejemplo se usa un vídeo de MrBeastEspañol

from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=28lCT6FdDFo&ab_channel=MrBeastenEspa%C3%B1ol")

# Máxima resolución posible
video = yt.streams.get_highest_resolution()

video.download()