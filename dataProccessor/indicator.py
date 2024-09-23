import pandas as pd
from .path import folder_paths

path = folder_paths()

path.ruta_temp
path.ruta_raw
path.ruta_final


def client_indicator():
    
    path = folder_paths()
    
    # Clients
    
    # Capturar la cantidad de errores encontrados en data
    result_kna1 = f'{path.ruta_process}result_kna1.csv'
    df_kna1_error = pd.read_csv(result_kna1)
    df_kna1_error['result'] = df_kna1_error['tratamiento_x_claseImpto'] | df_kna1_error['tratamiento_x_nif'] | df_kna1_error['tratamiento_x_medMag'] | df_kna1_error['error_nif5'] | df_kna1_error['error_telefono'] | df_kna1_error['error_telefono_vacio'] | df_kna1_error['error_calle'] | df_kna1_error['error_personaFisica']
    client_error_total = df_kna1_error['result'].sum()
    
    # Capturar la cantidad de registros creados o modificados en el periodo
    client_count = f'{path.ruta_final}count.csv'
    df_client_count = pd.read_csv(client_count)
    id_buscado = 1
    client_count_total = df_client_count[df_client_count['id'] == id_buscado]['total'].values[0]
    client_correct_total = client_count_total - client_error_total
    client_indicator = (client_error_total/client_count_total)
    client_indicator = f'{client_indicator:.6f}'
    
    
    
    # Providers
    
    # Capturar la cantidad de errores encontrados en data
    result_lfa1 = f'{path.ruta_process}result_lfa1.csv'
    df_lfa1_error = pd.read_csv(result_lfa1)
    df_lfa1_error['result'] = df_lfa1_error['tratamiento_x_claseImpto'] | df_lfa1_error['tratamiento_x_nif'] | df_lfa1_error['tratamiento_x_medMag'] | df_lfa1_error['error_nif5'] | df_lfa1_error['error_telefono'] | df_lfa1_error['error_telefono_vacio'] | df_lfa1_error['error_calle'] | df_lfa1_error['error_personaFisica']
    provider_error_total = df_lfa1_error['result'].sum()
    
    # Capturar la cantidad de registros creados o modificados en el periodo
    provider_count = f'{path.ruta_final}count.csv'
    df_provider_count = pd.read_csv(provider_count)
    id_buscado = 1
    provider_count_total = df_provider_count[df_provider_count['id'] == id_buscado]['total'].values[0]
    provider_correct_total = provider_count_total - provider_error_total
    provider_indicator = (provider_error_total/provider_count_total)
    provider_indicator = f'{provider_indicator:.6f}'

    
    df_client_indicator = {
        'id': [1, 2],
        'master': ['client', 'provider'],
        'correct': [client_correct_total, provider_correct_total],
        'error': [client_error_total, provider_error_total],
        'total': [client_count_total, provider_count_total],
        'indicator': [client_indicator, provider_indicator]
    }

    df_client_indicator = pd.DataFrame(df_client_indicator)
    df_client_indicator.to_csv(f'{path.ruta_final}/client_indicator.csv', index=False)
    

# Llamar a la función
client_indicator ()