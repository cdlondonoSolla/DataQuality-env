# Importar funciones de otros archivos
from fileConverter import convertirArchivo
from eliminate import eliminar_directorio
from tempProcessor import tempProcessor
from fileProcessor import file_processor


'''Ejecuta Funciones de fileConverter'''

#Ruta de la carpeta con archivos xlsx
carpeta_xlsx = "data/Raw"

#Ruta de la carpeta para guardar csv 
carpeta_csv = "data/temp/"

# Llamar a la función
convertirArchivo(carpeta_xlsx, carpeta_csv)

# Llamamos la funcion para procesar archivos temp
tempProcessor()
file_processor()

# Eliminar rutas
#eliminar_directorio('data/raw/')

print('Proceso Terminado')

