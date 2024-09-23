import pandas as pd
import numpy as np
from datetime import datetime
from path import folder_paths
import os



def historic():
    
    path = folder_paths()

    id_maestro = [1, 2, 3]
    name_maestro = ['cliente', 'proveedor', 'material']


    now = datetime.now()
    month = now.month
    year = now.year
    month_name = now.strftime('%B')
    full_date = f'{month_name}_{str(year)}'

    ruta_count = f'{path.ruta_final}count.csv'

    df_count = pd.read_csv(ruta_count)

    i = 0

    for id in id_maestro:
        # Ejemplo de DataFrames
        data = {
            'id': [],
            'maestro': [],
            'creacion': [],
            'actualizacion': [],
            'error': [],
            'total':[],
            'system': [],
            'user': [],
            'date': []
        }

        df_historic = pd.DataFrame(data)

        df_historic = pd.concat([df_historic, df_count], ignore_index=True)
        df_historic['date'] = full_date
        # ID que quieres buscar
        id_buscado = id

        # Seleccionar la fila con el ID específico
        fila = df_historic.loc[df_historic['id'] == id_buscado]

        df_final = pd.DataFrame(data)


        df_final = pd.concat([df_final, fila], ignore_index=True)

        df_final['id'] = df_final['id'].astype(int)
        df_final['creacion'] = df_final['creacion'].astype(int)
        df_final['actualizacion'] = df_final['actualizacion'].astype(int)
        df_final['error'] = df_final['error'].astype(int)
        df_final['total'] = df_final['total'].astype(int)
        df_final['system'] = df_final['system'].astype(int)
        df_final['user'] = df_final['user'].astype(int)
        
        # Ruta del archivo CSV
        ruta_csv = f'{path.ruta_historic}historic_{name_maestro[i]}.csv'

        # Verificar si el archivo existe
        if os.path.exists(ruta_csv):
            # Cargar el CSV en un DataFrame
            df_final_concat = pd.read_csv(ruta_csv)
        else:
            df_final_concat = pd.DataFrame(data)
        
        
        df_final_concat = pd.concat([df_final_concat, df_final], ignore_index=True)


        df_final_concat.to_csv(f'{path.ruta_historic}historic_{name_maestro[i]}.csv', index=False)
        
        i = i + 1
    

historic()