# Imprimir por salida estándar el porcentaje de batería del pc

import psutil

bateria = psutil.sensors_battery()
porcentaje = bateria.percent
porcentaje = round(porcentaje, 2)
print("El ordenador tiene un %s%% de batería" %porcentaje)