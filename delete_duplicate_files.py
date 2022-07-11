# Dadas dos carpetas, elimina los archivos duplicados que se encuentren en ambas carpetas

import os

ruta1 = ("ruta1")
ruta2 = ("ruta2")

archivos1 = os.listdir(ruta1)
archivos2 = os.listdir(ruta2)

for i in archivos1:
    for j in archivos2:
        if i == j:
            print("Eliminando el archivo ",i,"...")
            os.chdir(ruta1)
            os.remove(i)
