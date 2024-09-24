# Importar funciones de otros archivos
from dataProccessor.fileConverter import archivo_converter
from dataProccessor.count import count_processor
from dataProccessor.eliminate import eliminar_directorio
from dataProccessor.eliminate import crear_carpeta
from dataProccessor.indicator import client_indicator
from dataProccessor.path import folder_paths
from dataProccessor.client import client
from dataProccessor.provider import provider
from dataProccessor.historic import historic
from dataProccessor.material import material

path = folder_paths()


archivo_converter()


client()
provider()
count_processor()
client_indicator()
material()
historic()



# Eliminar rutas
eliminar_directorio('D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/temp/')

# Ejemplo de uso
crear_carpeta("D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/temp")


print('Proceso Terminado')