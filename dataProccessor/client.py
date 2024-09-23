import pandas as pd
import numpy as np
import re
from .path import folder_paths


path = folder_paths()

"""
path.ruta_temp
path.ruta_raw
path.ruta_process
"""

def client_processor():
    
    path = folder_paths()
    """
        Para el manejo de este archivo se define como regla general

            error = true
            ok = false

        Siempre que las validaciones arrojen True significa que hay datos sin calidad.
    """

    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_temp}kna1.csv'

    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    kna1 = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Tratamiento': str, 'Número fiscal 5': str, 'Teléfono 1': str},  # Tipos de datos
        na_values=['NA', 'N/A']  # Valores a considerar como NaN
    )


    D001= kna1['Grupo de cuentas'] == 'D001'
    D002= kna1['Grupo de cuentas'] == 'D002'
    D003= kna1['Grupo de cuentas'] == 'D003'
    D004= kna1['Grupo de cuentas'] == 'D004'
    D005= kna1['Grupo de cuentas'] == 'D005'
    D006= kna1['Grupo de cuentas'] == 'D006'
    D007= kna1['Grupo de cuentas'] == 'D007'
    D010= kna1['Grupo de cuentas'] == 'D010'
    D014= kna1['Grupo de cuentas'] == 'D014'
    D018= kna1['Grupo de cuentas'] == 'D018'
    D019= kna1['Grupo de cuentas'] == 'D019'

    kna1['creado_por'] = np.where(D001|D002|D003|D004|D005|D006|D007|D010|D014|D018|D019,
                                  'traer','no_traer')

    kna1 = kna1[kna1['creado_por'] == 'traer']
    
    kna1 = kna1  



    kna1_renamed =  kna1.rename(columns={'Tipo NIF': 'nif'})

    # Ruta al archivo CSV
    #ruta_csv = 'data/generalTabes/nif.csv'
    ruta_csv = f'{path.ruta_general_tables}/nif.csv'

    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    nif = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        
    )


    nif_renamed =  nif.rename(columns={'nif': 'nif'})


    # Realizar el merge
    kna1_renamed = pd.merge(kna1_renamed, nif_renamed, on='nif', how='left')

    # Seleccionar columnas específicas
    validacionNif = ['Cliente','nif', 'descripcion']
    resultado_seleccionado = kna1_renamed[validacionNif]


    kna1_renamed =  kna1_renamed.rename(columns={'Clase de impuesto': 'claseImp'})

    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_general_tables}/claseImpuesto.csv'

    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    impuesto = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
    )


    impuesto_renamed =  impuesto.rename(columns={'clase': 'claseImp'})


    # Realizar el merge
    resultado = pd.merge(kna1_renamed, impuesto_renamed, on='claseImp', how='left')
    resultado['tipoPerona'] = resultado['descripcion impuesto'].str[:2]


    # tratamiento empresa no tenga clase de impuestos pn
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['tipoPerona'] == 'PN'

    resultado['tratamiento_x_claseImpto'] = np.where(cond1 & cond2, True, False)


    # tratamiento empresa no tenga tipo nif <> 31
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['nif'] != 31
    cond3 = resultado['Grupo de cuentas'] == 'D001'

    resultado['tratamiento_x_nif'] = np.where(cond1 & cond2 & cond3,True,False)

    # tratamiento empresa no tenga medios magneticos (nombre1 y nombre2)

    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['Nombre 3'].isnull()
    cond3 = resultado['Nombre 4'].isnull()

    resultado['tratamiento_x_medMag'] = np.where(cond1 & cond2 & cond3,True,False)

    # nif 5 no este vacio

    cond1 = resultado['Número fiscal 5'].isnull()


    resultado['error_nif5'] = np.where(cond1,True,False)

    # los numeros de telefono no tengan guiones (-)

    cond1 = resultado['Teléfono 1']

    cond1 = cond1.fillna('').astype(str)

    def contains_hyphen(text):
        return '-' in text

    # Aplicar la función a cada elemento de la serie
    resultado['error_telefono'] = cond1.apply(contains_hyphen)

    # los numeros de telefono estan vacios

    cond1 = resultado['Teléfono 1'].isnull()


    resultado['error_telefono_vacio'] = np.where(cond1,True,False)

    # las direcciones no tengan caracteres especiales (# - grados N`)

    cond1 = resultado['Calle']

    cond1 = cond1.fillna('').astype(str)

    def contains_hyphen(text):
        #definir los caracteres especiales que se consideran como error en la direccion
        patron = r'[#-]'
        return bool(re.search(patron, text))

    # Aplicar la función a cada elemento de la serie
    resultado['error_calle'] = cond1.apply(contains_hyphen)



    # Cliente tenga Ramo diligenciado
    cond1 = resultado['Ramo'].isnull()

    resultado['ramo_vacio'] = np.where(cond1, True, False)

        
    # Crear una columna 'error_personaFisica' basada en condiciones
    resultado['error_personaFisica'] = False  # Inicializar con un valor por defecto

    # Aplicar condiciones
    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] == 13) & (resultado['Persona física'].isnull()), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] != 13) & (resultado['nif'] == 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] != 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True


    # Seleccionar columnas específicas
    vista = ['Cliente','tratamiento_x_claseImpto', 
            'tratamiento_x_nif', 'tratamiento_x_medMag','error_nif5',
            'error_telefono', 'error_telefono_vacio', 'error_calle', 
            'error_personaFisica', 'ramo_vacio']

    resultado_seleccionado = resultado[vista]

    resultado_seleccionado.to_csv(f'{path.ruta_process}/result_kna1.csv', index=False)
    

def client_count_error ():
    
    path = folder_paths()
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_process}result_kna1.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_kna1_error = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Cliente': str})
    
    tratamiento_x_claseImpto = df_kna1_error['tratamiento_x_claseImpto'].sum()
    
    tratamiento_x_nif = df_kna1_error['tratamiento_x_nif'].sum()
    
    tratamiento_x_medMag = df_kna1_error['tratamiento_x_medMag'].sum()
    
    error_nif5 = df_kna1_error['error_nif5'].sum()
    
    error_telefono = df_kna1_error['error_telefono'].sum() + df_kna1_error['error_telefono_vacio'].sum()
    
    error_calle = df_kna1_error['error_calle'].sum()
    
    error_personaFisica = df_kna1_error['error_personaFisica'].sum()
    
    ramo_vacio = df_kna1_error['ramo_vacio'].sum()
    
    
    conteo_registros = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'Campo': ['Clase impuestos', 'Nif', 'Medios Magneticos', 'Nif 5', 'Telefono', 'Calle (direccion)', 'Persona Fisica', 'Ramo'],
    'conteo': [tratamiento_x_claseImpto, tratamiento_x_nif, tratamiento_x_medMag, error_nif5, error_telefono, error_calle, error_personaFisica, ramo_vacio],
    'Descripcion': ['Empresas que cuentan con clase de impuestos de PN', 'Empresas con tipo de Nif diferente a RUT', 'Empresas con medios magneticos diligenciados', 'Clientes con Nif 5 vacio', 'Clientes con telefono vacio, espacios o guiones', 'Clientes con caracteres especiales en direccion', 'Clientes con check de PF mal diligenciado', 'El campo Ramo (Actividad Economica) se encuentra vacio.']
    }
    
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv(f'{path.ruta_process}/kna1_count.csv', index=False)


def user_filter():
    
    path = folder_paths()
    
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_temp}kna1.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    kna1 = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Tratamiento': str, 'Número fiscal 5': str, 'Teléfono 1': str},  # Tipos de datos
        na_values=['NA', 'N/A']  # Valores a considerar como NaN
    )
    
    D001= kna1['Grupo de cuentas'] == 'D001'
    D002= kna1['Grupo de cuentas'] == 'D002'
    D003= kna1['Grupo de cuentas'] == 'D003'
    D004= kna1['Grupo de cuentas'] == 'D004'
    D005= kna1['Grupo de cuentas'] == 'D005'
    D006= kna1['Grupo de cuentas'] == 'D006'
    D007= kna1['Grupo de cuentas'] == 'D007'
    D010= kna1['Grupo de cuentas'] == 'D010'
    D014= kna1['Grupo de cuentas'] == 'D014'
    D018= kna1['Grupo de cuentas'] == 'D018'
    D019= kna1['Grupo de cuentas'] == 'D019'

    kna1['creado_por'] = np.where(D001|D002|D003|D004|D005|D006|D007|D010|D014|D018|D019,
                                  'traer','no_traer')

    kna1 = kna1[kna1['creado_por'] == 'traer']
    
    kna1 = kna1

    kna1_user = pd.DataFrame(kna1)

    cond1 = kna1['Creado por'] == 'USERRFC8'
    cond2 = kna1['Grupo de cuentas'] == 'D006'

    kna1_user['creado_por'] = np.where(cond1 | cond2,'system','user')

    df_user = kna1_user[kna1_user['creado_por'] == 'user']
    
    kna1 = df_user    

    kna1_renamed =  kna1.rename(columns={'Tipo NIF': 'nif'})

    # Ruta al archivo CSV
    #ruta_csv = 'data/generalTabes/nif.csv'
    ruta_csv = f'{path.ruta_general_tables}/nif.csv'

    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    nif = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        
    )


    nif_renamed =  nif.rename(columns={'nif': 'nif'})


    # Realizar el merge
    kna1_renamed = pd.merge(kna1_renamed, nif_renamed, on='nif', how='left')

    # Seleccionar columnas específicas
    validacionNif = ['Cliente','nif', 'descripcion']
    resultado_seleccionado = kna1_renamed[validacionNif]


    kna1_renamed =  kna1_renamed.rename(columns={'Clase de impuesto': 'claseImp'})

    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_general_tables}/claseImpuesto.csv'

    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    impuesto = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
    )


    impuesto_renamed =  impuesto.rename(columns={'clase': 'claseImp'})


    # Realizar el merge
    resultado = pd.merge(kna1_renamed, impuesto_renamed, on='claseImp', how='left')
    resultado['tipoPerona'] = resultado['descripcion impuesto'].str[:2]


    # tratamiento empresa no tenga clase de impuestos pn
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['tipoPerona'] == 'PN'

    resultado['tratamiento_x_claseImpto'] = np.where(cond1 & cond2, True, False)


    # tratamiento empresa no tenga tipo nif <> 31
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['nif'] != 31
    cond3 = resultado['Grupo de cuentas'] == 'D001'

    resultado['tratamiento_x_nif'] = np.where(cond1 & cond2 & cond3,True,False)

    # tratamiento empresa no tenga medios magneticos (nombre1 y nombre2)

    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['Nombre 3'].isnull()
    cond3 = resultado['Nombre 4'].isnull()

    resultado['tratamiento_x_medMag'] = np.where(cond1 & cond2 & cond3,True,False)

    # nif 5 no este vacio

    cond1 = resultado['Número fiscal 5'].isnull()


    resultado['error_nif5'] = np.where(cond1,True,False)

    # los numeros de telefono no tengan guiones (-)

    cond1 = resultado['Teléfono 1']

    cond1 = cond1.fillna('').astype(str)

    def contains_hyphen(text):
        return '-' in text

    # Aplicar la función a cada elemento de la serie
    resultado['error_telefono'] = cond1.apply(contains_hyphen)

    # los numeros de telefono estan vacios

    cond1 = resultado['Teléfono 1'].isnull()


    resultado['error_telefono_vacio'] = np.where(cond1,True,False)

    # las direcciones no tengan caracteres especiales (# - grados N`)

    cond1 = resultado['Calle']

    cond1 = cond1.fillna('').astype(str)

    def contains_hyphen(text):
        #definir los caracteres especiales que se consideran como error en la direccion
        patron = r'[#-]'
        return bool(re.search(patron, text))

    # Aplicar la función a cada elemento de la serie
    resultado['error_calle'] = cond1.apply(contains_hyphen)



    # Cliente tenga Ramo diligenciado
    cond1 = resultado['Ramo'].isnull()

    resultado['ramo_vacio'] = np.where(cond1, True, False)

        
    # Crear una columna 'error_personaFisica' basada en condiciones
    resultado['error_personaFisica'] = False  # Inicializar con un valor por defecto

    # Aplicar condiciones
    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] == 13) & (resultado['Persona física'].isnull()), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] != 13) & (resultado['nif'] == 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] != 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True


    # Seleccionar columnas específicas
    vista = ['Cliente','tratamiento_x_claseImpto', 
            'tratamiento_x_nif', 'tratamiento_x_medMag','error_nif5',
            'error_telefono', 'error_telefono_vacio', 'error_calle', 
            'error_personaFisica', 'ramo_vacio']

    resultado_seleccionado = resultado[vista]

    resultado_seleccionado.to_csv(f'{path.ruta_process}/result_kna1_user.csv', index=False)
    

def sys_filter():
    
    path = folder_paths()
    
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_temp}kna1.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    kna1 = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Tratamiento': str, 'Número fiscal 5': str, 'Teléfono 1': str},  # Tipos de datos
        na_values=['NA', 'N/A']  # Valores a considerar como NaN
    )
    
    D001= kna1['Grupo de cuentas'] == 'D001'
    D002= kna1['Grupo de cuentas'] == 'D002'
    D003= kna1['Grupo de cuentas'] == 'D003'
    D004= kna1['Grupo de cuentas'] == 'D004'
    D005= kna1['Grupo de cuentas'] == 'D005'
    D006= kna1['Grupo de cuentas'] == 'D006'
    D007= kna1['Grupo de cuentas'] == 'D007'
    D010= kna1['Grupo de cuentas'] == 'D010'
    D014= kna1['Grupo de cuentas'] == 'D014'
    D018= kna1['Grupo de cuentas'] == 'D018'
    D019= kna1['Grupo de cuentas'] == 'D019'

    kna1['creado_por'] = np.where(D001|D002|D003|D004|D005|D006|D007|D010|D014|D018|D019,
                                  'traer','no_traer')

    kna1 = kna1[kna1['creado_por'] == 'traer']
    
    kna1 = kna1  

    kna1_user = pd.DataFrame(kna1)

    cond1 = kna1['Creado por'] == 'USERRFC8'
    cond2 = kna1['Grupo de cuentas'] == 'D006'

    kna1_user['creado_por'] = np.where(cond1 | cond2,'system','user')

    df_user = kna1_user[kna1_user['creado_por'] == 'system']
    
    kna1 = df_user    

    kna1_renamed =  kna1.rename(columns={'Tipo NIF': 'nif'})

    # Ruta al archivo CSV
    #ruta_csv = 'data/generalTabes/nif.csv'
    ruta_csv = f'{path.ruta_general_tables}/nif.csv'

    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    nif = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        
    )


    nif_renamed =  nif.rename(columns={'nif': 'nif'})


    # Realizar el merge
    kna1_renamed = pd.merge(kna1_renamed, nif_renamed, on='nif', how='left')

    # Seleccionar columnas específicas
    validacionNif = ['Cliente','nif', 'descripcion']
    resultado_seleccionado = kna1_renamed[validacionNif]


    kna1_renamed =  kna1_renamed.rename(columns={'Clase de impuesto': 'claseImp'})

    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_general_tables}/claseImpuesto.csv'

    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    impuesto = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
    )


    impuesto_renamed =  impuesto.rename(columns={'clase': 'claseImp'})


    # Realizar el merge
    resultado = pd.merge(kna1_renamed, impuesto_renamed, on='claseImp', how='left')
    resultado['tipoPerona'] = resultado['descripcion impuesto'].str[:2]


    # tratamiento empresa no tenga clase de impuestos pn
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['tipoPerona'] == 'PN'

    resultado['tratamiento_x_claseImpto'] = np.where(cond1 & cond2, True, False)


    # tratamiento empresa no tenga tipo nif <> 31
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['nif'] != 31
    cond3 = resultado['Grupo de cuentas'] == 'D001'

    resultado['tratamiento_x_nif'] = np.where(cond1 & cond2 & cond3,True,False)

    # tratamiento empresa no tenga medios magneticos (nombre1 y nombre2)

    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['Nombre 3'].isnull()
    cond3 = resultado['Nombre 4'].isnull()

    resultado['tratamiento_x_medMag'] = np.where(cond1 & cond2 & cond3,True,False)

    # nif 5 no este vacio

    cond1 = resultado['Número fiscal 5'].isnull()


    resultado['error_nif5'] = np.where(cond1,True,False)

    # los numeros de telefono no tengan guiones (-)

    cond1 = resultado['Teléfono 1']

    cond1 = cond1.fillna('').astype(str)

    def contains_hyphen(text):
        return '-' in text

    # Aplicar la función a cada elemento de la serie
    resultado['error_telefono'] = cond1.apply(contains_hyphen)

    # los numeros de telefono estan vacios

    cond1 = resultado['Teléfono 1'].isnull()


    resultado['error_telefono_vacio'] = np.where(cond1,True,False)

    # las direcciones no tengan caracteres especiales (# - grados N`)

    cond1 = resultado['Calle']

    cond1 = cond1.fillna('').astype(str)

    def contains_hyphen(text):
        #definir los caracteres especiales que se consideran como error en la direccion
        patron = r'[#-]'
        return bool(re.search(patron, text))

    # Aplicar la función a cada elemento de la serie
    resultado['error_calle'] = cond1.apply(contains_hyphen)



    # Cliente tenga Ramo diligenciado
    cond1 = resultado['Ramo'].isnull()

    resultado['ramo_vacio'] = np.where(cond1, True, False)

        
    # Crear una columna 'error_personaFisica' basada en condiciones
    resultado['error_personaFisica'] = False  # Inicializar con un valor por defecto

    # Aplicar condiciones
    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] == 13) & (resultado['Persona física'].isnull()), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] != 13) & (resultado['nif'] == 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] != 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True


    # Seleccionar columnas específicas
    vista = ['Cliente','tratamiento_x_claseImpto', 
            'tratamiento_x_nif', 'tratamiento_x_medMag','error_nif5',
            'error_telefono', 'error_telefono_vacio', 'error_calle', 
            'error_personaFisica', 'ramo_vacio']

    resultado_seleccionado = resultado[vista]

    resultado_seleccionado.to_csv(f'{path.ruta_process}/result_kna1_system.csv', index=False)

    
def client_count_error_system():
    
    
    path = folder_paths()
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_process}result_kna1_system.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_kna1_error = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Cliente': str})
    
    tratamiento_x_claseImpto = df_kna1_error['tratamiento_x_claseImpto'].sum()
    
    tratamiento_x_nif = df_kna1_error['tratamiento_x_nif'].sum()
    
    tratamiento_x_medMag = df_kna1_error['tratamiento_x_medMag'].sum()
    
    error_nif5 = df_kna1_error['error_nif5'].sum()
    
    error_telefono = df_kna1_error['error_telefono'].sum() + df_kna1_error['error_telefono_vacio'].sum()
    
    error_calle = df_kna1_error['error_calle'].sum()
    
    error_personaFisica = df_kna1_error['error_personaFisica'].sum()
    
    ramo_vacio = df_kna1_error['ramo_vacio'].sum()
    
    
    conteo_registros = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'Campo': ['Clase impuestos', 'Nif', 'Medios Magneticos', 'Nif 5', 'Telefono', 'Calle (direccion)', 'Persona Fisica', 'Ramo'],
    'conteo': [tratamiento_x_claseImpto, tratamiento_x_nif, tratamiento_x_medMag, error_nif5, error_telefono, error_calle, error_personaFisica, ramo_vacio],
    'Descripcion': ['Empresas que cuentan con clase de impuestos de PN', 'Empresas con tipo de Nif diferente a RUT', 'Empresas con medios magneticos diligenciados', 'Clientes con Nif 5 vacio', 'Clientes con telefono vacio, espacios o guiones', 'Clientes con caracteres especiales en direccion', 'Clientes con check de PF mal diligenciado', 'El campo Ramo (Actividad Economica) se encuentra vacio.']
    }
    
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv(f'{path.ruta_process}/kna1_count_system.csv', index=False)


def client_count_error_user():
    
    
    path = folder_paths()
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_process}result_kna1_user.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_kna1_error = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Cliente': str})
    
    tratamiento_x_claseImpto = df_kna1_error['tratamiento_x_claseImpto'].sum()
    
    tratamiento_x_nif = df_kna1_error['tratamiento_x_nif'].sum()
    
    tratamiento_x_medMag = df_kna1_error['tratamiento_x_medMag'].sum()
    
    error_nif5 = df_kna1_error['error_nif5'].sum()
    
    error_telefono = df_kna1_error['error_telefono'].sum() + df_kna1_error['error_telefono_vacio'].sum()
    
    error_calle = df_kna1_error['error_calle'].sum()
    
    error_personaFisica = df_kna1_error['error_personaFisica'].sum()
    
    ramo_vacio = df_kna1_error['ramo_vacio'].sum()
    
    
    conteo_registros = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'Campo': ['Clase impuestos', 'Nif', 'Medios Magneticos', 'Nif 5', 'Telefono', 'Calle (direccion)', 'Persona Fisica', 'Ramo'],
    'conteo': [tratamiento_x_claseImpto, tratamiento_x_nif, tratamiento_x_medMag, error_nif5, error_telefono, error_calle, error_personaFisica, ramo_vacio],
    'Descripcion': ['Empresas que cuentan con clase de impuestos de PN', 'Empresas con tipo de Nif diferente a RUT', 'Empresas con medios magneticos diligenciados', 'Clientes con Nif 5 vacio', 'Clientes con telefono vacio, espacios o guiones', 'Clientes con caracteres especiales en direccion', 'Clientes con check de PF mal diligenciado', 'El campo Ramo (Actividad Economica) se encuentra vacio.']
    }
    
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv(f'{path.ruta_process}/kna1_count_user.csv', index=False)
    
    
def client_combiner():
    path = folder_paths()
    
    ruta_csv = f'{path.ruta_process}kna1_count.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_kna1_count = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Cliente': str})

    ruta_csv = f'{path.ruta_process}kna1_count_system.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_kna1_count_system = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Cliente': str})

    ruta_csv = f'{path.ruta_process}kna1_count_user.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_kna1_count_user = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Cliente': str})
   
    df_total = pd.DataFrame({
        'id': [],
        'campo':[],
        'conteo_user': [],
        'conteo_system': [],
        'total':[],
        'Descripcion': []
    })
    
    df_total['id'] = df_kna1_count['id']
    df_total['campo'] = df_kna1_count['Campo']
    df_total['total'] = df_kna1_count['conteo']
    df_total['conteo_user'] = df_kna1_count_user['conteo']
    df_total['conteo_system'] = df_kna1_count_system['conteo']
    df_total['Descripcion'] = df_kna1_count['Descripcion']

    df_total.to_csv(f'{path.ruta_final}/kna1_count.csv', index=False)


def sys_user_crea():
    """USER SYSTEM COMPARISON"""
    
    path = folder_paths()
    
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
    
    cli_system_crea = create_system['creado_por']
    cli_user_crea = create_user['creado_por']
    
    return(cli_system_crea, cli_user_crea)
    
    """END"""
    


# La funcion client() debe ser utilizada para ejecutar todas las demas funciones.

def client():
    
    # Llamar a la función
    client_processor()
    client_count_error ()
    sys_filter()
    user_filter()
    client_count_error_system()
    client_count_error_user()
    
    client_combiner()


client()