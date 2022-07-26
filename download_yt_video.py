# Descargar vídeo de Youtube desde python en formato mp4. El enlace del vídeo a descargar se le pide al usuario por entrada estándar.

from pytube import YouTube

enlace = input("Introduce el enlace del vídeo que desea descargar: ")

yt = YouTube(enlace)

# Máxima resolución posible
video = yt.streams.get_highest_resolution()

video.download()
