# Script para enviar un mensaje de whatsapp desde python.
# Requiere instalar las librerías pywhatkit y flask.
# Pide el número, mensaje y hora de envío y lo lleva a cabo desde whatsapp web, que se abre automáticamente para realizar el envío.
# El código del país del número, se pone por defecto hardcodeado, pero se podría pedir al usuario también.


import pywhatkit

numero = input("Introduce el número de teléfono: ")
numero = "+34 "+numero
print(numero)

msg = input("Introduce el mensaje que desea enviar: ")

hora = input("Introduce la hora a la que desea enviar el mensaje (00-23): ")
while(int(hora) not in range(0, 24)):
    hora = input("Introduce la hora a la que desea enviar el mensaje (00-23): ")
    print(hora in range(0,24))

minuto = input("Introduce el minuto en el que desea enviar el mensaje (00-59): ")
while(int(minuto) not in range(0, 60)):
    minuto = input("Introduce el minuto en el que desea enviar el mensaje (00-59): ")

pywhatkit.sendwhatmsg(numero, msg, int(hora), int(minuto))

