# Importar funciones de otros archivos
from dataProccessor.fileConverter import convertirArchivo
from dataProccessor.client import client_processor
from dataProccessor.client import client_count_error
from dataProccessor.count import count_processor
from dataProccessor.eliminate import eliminar_directorio
from dataProccessor.eliminate import crear_carpeta
from dataProccessor.indicator import client_indicator
from dataProccessor.path import folder_paths

path = folder_paths()
'''Ejecuta Funciones de fileConverter'''

#Ruta de la carpeta con archivos xlsx
carpeta_xlsx = "D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/raw/"

#Ruta de la carpeta para guardar csv 
carpeta_csv = "D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/temp/"

# Llamar a la función
convertirArchivo()

# Llamamos la funcion para procesar archivos temp
ruta_temp = 'D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/temp/'
ruta_destino = 'D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/final/'


client_processor()
client_count_error ()
count_processor()
client_indicator ()




# Eliminar rutas
eliminar_directorio('D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/temp/')

# Ejemplo de uso
crear_carpeta("D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/temp")


print('Proceso Terminado')