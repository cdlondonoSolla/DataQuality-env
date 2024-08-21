import os
import pandas as pd

def convertirArchivo(carpeta_xlsx, carpeta_csv):

    #Crear la carpeta de salida si no existe
    if not os.path.exists(carpeta_csv):
        os.makedirs(carpeta_csv)

    # Crear la carpeta de salida si no existe
    if not os.path.exists(carpeta_csv):
        os.makedirs(carpeta_csv)

    # Recorrer todos los archivos en la carpeta de entrada
    for archivo in os.listdir(carpeta_xlsx):
        if archivo.endswith('.xlsx'):
            # Ruta completa del archivo .xlsx
            ruta_xlsx = os.path.join(carpeta_xlsx, archivo)
            
            try:
                # Leer la pestaña específica del archivo .xlsx
                df = pd.read_excel(ruta_xlsx, engine='openpyxl')

                # Limpiar espacios en blanco al final de las cadenas en todas las columnas
                for col in df.select_dtypes(include='object').columns:
                    df[col] = df[col].astype(str).str.strip()
                
                
                # Generar el nombre del archivo .csv
                nombre_csv = os.path.splitext(archivo)[0] +'.csv'
                ruta_csv = os.path.join(carpeta_csv, nombre_csv)
                
                # Guardar el DataFrame como archivo .csv
                df.to_csv(ruta_csv, index=False)
                
                print(f"Convertido archivo: de {archivo} a {nombre_csv}")
            
            except ValueError as e:
                print(f"Error: {e}. No se encontró el archivo {archivo}")

    print("Conversión completada para todos los archivos .xlsx en la carpeta.")
    
    
#Ruta de la carpeta con archivos xlsx
carpeta_xlsx = "data/Raw"

#Ruta de la carpeta para guardar csv 
carpeta_csv = "data/temp/"

# Llamar a la función
convertirArchivo(carpeta_xlsx, carpeta_csv)

