import pandas as pd


def tempProcessor():
    ruta_kna1 = 'data/temp/kna1.csv'
    df_kna1 = pd.read_csv(ruta_kna1)

    ruta_lfa1 = 'data/temp/lfa1.csv'
    df_lfa1 = pd.read_csv(ruta_lfa1)

    ruta_mara = 'data/temp/mara.csv'
    df_mara = pd.read_csv(ruta_mara)
    
    conteo_Cliente = df_kna1['Cliente'].count()
    conteo_Acreedor = df_lfa1['Acreedor'].count()
    conteo_Material = df_mara['Material'].count()
    
    conteo_registros = {
        'id': ['kna1', 'lfa1', 'mara'],
    'maestro': ['conteo_Cliente', 'conteo_Acreedor', 'conteo_Material'],
    'conteo': [conteo_Cliente, conteo_Acreedor, conteo_Material]
       }
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv('data/final/count.csv', index=False)


