# Importar funciones de otros archivos
from dataProccessor.fileConverter import convertirArchivo
from dataProccessor.client import client_processor
from dataProccessor.client import client_count_error
from dataProccessor.count import count_processor
from dataProccessor.eliminate import eliminar_directorio
from dataProccessor.eliminate import crear_carpeta
from dataProccessor.indicator import client_indicator
from dataProccessor.path import folder_paths
from dataProccessor.client import client
from dataProccessor.provider import provider
from dataProccessor.historic import historic

path = folder_paths()


#convertirArchivo()

client()
provider()
count_processor()
client_indicator()
historic()



# Eliminar rutas
#eliminar_directorio('D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/temp/')

# Ejemplo de uso
#crear_carpeta("D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/temp")


print('Proceso Terminado')