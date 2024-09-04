import os
import pandas as pd
from .path import folder_paths

path = folder_paths()

path.ruta_temp
path.ruta_general_tables
path.ruta_raw


def convertirArchivo():
    
    path = folder_paths()

    #Crear la carpeta de salida si no existe
    if not os.path.exists(path.ruta_temp):
        os.makedirs(path.ruta_temp)

    # Crear la carpeta de salida si no existe
    if not os.path.exists(path.ruta_temp):
        os.makedirs(path.ruta_temp)

    # Recorrer todos los archivos en la carpeta de entrada
    for archivo in os.listdir(path.ruta_raw):
        if archivo.endswith('.xlsx'):
            # Ruta completa del archivo .xlsx
            ruta_xlsx = os.path.join(path.ruta_raw, archivo)
            
            try:
                # Leer la pestaña específica del archivo .xlsx
                df = pd.read_excel(ruta_xlsx, engine='openpyxl')

                # Limpiar espacios en blanco al final de las cadenas en todas las columnas
                for col in df.select_dtypes(include='object').columns:
                    df[col] = df[col].astype(str).str.strip()
                
                
                # Generar el nombre del archivo .csv
                nombre_csv = os.path.splitext(archivo)[0] +'.csv'
                ruta_csv = os.path.join(path.ruta_temp, nombre_csv)
                
                # Guardar el DataFrame como archivo .csv
                df.to_csv(ruta_csv, index=False)
                
                print(f"Convertido archivo: de {archivo} a {nombre_csv}")
            
            except ValueError as e:
                print(f"Error: {e}. No se encontró el archivo {archivo}")

    print("Conversión completada para todos los archivos .xlsx en la carpeta.")
    

convertirArchivo()
