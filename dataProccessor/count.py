import pandas as pd
import numpy as np
from .path import folder_paths
from .client import sys_user_crea as cli
from .provider import sys_user_crea as prov


path = folder_paths()

path.ruta_temp
path.ruta_raw
path.ruta_final


def count_processor():

    path = folder_paths()
    
    # General Data
    ruta_kna1 = f'{path.ruta_temp}kna1.csv'
    df_kna1 = pd.read_csv(ruta_kna1)
    conteo_Cliente = df_kna1['Cliente'].count()

    ruta_lfa1 = f'{path.ruta_temp}lfa1.csv'
    df_lfa1 = pd.read_csv(ruta_lfa1)
    conteo_Acreedor = df_lfa1['Acreedor'].count()

    ruta_mara = f'{path.ruta_temp}mara.csv'
    df_mara = pd.read_csv(ruta_mara)
    conteo_Material = df_mara['Material'].count()
    
    ruta_mara2 = f'{path.ruta_temp}mara2.csv'
    df_mara2 = pd.read_csv(ruta_mara2)
    conteo_mara2 = df_mara2['Material'].count()
    
    ruta_knb1 = f'{path.ruta_temp}knb1.csv'
    df_knb1 = pd.read_csv(ruta_knb1)
    conteo_knb1 = df_knb1['Cliente'].count()
    
    ruta_lfb1 = f'{path.ruta_temp}lfb1.csv'
    df_lfb1 = pd.read_csv(ruta_lfb1)
    conteo_lfb1 = df_lfb1['Acreedor'].count()
    
    
    # Client Data Result
    
    result_kna1 = f'{path.ruta_process}result_kna1.csv'
    df_kna1_error = pd.read_csv(result_kna1)
    df_kna1_error['result'] = df_kna1_error['tratamiento_x_claseImpto'] | df_kna1_error['tratamiento_x_nif'] | df_kna1_error['tratamiento_x_medMag'] | df_kna1_error['error_nif5'] | df_kna1_error['error_telefono'] | df_kna1_error['error_telefono_vacio'] | df_kna1_error['error_calle'] | df_kna1_error['error_personaFisica']    
    conteo_kna1_error = df_kna1_error['result'].sum()
    
    cli()
    cli_system_crea, cli_user_crea = cli()
    #Provider Data Result
    
    result_lfa1 = f'{path.ruta_process}result_lfa1.csv'
    df_lfa1_error = pd.read_csv(result_lfa1)
    df_lfa1_error['result'] = df_lfa1_error['tratamiento_x_claseImpto'] | df_lfa1_error['tratamiento_x_nif'] | df_lfa1_error['tratamiento_x_medMag'] | df_lfa1_error['error_nif5'] | df_lfa1_error['error_telefono'] | df_lfa1_error['error_telefono_vacio'] | df_lfa1_error['error_calle'] | df_lfa1_error['error_personaFisica']    
    conteo_lfa1_error = df_lfa1_error['result'].sum()
    
    prov()
    prov_system_crea, prov_user_crea = prov()

    # Material Data Result

    result_mara = f'{path.ruta_process}result_mara.csv'
    df_mara_error = pd.read_csv(result_mara)
    df_mara_error['result'] = df_mara_error['error_nombre']    
    conteo_mara_error = df_mara_error['result'].sum() 
    

    conteo_registros = {
    'id': [1, 2, 3],
    'maestro': ['cliente', 'proveedor', 'material'],
    'creacion': [conteo_Cliente, conteo_Acreedor, conteo_Material],
    'actualizacion': [conteo_knb1, conteo_lfb1, conteo_mara2],
    'error': [conteo_kna1_error, conteo_lfa1_error, conteo_mara_error],
    'total': [conteo_Cliente+ conteo_knb1, conteo_Acreedor + conteo_lfb1, conteo_Material + conteo_mara2],
    'system': [cli_system_crea, prov_system_crea, 0],
    'user': [cli_user_crea, prov_user_crea, conteo_Material]
    }
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv(f'{path.ruta_final}/count.csv', index=False)

# Llamamos la funcion para procesar archivos temp

count_processor()
