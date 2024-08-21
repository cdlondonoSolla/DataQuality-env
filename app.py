import subprocess


#Ejecutar aplicacion runVbs.py
print("Ejecutando runVbs.py...")
resultado_app = subprocess.run(['python', 'runVbs.py'], capture_output=True, text=True)

if resultado_app.returncode == 0:
    print("runVbs.py ejecutado exitosamente")
else:
    print("Error al ejecutar runVbs.py: ")
    print(resultado_app.stderr)




from closeExcel import cerrar_excel
cerrar_excel()

import time
time.sleep(2)


# Importar funciones de otros archivos
from fileConverter import convertirArchivo


'''Ejecuta Funciones de fileConverter'''

#Ruta de la carpeta con archivos xlsx
carpeta_xlsx = "data/Raw"

#Ruta de la carpeta para guardar csv 
carpeta_csv = "data/temp/"

# Llamar a la función
convertirArchivo(carpeta_xlsx, carpeta_csv)


# Eliminar rutas
from eliminate import eliminar_directorio

eliminar_directorio('data/raw/')

