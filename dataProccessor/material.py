import pandas as pd
import numpy as np
from .path import folder_paths
import re

def material_procesor():
    
    path = folder_paths()
    
    """
        Para el manejo de este archivo se define como regla general

            error = true
            ok = false

        Siempre que las validaciones arrojen True significa que hay datos sin calidad.
    """
    
    ruta_csv = f'{path.ruta_temp}mara.csv'
    
    mara = pd.read_csv(
        ruta_csv,
        sep=',',
        header=0
    )
    
    cond1 = mara['Texto breve de material']

    cond1 = cond1.fillna('').astype(str)

    def contains_hyphen(text):
        #definir los caracteres especiales que se consideran como error en la direccion
        patron = r'[Ã³]'
        return bool(re.search(patron, text))

    # Aplicar la función a cada elemento de la serie
    mara['error_nombre'] = cond1.apply(contains_hyphen)

    # Seleccionar columnas específicas
    vista = ['Material','error_nombre']

    result_mara = mara[vista]

    result_mara.to_csv(f'{path.ruta_process}/result_mara.csv', index=False)

    
    return()

def material_count_error():
    
    path = folder_paths()
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_process}result_mara.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_mara_error = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Cliente': str})
    
    error_nombre = df_mara_error['error_nombre'].sum()
    
    
    
    conteo_registros = {
    'id': [1],
    'Campo': ['Nombre Material'],
    'conteo': [error_nombre],
    'Descripcion': ['Materiales con caracteres especiales en el nombre']
    }
    
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv(f'{path.ruta_process}/mara_count.csv', index=False)
    conteo_registros.to_csv(f'{path.ruta_final}/mara_count.csv', index=False)


def material():
    material_procesor()
    material_count_error()

