# Script para crear una BD sencilla con sqlite3 desde python

import sqlite3

miConexion = sqlite3.connect("PruebaDB")

cursor = miConexion.cursor()

cursor.execute("""
    CREATE TABLE VEHICULOS (
        MATRICULA VARCHAR(10) PRIMARY KEY,
        MODELO VARCHAR(15),
        PRECIO INTEGER,
        COLOR VARCHAR(15)
    )
    """)

data = [
    ("1234-ABC", "Mercedes", "15000", "Gris"),
    ("5678-GQE", "BMW", "12000", "Rojo"),
    ("5947-POG", "Renault", "10000", "Azul"),
    ("9875-PMN", "Toyota", "11000", "Blanco"),
    ("4712-WER", "Seat", "10500", "Negro")
]

cursor.executemany("INSERT INTO VEHICULOS VALUES (?,?,?,?)", data)

miConexion.commit() # Guardar los cambios realizados en la BD

miConexion.close()