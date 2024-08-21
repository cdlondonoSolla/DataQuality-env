import os

def eliminar_archivo(ruta_archivo):
    """
    Elimina un archivo en la ruta especificada.

    Parámetros:
    ruta_archivo (str): Ruta completa al archivo que se desea eliminar.
    """
    try:
        # Verificar si el archivo existe
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
            print(f"Archivo '{ruta_archivo}' eliminado correctamente.")
        else:
            print(f"El archivo '{ruta_archivo}' no existe.")
    except Exception as e:
        print(f"Ocurrió un error al intentar eliminar el archivo: {e}")



def eliminar_directorio(ruta_directorio):
    """
    Elimina un directorio y todo su contenido en la ruta especificada.

    Parámetros:
    ruta_directorio (str): Ruta completa al directorio que se desea eliminar.
    """
    try:
        # Verificar si el directorio existe
        if os.path.isdir(ruta_directorio):
            # Eliminar todos los archivos y subdirectorios dentro del directorio
            for root, dirs, files in os.walk(ruta_directorio, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            # Finalmente eliminar el directorio vacío
            os.rmdir(ruta_directorio)
            print(f"Directorio '{ruta_directorio}' eliminado correctamente.")
        else:
            print(f"El directorio '{ruta_directorio}' no existe.")
    except Exception as e:
        print(f"Ocurrió un error al intentar eliminar el directorio: {e}")


# # Eliminar archivos restantes
# eliminar_archivo('Data/Converted/material.csv')
# eliminar_archivo('Data/Converted/cliente.csv')


