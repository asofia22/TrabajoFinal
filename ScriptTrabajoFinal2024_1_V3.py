
#inicio region Importaciones
import os
import random as rnd
import numpy as np 
import pandas as pd
import time
import datetime
import logging
import tqdm 
import warnings 
import platform  # Librería para información del sistema operativo
import getpass  # Librería para obtener el nombre del usuario
from timeit import default_timer as timer  # Para medir el tiempo de ejecución de código
warnings.filterwarnings('ignore') # Ignorar advertencias para evitar que se muestren en la salida
# fin region Importaciones

#########################################################
# Se utilizó el algoritmo del profe como base para ejecutar el trabajo final
##########################################################

# inicio Configuración de logging
usuario = getpass.getuser() # Obtener el nombre del usuario actual
sistema_operativo = platform.system() # Obtener el nombre del sistema operativo
plataforma = platform.platform() # Obtener detalles de la plataforma

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
            start_time = timer() # Registrar el tiempo de inicio
            result = func(*args, **kwargs) # Ejecutar la función decorada
            end_time = timer() # Registrar el tiempo de finalización
            duration = end_time - start_time # Calcular la duración de la ejecución
            logging.info(f"{mensaje}\tDuración: {duration:.6f} segundos") # Registrar la duración en el log
            return result
        return wrapped
    return wrapper

@log_evento("Generar nombre")
def GenerarNombre(Nombres: list, Apellidos: list) -> str:
    Nombre = rnd.choice(Nombres) # Elegir un nombre aleatorio
    Apellido = rnd.choice(Apellidos) # Elegir un apellido aleatorio
    return f'{Nombre} {Apellido}' # Combinar el nombre y el apellido

@log_evento("Generar edad")
def GenerarEdad() -> int:
    r = rnd.random() # Generar un número aleatorio entre 0 y 1
    if r < 0.5:
        return rnd.randint(16, 25) # 50% probabilidad de edad entre 16 y 25
    elif r < 0.75:
        return rnd.randint(26, 33) # 25% probabilidad de edad entre 26 y 33
    elif r < 0.9:
        return rnd.randint(34, 40) # 15% probabilidad de edad entre 34 y 40
    else:
        return rnd.randint(41, 85) # 10% probabilidad de edad entre 41 y 85

@log_evento("Generar semestre")
def GenerearSemestre() -> int:
    r = rnd.random() # Generar un número aleatorio entre 0 y 1
    if r < 0.14:
        return 1 # 14% probabilidad de estar en el semestre 1
    elif r < 0.27:
        return 2 # 13% probabilidad de estar en el semestre 2
    elif r < 0.39:
        return 3 # 12% probabilidad de estar en el semestre 3
    elif r < 0.5:
        return 4 # 11% probabilidad de estar en el semestre 4
    elif r < 0.6:
        return 5 # 10% probabilidad de estar en el semestre 5
    elif r < 0.7:
        return 6 # 10% probabilidad de estar en el semestre 6
    elif r < 0.79:
        return 7 # 9% probabilidad de estar en el semestre 7
    elif r < 0.87:
        return 8 # 8% probabilidad de estar en el semestre 8
    elif r < 0.94:
        return 9 # 7% probabilidad de estar en el semestre 9
    else:
        return 10 # 6% probabilidad de estar en el semestre 10
#FIN region Funciones para generación de estudiantes

# Funciones para la asignación de cursos y generación de archivos
MAX_ESTUDIANTES = 1000 # Número máximo de estudiantes
PROPORCION_SEMESTRES = {
    1: 14, 2: 13, 3: 12, 4: 11, 5: 10,
    6: 10, 7: 9, 8: 8, 9: 7, 10: 6
} # Proporción de estudiantes por semestre
# Máximos de estudiantes por clase según el semestre
MAX_ESTUDIANTES_POR_CLASE = {
    1: 30, 2: 30, 3: 30, 4: 25, 5: 25, 6: 25,
    7: 20, 8: 20, 9: 20, 10: 10
}
# Horas teóricas y prácticas por número de créditos
CREDITOS_A_HTD = {12:0 ,4: 96, 3: 64, 2: 32, 1: 16}
CREDITOS_A_HTI = {12:240,4: 120, 3: 80, 2: 64, 1: 32}

@log_evento("Cargar estudiantes desde archivo Excel")
def cargar_estudiantes(ruta_excel): # Leer el archivo Excel con los estudiantes
    df = pd.read_excel(ruta_excel) # Convertir la columna de nombres a una lista
    estudiantes = df['Nombre'].tolist()
    return estudiantes

@log_evento("Asignar estudiantes a semestres")
def asignar_estudiantes_a_semestres(estudiantes, PROPORCION_SEMESTRES):
    #Asignar estudiantes a semestres según las proporciones definidas
    np.random.shuffle(estudiantes) # Mezclar aleatoriamente la lista de estudiantes
    asignacion = {} # Diccionario para almacenar la asignación
    indice_inicio = 0 # Índice inicial para la asignación
    for semestre, proporcion in PROPORCION_SEMESTRES.items():
        cantidad = int(MAX_ESTUDIANTES * proporcion / 100) # Calcular la cantidad de estudiantes por semestre
        asignacion[semestre] = estudiantes[indice_inicio:indice_inicio+cantidad] # Asignar estudiantes al semestre
        indice_inicio += cantidad # Actualizar el índice de inicio
    return asignacion

@log_evento("Crear código de curso")
def crear_codigo_curso(nombre, semestre, creditos, secuencia):
    return f"{nombre[:3].upper()}{semestre}{creditos}{secuencia:02d}" #Crear un código único para el curso

@log_evento("Calcular HTD")
def calcular_htd(creditos):
    return CREDITOS_A_HTD[creditos] #Calcular las horas teóricas directas (HTD) basado en los créditos

@log_evento("Calcular HTI")
def calcular_hti(creditos):
    return CREDITOS_A_HTI[creditos] #Calcular las horas teóricas indirectas (HTI) basado en los créditos

@log_evento("Generar archivos de cursos")
def generar_archivos_cursos(semestre, cursos, asignacion_estudiantes, max_estudiantes_por_clase):
    #Generar archivos Excel y CSV para cada curso, con los estudiantes asignados
    base_dir = 'CarpetaArchivosTrabajoFinal' # Directorio base para los archivos
    if not os.path.exists(base_dir):
        os.mkdir(base_dir) # Crear el directorio base si no existe
    
    for curso in cursos:
        curso_dir = os.path.join(base_dir, f"Semestre_{semestre}", curso['nombre'].replace(' ', '_'))
        if not os.path.exists(curso_dir):
            os.makedirs(curso_dir) # Crear directorio del curso si no existe
        
        estudiantes = asignacion_estudiantes[semestre]
        total_estudiantes = len(estudiantes)
        max_estudiantes_por_clase = MAX_ESTUDIANTES_POR_CLASE[semestre] # Calcular el número de estudiantes por semestre
        secuencia_curso = 1
        
        # Calcular el número total de grupos
        tca = total_estudiantes // max_estudiantes_por_clase
        if total_estudiantes % max_estudiantes_por_clase != 0:
            tca += 1
            
        # Calcular el número de estudiantes por clase
        for i in range(0, total_estudiantes, max_estudiantes_por_clase):
            grupo_estudiantes = estudiantes[i:i+max_estudiantes_por_clase]
            if not grupo_estudiantes:
                break
            # Crea un código único para el curso siguiendo la sugerencia del profesor
            codigo_curso = crear_codigo_curso(curso['nombre'], semestre, curso['creditos'], secuencia_curso)
            htd = calcular_htd(curso['creditos']) # Calcular las horas teóricas directas (HTD)
            hti = calcular_hti(curso['creditos']) # Calcular las horas teóricas indirectas (HTI)
            
            #genera los datos para el archivo Excel
            datos = {
                'CA': codigo_curso,
                'HTD': htd,
                'HTI': hti,
                'NTE': len(grupo_estudiantes),
                'CC': secuencia_curso,
                'TCA': tca,
                'FC': datetime.datetime.now().strftime("%Y%m%d")
            }
            
            # Crea un DataFrame con los datos de los estudiantes
            df = pd.DataFrame(grupo_estudiantes, columns=['Estudiante'])
            for key, value in datos.items():
                df[key] = value
                
            #guarda el archivo Excel
            ruta_excel = os.path.join(curso_dir, f"{codigo_curso}-{curso['nombre'].replace(' ', '')}-{len(grupo_estudiantes)}-{secuencia_curso}.xlsx")
            df.to_excel(ruta_excel, index=False)
            #guarda el archivo CSV
            ruta_csv = os.path.join(curso_dir, f"{codigo_curso}-{curso['nombre'].replace(' ', '')}-{len(grupo_estudiantes)}-{secuencia_curso}.csv")
            df.to_csv(ruta_csv, index=False)
            
            logging.info(f"Archivos generados para el curso {curso['nombre']} en el semestre {semestre}, grupo {secuencia_curso}")
            
            secuencia_curso += 1
            
@log_evento("Generar estudiantes")
def generar_estudiantes():
    #Generar el archivo Excel con estudiantes y asignarlos a cursos
    print('*'*100)
    print(f'{"Inicio del proceso":>15}')
    inicio = time.time() # Tiempo de inicio del proceso
    hoy = datetime.date.today().strftime('%Y%m%d') # Fecha de ejecución
    nombre_archivo_log = f"log_{hoy}.log" # Nombre del archivo de log
    logging.basicConfig(filename=nombre_archivo_log, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') # Configuración del log echa por el profesor
    logging.info("Iniciando el proceso, por NAS PROGRAMMING 😃😃😃👀✔") #no la toque pero si quieren la quitan 
    
    DirectorioActual = os.getcwd() # Directorio actual de trabajo
    textemp = f'El directorio actual de trabajo es: \n\t--> {DirectorioActual}, \nEsta carpeta contendrá los archivos del trabajo final'
    print(textemp) # Imprimir la ruta del directorio actual
    logging.info(textemp)
    
    CarpetaNueva = "CarpetaArchivosTrabajoFinal" # Carpeta para almacenar los resultados
    os.makedirs(CarpetaNueva, exist_ok=True) # Crear la carpeta si no existe
    logging.info("Se crea el directorio {}".format(CarpetaNueva)) # Log de creación de la carpeta
    print(f"'{CarpetaNueva}' La carpeeta ha sido creada.")
    
    carpeta = os.path.join(DirectorioActual, "CarpetaArchivosTrabajoFinal") 
    logging.info("La ruta de trabajo será {}".format(carpeta))
    RutaNombres = r'NombresArgentina.csv' # Ruta del archivo con nombres
    RutaApellidos = r'ApellidosArgentina.csv' # Ruta del archivo con apellidos
    RutaNombres = os.path.join(DirectorioActual, RutaNombres) # Ruta completa del archivo con nombres
    RutaApellidos = os.path.join(DirectorioActual, RutaApellidos) # Ruta completa del archivo con apellidos
    logging.info("Cargando CSV con nombres")
    dfNombres = pd.read_csv(RutaNombres, encoding='ISO-8859-1') # Cargar el archivo CSV con nombres
    Nombres = dfNombres['name'].tolist() # Convertir la columna de nombres a una lista
    logging.info("Reemplazando nombres y detalles del documento")
    for i in tqdm.trange(len(Nombres)): # Reemplazar espacios en los nombres
        if ' ' in Nombres[i]: 
            Nombres[i] = Nombres[i].replace(' ', '_') # Reemplazar espacios por guiones bajos
    logging.info("Cargando CSV con apellidos")
    dfApellidos = pd.read_csv(RutaApellidos, encoding='ISO-8859-1') # Cargar el archivo CSV con apellidos
    Apellidos = dfApellidos['lastname'].tolist() # Convertir la columna de apellidos a una lista
    logging.info("Reemplazando apellidos y detalles del documento")
    for i in tqdm.trange(len(Apellidos)): # Reemplazar espacios en los apellidos
        if ' ' in Apellidos[i]:
            Apellidos[i] = Apellidos[i].replace(' ', '_') # Reemplazar espacios por guiones bajos
    logging.info("Finalizado proceso de gestion de nombres y apellidos")
    
    logging.info("Creando DataFrame con datos de estudiantes")
    df = pd.DataFrame(columns=['Nombre', 'Semestre', 'Edad', 'Fecha']) # Crear un DataFrame para los datos de los estudiantes
    for i in tqdm.trange(1000):
        vector = [] # Vector para almacenar los datos de cada estudiante
        nombre = GenerarNombre(Nombres, Apellidos).upper() # Generar un nombre aleatorio
        semestre = GenerearSemestre() # Generar un semestre aleatorio
        edad = GenerarEdad() # Generar una edad aleatoria
        fecha = datetime.date.today().strftime('%Y-%m-%d') # Fecha actual
        vector = [nombre, semestre, edad, fecha] # Agregar los datos al vector
        df.loc[len(df)] = vector # Agregar el vector al DataFrame
    
    logging.info("Exportando a Excel")
    excel = 'Estudiantes.xlsx' #exporta el archivo Excel
    RutaExcel = os.path.join(DirectorioActual, excel) # Ruta completa del archivo Excel
    df.to_excel(RutaExcel, index=False) # Exportar el DataFrame a un archivo Excel
    logging.info("Finalizado el proceso")
    print(f"El archivo {excel} ha sido creado en la carpeta {DirectorioActual}")

def main():
    # Generar archivo de estudiantes
    generar_estudiantes()
    
    # Ruta del archivo Excel con los estudiantes
    ruta_excel = 'Estudiantes.xlsx'
    
    # Cargar estudiantes
    estudiantes = cargar_estudiantes(ruta_excel)
    
    # Asignar estudiantes a semestres
    asignacion_estudiantes = asignar_estudiantes_a_semestres(estudiantes, PROPORCION_SEMESTRES)
    
    # Definición de cursos por semestre
    cursos_por_semestre = {
        #primer semestre
        1: [{'nombre': 'Álgebra y Trigonometría', 'creditos': 3}, 
            {'nombre': 'Cálculo Diferencial', 'creditos': 3},
            {'nombre': 'Geometría Vectorial y Analítica', 'creditos': 3},
            {'nombre': 'Vivamos la Universidad', 'creditos': 1},
            {'nombre': 'Inglés I', 'creditos': 1},
            {'nombre': 'Lectoescritura', 'creditos': 3},
            {'nombre': 'Introducción a la Ingeniería Industrial', 'creditos': 1}],
        #segundo semestre
        2: [{'nombre': 'Gestión de las Organizaciones', 'creditos': 3}, 
            {'nombre': 'Habilidades Gerenciales', 'creditos': 3},
            {'nombre': 'Álgebra Lineal', 'creditos': 3},
            {'nombre': 'Cálculo Integral', 'creditos': 3},
            {'nombre': 'Descubriendo la Física', 'creditos': 3},
            {'nombre': 'Inglés II', 'creditos': 1}],
        #tercer semestre
        3: [{'nombre': 'Gestión Contable', 'creditos': 3}, 
            {'nombre': 'Física Mecánica', 'creditos': 3},
            {'nombre': 'Inglés III', 'creditos': 1},
            {'nombre': 'Algoritmia y Programación', 'creditos': 3},
            {'nombre': 'Probabilidad e Inferencia Estadística', 'creditos': 3},
            {'nombre': 'Teoría General de Sistemas', 'creditos': 3}],
        #cuarto semestre
        4:[{'nombre': 'Ingeniería Económicas', 'creditos': 3}, 
            {'nombre': 'Electiva en Física', 'creditos': 3},
            {'nombre': 'Inglés IV', 'creditos': 1},
            {'nombre': 'Diseño de Experimentos y Análisis de Regresión', 'creditos': 3},
            {'nombre': 'Optimización', 'creditos': 3},
            {'nombre': 'Gestión de Métodos y Tiempos', 'creditos': 4}],
        #quinto semestre
        5:[{'nombre': 'Gestión Financiera', 'creditos': 3}, 
            {'nombre': 'Laboratorio Integrado de Física', 'creditos': 1},
            {'nombre': 'Inglés V', 'creditos': 1},
            {'nombre': 'Formación Ciudadana y Constitucional', 'creditos': 1},
            {'nombre': 'Dinámica de Sistemas', 'creditos': 3},
            {'nombre': 'Muestreo y Series de Tiempo', 'creditos': 3},
            {'nombre': 'Procesos Estocásticos y Análisis de Decisión', 'creditos': 3},
            {'nombre': 'Gestión por Procesos', 'creditos': 3}],
        #sexto semestre
        6:[{'nombre': 'Gestión Tecnológica', 'creditos': 3}, 
            {'nombre': 'Legislación', 'creditos': 3},
            {'nombre': 'Electiva en Humanidades I', 'creditos': 3},
            {'nombre': 'Inglés VI', 'creditos': 1},
            {'nombre': 'Simulación Discreta', 'creditos': 3},
            {'nombre': 'Formulación de Proyectos de Investigación', 'creditos': 3},
            {'nombre': 'Normalización y Control de la Calidad', 'creditos': 3}],
        #septimo semestre
        7:[{'nombre': 'Formulación y Evaluación de Proyectos de Inversión', 'creditos': 3}, 
            {'nombre': 'Emprendimiento', 'creditos': 2},
            {'nombre': 'Electiva en Humanidades II', 'creditos': 3},
            {'nombre': 'Énfasis Profesional I', 'creditos': 3},
            {'nombre': 'Electiva Complementaria I', 'creditos': 3},
            {'nombre': 'Diseño de Sistemas Productivos', 'creditos': 3}],
        #octavo semestre
        8:[{'nombre': 'Gestión de Proyectos', 'creditos': 3}, 
            {'nombre': 'Electiva en Humanidades III', 'creditos': 3},
            {'nombre': 'Énfasis Profesional II', 'creditos': 3},
            {'nombre': 'Electiva Complementaria II', 'creditos': 3},
            {'nombre': 'Administración de la Producción y del Servicio', 'creditos': 3}],
        #noveno semestre
        9:[{'nombre': 'Electiva en Humanidades IV', 'creditos': 3}, 
            {'nombre': 'Énfasis Profesional III', 'creditos': 3},
            {'nombre': 'Electiva Complementaria III', 'creditos': 3},
            {'nombre': 'Gestión de la Cadena de Abastecimiento', 'creditos': 3},
            {'nombre': 'Ingeniería del Mejoramiento Continuo', 'creditos': 3}],
        #decimo semestre
        10:[{'nombre': 'Práctica Profesional', 'creditos': 12},]
    }
    
    # Generar archivos de cursos para cada semestre
    for semestre, cursos in cursos_por_semestre.items():
        generar_archivos_cursos(semestre, cursos, asignacion_estudiantes, MAX_ESTUDIANTES)
    # region Fin del proceso
    fin = time.time()
    print(f'{"Fin del proceso. ":>15} {fin :.2f} segundos')
    logging.info(f"Fin del proceso. {fin :.2f} segundos")
    print('*'*100)
    
if __name__ == "__main__": # Ejecutar la función principal
    main()
