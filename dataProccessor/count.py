import pandas as pd
import numpy as np
from .path import folder_paths

path = folder_paths()

path.ruta_temp
path.ruta_raw
path.ruta_final


def count_processor():

    path = folder_paths()
    
    ruta_kna1 = f'{path.ruta_temp}kna1.csv'
    df_kna1 = pd.read_csv(ruta_kna1)
    conteo_Cliente = df_kna1['Cliente'].count()

    ruta_lfa1 = f'{path.ruta_temp}lfa1.csv'
    df_lfa1 = pd.read_csv(ruta_lfa1)
    conteo_Acreedor = df_lfa1['Acreedor'].count()

    ruta_mara = f'{path.ruta_temp}mara.csv'
    df_mara = pd.read_csv(ruta_mara)
    conteo_Material = df_mara['Material'].count()
    
    ruta_knb1 = f'{path.ruta_temp}knb1.csv'
    df_knb1 = pd.read_csv(ruta_knb1)
    conteo_knb1 = df_knb1['Cliente'].count()
    
    ruta_lfb1 = f'{path.ruta_temp}lfb1.csv'
    df_lfb1 = pd.read_csv(ruta_lfb1)
    conteo_lfb1 = df_lfb1['Acreedor'].count()
    
    
    
    
    result_kna1 = f'{path.ruta_final}result_kna1.csv'
    df_kna1_error = pd.read_csv(result_kna1)
    df_kna1_error['result'] = df_kna1_error['tratamiento_x_claseImpto'] | df_kna1_error['tratamiento_x_nif'] | df_kna1_error['tratamiento_x_medMag'] | df_kna1_error['error_nif5'] | df_kna1_error['error_telefono'] | df_kna1_error['error_telefono_vacio'] | df_kna1_error['error_calle'] | df_kna1_error['error_personaFisica']    
    conteo_kna1_error = df_kna1_error['result'].sum()
    
    
    """USER SYSTEM COMPARISON"""
    
    data = {
    'cliente': [],
    'creado_por': []
    }
    
    df_userXsystem = pd.DataFrame(data)
    
    ruta_kna1 = f'{path.ruta_temp}kna1.csv'
    df_kna1 = pd.read_csv(ruta_kna1)
    
    df_userXsystem['cliente'] = df_kna1['Cliente']
    
    # la cantidad de clientes creados automaticamente

    cond1 = df_kna1['Creado por'] == 'USERRFC8'
    cond2 = df_kna1['Grupo de cuentas'] == 'D006'

    df_userXsystem['creado_por'] = np.where(cond1 | cond2,'system','user')
    
    create_system = df_userXsystem['creado_por'].str.contains('system', case=False, na=False)
    create_user = df_userXsystem['creado_por'].str.contains('user', case=False, na=False)
    
    # Aplicar el filtro al DataFrame
    create_system = df_userXsystem[create_system].count()
    create_user = df_userXsystem[create_user].count()
    
    """END"""
    
    system_crea = create_system['creado_por']
    user_crea = create_user['creado_por']
    
    conteo_marc = 0

    conteo_registros = {
    'id': [1, 2, 3],
    'maestro': ['cliente', 'proveedor', 'material'],
    'creacion': [conteo_Cliente, conteo_Acreedor, conteo_Material],
    'actualizacion': [conteo_knb1, conteo_lfb1, 0],
    'error': [conteo_kna1_error, 0, 0],
    'total': [conteo_Cliente+ conteo_knb1, conteo_Acreedor + conteo_lfb1, conteo_Material + conteo_marc],
    'system': [system_crea, 0, 0],
    'user': [user_crea, 0, 0]
    }
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv(f'{path.ruta_final}/count.csv', index=False)

# Llamamos la funcion para procesar archivos temp

count_processor()
