
#inicio region Importaciones
import os  
import random as rnd  
import numpy as np 
import pandas as pd 
import datetime  
import logging  
import tqdm  
import warnings 
import platform  # Librería para información del sistema operativo
import getpass  # Librería para obtener el nombre del usuario
from timeit import default_timer as timer  # Para medir el tiempo de ejecución de código
warnings.filterwarnings('ignore') 
# fin region Importaciones

#########################################################
# Se utilizó el algoritmo del profesor como base para ejecutar el trabajo final
##########################################################

# inicio Configuración de logging
usuario = getpass.getuser() 
sistema_operativo = platform.system() 
plataforma = platform.platform() 

# Crear un archivo de log con la fecha y hora actuales en el nombre
nombre_archivo_log = f"log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=nombre_archivo_log, level=logging.INFO,
                    format='%(asctime)s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Registrar información del usuario y sistema en el log
logging.info(f"Usuario: {usuario}")
logging.info(f"Sistema Operativo: {sistema_operativo}")
logging.info(f"Plataforma: {plataforma}")
# fin region Configuración de logging

# log de eventos registro de cada cosa que se hace
def log_evento(mensaje):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            start_time = timer()
            result = func(*args, **kwargs) 
            end_time = timer() 
            duration = end_time - start_time 
            logging.info(f"{mensaje}\tDuración: {duration:.6f} segundos")
            return result
        return wrapped
    return wrapper


# region funciones
def GenerarNombre(Nombres: list, Apellidos: list) -> str:
    Nombre = rnd.choice(Nombres)
    Apellido = rnd.choice(Apellidos)
    return f'{Nombre} {Apellido}'
def GenerarEdad() -> int:
    r = rnd.random()
    if r < 0.5:
        return rnd.randint(16, 25)
    elif r < 0.75:
        return rnd.randint(26, 33)
    elif r < 0.9:
        return rnd.randint(34, 40)
    else:
        return rnd.randint(41, 85)
def GenerearSemestre() -> int:
    r = rnd.random()
    if r < 0.14:
        return 1
    elif r < 0.27:
        return 2
    elif r < 0.39:
        return 3
    elif r < 0.5:
        return 4
    elif r < 0.6:
        return 5
    elif r < 0.7:
        return 6
    elif r < 0.79:
        return 7
    elif r < 0.87:
        return 8
    elif r < 0.94:
        return 9
    else:
        return 10
# endregion funciones
# region Inicializacion de fechas y log
print('*'*100)
print(f'{"Inicio del proceso":>15}')
inicio = time.time() #Inicio contador de ejecucion
hoy = datetime.date.today().strftime('%Y%m%d') #Captura de fecha de ejecucion
nombre_archivo_log = f"log_{hoy}.log" # Inicializacion del log
#Configuracion de almacenamiento y niveles del log
logging.basicConfig(filename=nombre_archivo_log, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#Primer registro del log
logging.info("Iniciando el proceso, por CastilloEnterprises 😃😃😃👀✔")
# endregion Inicializacion de fechas y log

# region Gestion de archivos y ubicaciones
#Creamos el directorio (carpeta) en donde se crearan los archivos
DirectorioActual = os.getcwd()
textemp = f'El directorio actual de trabajo es: \n\t--> {DirectorioActual}, \nEsta carpeta contendrá los archivos del trabajo final'
print(textemp)
logging.info(textemp)
#Creamos una carpeta donde almacenamos los resultados
CarpetaNueva = "CarpetaArchivosTrabajoFinal"
os.makedirs(CarpetaNueva, exist_ok=True)
logging.info("Se crea el directorio {}".format(CarpetaNueva))
print(f"'{CarpetaNueva}' La carpeeta ha sido creada.")
# Nombre de la carpeta donde se crearán los archivos
carpeta = os.path.join(DirectorioActual, "CarpetaArchivosTrabajoFinal")
logging.info("La ruta de trabajo será {}".format(carpeta))
RutaNombres = r'NombresArgentina.csv'
RutaApellidos = r'ApellidosArgentina.csv'
RutaNombres = os.path.join(DirectorioActual, RutaNombres)
RutaApellidos = os.path.join(DirectorioActual, RutaApellidos)
logging.info("Cargando CSV con nombres")
dfNombres = pd.read_csv(RutaNombres, encoding='ISO-8859-1')
Nombres = dfNombres['name'].tolist()
logging.info("Reemplazando nombres y detalles del documento")
for i in tqdm.trange(len(Nombres)):
    if ' ' in Nombres[i]:
        Nombres[i]=Nombres[i].replace(' ', '_')
logging.info("Cargando CSV con apellidos")
dfApellidos = pd.read_csv(RutaApellidos, encoding='ISO-8859-1')
Apellidos = dfApellidos['lastname'].tolist()
logging.info("Reemplazando apellidos y detalles del documento")
for i in tqdm.trange(len(Apellidos)):
    if ' ' in Apellidos[i]:
        Apellidos[i]=Apellidos[i].replace(' ', '_')
logging.info("Finalizado proceso de gestion de nombres y apellidos")
# endregion Gestion de archivos y ubicaciones
logging.info("Creando DataFrame con datos de estudiantes")
#region Generar datos filas.
df = pd.DataFrame(columns=['Nombre', 'Semestre', 'Edad', 'Fecha'])
for i in tqdm.trange(1000):
    vector = []
    nombre = GenerarNombre(Nombres, Apellidos).upper()
    semestre = GenerearSemestre()
    edad = GenerarEdad()
    fecha = datetime.date.today().strftime('%Y-%m-%d')
    vector = [nombre, semestre, edad, fecha]
    df.loc[len(df)] = vector
#endregion Generar datos filas.
logging.info("Exportando a Excel")
excel = 'Estudiantes.xlsx'
RutaExcel = os.path.join(DirectorioActual, excel)
df.to_excel(RutaExcel, index=False)
logging.info("Finalizado el proceso")
print(f"El archivo {excel} ha sido creado en la carpeta {DirectorioActual}")
print('FIN DEL PROCESO')
print('*'*100)
