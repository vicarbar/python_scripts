# Script para enviar un mensaje de whatsapp a un grupo desde python.
# Requiere instalar las librerías pywhatkit y flask.
# Pide el id del grupo, mensaje y hora de envío y lo lleva a cabo desde whatsapp web, que se abre automáticamente para realizar el envío.

import pywhatkit

id_grupo = "CP7mTJonXAGD9eP18ATpBQ" # Lo copiamos de "enlace de invitación al grupo" y eliminamos lo que sobra de la cadena de texto

msg = input("Introduce el mensaje que desea enviar al grupo: ")

hora = input("Introduce la hora a la que desea enviar el mensaje (00-23): ")
while(int(hora) not in range(0, 24)):
    hora = input("Introduce la hora a la que desea enviar el mensaje (00-23): ")
    print(hora in range(0,24))

minuto = input("Introduce el minuto en el que desea enviar el mensaje (00-59): ")
while(int(minuto) not in range(0, 60)):
    minuto = input("Introduce el minuto en el que desea enviar el mensaje (00-59): ")

pywhatkit.sendwhatmsg_to_group(id_grupo, msg, int(hora), int(minuto))