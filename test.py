# Librerias
import os
import pandas as pd # 1.3.4
import json # 2.0.9
import csv # 1.0
from collections import Counter


################################
# FUNCTIONS
################################


# Crea el fichero .csv donde se guardaran las variables amount of tip, extra payment y trip distance, necesarias para calcular la metrica 3
def create_csv_metric3():
    number_json = len(os.listdir('json_files'))
    if number_json == 0:
        with open("/files/data_metrica3.csv", "w") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['amount_of_tip', 'extra_payment', 'trip_distance'])

# Actualiza el fichero .csv que guarda los valores de las variables amount of tip, extra payment y trip distance, necesarias para calcular la metrica 3
# Parametro: conjunto de datos
def store_metric3_values(data):
    amount_of_tip = data['tip_amount'].sum()
    extra_payment = data['extra'].sum()
    trip_distance = data['trip_distance'].sum()
    datos_old = pd.read_csv("/files/data_metrica3.csv")
    if len(datos_old) > 0:
        amount_of_tip = amount_of_tip + float(datos_old.iloc[:,0])
        extra_payment = extra_payment + float(datos_old.iloc[:,1])
        trip_distance = trip_distance + float(datos_old.iloc[:,2])
    row = [amount_of_tip, extra_payment, trip_distance]
    with open("/files/data_metrica3.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['amount_of_tip', 'extra_payment', 'trip_distance'])
        writer.writerow(row)

# Obtiene la primera metrica: precio medio por milla viajada por los clientes
# Parametro: conjunto de datos
# Return: metrica calculada, float
def average_per_mile(data):
    millas = data['trip_distance'].sum()
    precio = data['total_amount'].sum()
    average_per_mile = millas/precio
    return(average_per_mile)

# Obtiene la segunda metrica: distribucion de los tipos de pago
# Parametro: conjunto de datos
# Return: metrica calculada, diccionario con claves = tipos de pago y valor = numero de viajes pagados con cada tipo de pago
def payment_types_distribution(data):
    indices = data[data['payment_type'] == 0].index
    data = data.drop(indices)
    total = data['payment_type'].value_counts(sort = False)
    payment_types = pd.DataFrame({'Total': total})
    return(payment_types)

# Obtiene la tercera metrica: (amount of tip + extra payment) / trip distance
# Para ello lee la informacion almacenada en el documento csv que almacena la suma acumuladad de los datos acumulados de esas 3 variables
# Return: metrica calculada, float
def custom_indicator():
    data_metrica3_old = pd.read_csv('/files/data_metrica3.csv')
    amount_of_tip = data_metrica3_old.iloc[:,0]
    extra_payment = data_metrica3_old.iloc[:,1]
    trip_distance = data_metrica3_old.iloc[:,2]
    return((float(amount_of_tip) + float(extra_payment))/float(trip_distance))

# Obtiene las 3 metricas deseadas y las almacena en un diccionario, para su posterior almacenamiento en fichero .json
# Parametro: conjunto de datos
# Return: metricas, diccionario
def calculate_metrics(data):
    metrica1 = average_per_mile(data)
    metrica2 = payment_types_distribution(data)
    metrica3 = custom_indicator()
    metrics = {
        'metrica1': metrica1,
        'metrica2': metrica2.to_dict(),
        'metrica3': metrica3
    }
    return(metrics)

# Obtiene el numero de la fecha de cada dia en formato <ano><mes><dia>, de forma concatenada
# Parametro: conjuto de datos
# Return: numero de la fecha, string
def getDateNumber(data):
    year = data.iloc[0, 1].year
    month = data.iloc[0, 1].month
    day = data.iloc[0, 1].day
    return(str(year) + str(month).zfill(2) + str(day).zfill(2))

# Genera el fichero .json que almacena las metricas para un dia concreto
# Parametros: 
#   - metricas: metricas calculadas para un dia
#   - nombre: nombre del fichero, es el numero del dia obtenido con @getDateNumber
def generateJSON(metricas, nombre):
    json_object = json.dumps(metricas, indent = 4)
    with open("/files/json_files/" + nombre + "_yellow_taxi_kpis.json", "w") as outfile:
        outfile.write(json_object)
   
    
################################
# END FUNCTIONS
################################



# Listado de ficheros de datos disponibles
files = os.listdir('/files/data')
# Numero total de ficheros de datos disponibles
cont_files = len(files)

# Para ver que fichero/s son los que se han anadido, es necesario tenerlos ordenados por instante de creacion (ya que se entiende que el de un dia sera creado posteriormente
# que el del dia anterior). Como los nombres de los ficheros no se nos indica que determinen cual se ha creado antes, miramos la hora en la que se ha creado en las caracteristicas
# de cada fichero.
tiempos = []
for i in files:
    tiempos.append(os.path.getctime('/files/data/' + i)) # obtener la fecha y hora de creacion de cada fichero
# Se ordenan por fecha y hora de creacion (mas reciente el ultimo)
files = [i for _,i in sorted(zip(tiempos,files))]

# Se crea el fichero que guardara las variables de la metrica 3
create_csv_metric3()


##############################################################################################################################################################################
# Bucle principal, se actualizan las distintas metricas de forma que se obtienen los valores acumulados para cada dia, es decir, para el dia 2, se obtendran las metricas
# teniendo en cuenta la informacion del dia 1 y del dia 2. Y asi sucesivamente.
##############################################################################################################################################################################

# Se mira en primer lugar cuantos ficheros .json se tienen ya creados (para cuantos dias se han obtenido ya las metricas)
number_json = len(os.listdir('/files/json_files'))
# Se mira a su vez cuantos ficheros de datos hay. La diferencia entre el numero de ficheros de datos y el numero de ficheros .json indica el numero de dias para los cuales
# hay que obtener aun las metricas.
number_data = len(files)
# Se recorren los ficheros de datos para los cuales no se han obtenido las metricas y se obtienen, teniendo en cuenta la totalidad de los dias anteriores.
for i in range(number_json, number_data): 
    # Se lee el fichero de datos correspondiente
    datos = pd.read_parquet('/files/data/' + files[i], engine = 'pyarrow')
    # Se guardan los datos para la metrica 3
    store_metric3_values(datos) 
    # Se calculan las metricas
    metrics = calculate_metrics(datos)
    # Se obtiene el nombre del fichero .json que se va a generar
    nombre = getDateNumber(datos)
    
    # Si NO es el primer fichero que se genera...
    if i != 0:
        # Lectura del ultimo json creado. Se tiene en cuenta que estos ficheros SI se ordenan por nombre
        jsons = sorted(os.listdir('/files/json_files'))
        with open('/files/json_files/' + jsons[-1], 'r') as openfile:
            metric_old = json.load(openfile)

        # Actualizacion de la primera metrica
        metrics['metrica1'] = (i * metric_old['metrica1'] + metrics['metrica1'])/(i + 1)
        
        # Actualizacion de la segunda metrica
        # Para ello, como los dos diccionarios que se comparan pueden tener distintas claves o estar estas ordenadas de distinta manera, utilizamos la funcion Counter de la 
        # libreria collections, que resuelve este problema. 
        # Como al leer el .json las claves aparecen como enteros en lugar de como strings, tenemos que volver a generarlas (segundo termino del sumatorio)
        metrics['metrica2'] = {'Total': dict(Counter(metric_old['metrica2']['Total']) + Counter({str(k): v for k, v in metrics['metrica2']['Total'].items()}))}
    # Generacion del nuevo fichero .json
    generateJSON(metrics, nombre)

