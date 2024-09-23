import pandas as pd
import numpy as np
import re
from .path import folder_paths



def provider_processor():
    
    path = folder_paths()
    """
        Para el manejo de este archivo se define como regla general

            error = true
            ok = false

        Siempre que las validaciones arrojen True significa que hay datos sin calidad.
    """
    
     # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_temp}lfa1.csv'

    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    lfa1 = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Tratamiento': str, 'Número fiscal 5': str, 'Teléfono 1': str},  # Tipos de datos
        na_values=['NA', 'N/A']  # Valores a considerar como NaN
    )

    K001 = lfa1['Grupo de cuentas'] == 'K001'
    K002 = lfa1['Grupo de cuentas'] == 'K002'
    K003 = lfa1['Grupo de cuentas'] == 'K003'
    K004 = lfa1['Grupo de cuentas'] == 'K004'
    K005 = lfa1['Grupo de cuentas'] == 'K005'
    K006 = lfa1['Grupo de cuentas'] == 'K006'
    K009 = lfa1['Grupo de cuentas'] == 'K009'


    lfa1['creado_por'] = np.where(K001|K002|K003|K004|K005|K006|K009,
                                  'traer','no_traer')

    lfa1 = lfa1[lfa1['creado_por'] == 'traer']
    
    lfa1 = lfa1  


    lfa1_renamed =  lfa1.rename(columns={'Tipo NIF': 'nif'})
    
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
    lfa1_renamed = pd.merge(lfa1_renamed, nif_renamed, on='nif', how='left')

    # Seleccionar columnas específicas
    validacionNif = ['Acreedor','nif', 'descripcion']
    resultado_seleccionado = lfa1_renamed[validacionNif]


    lfa1_renamed =  lfa1_renamed.rename(columns={'Clase de impuesto': 'claseImp'})
    
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
    resultado = pd.merge(lfa1_renamed, impuesto_renamed, on='claseImp', how='left')
    resultado['tipoPerona'] = resultado['descripcion impuesto'].str[:2]


    # tratamiento empresa no tenga clase de impuestos pn
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['tipoPerona'] == 'PN'

    resultado['tratamiento_x_claseImpto'] = np.where(cond1 & cond2, True, False)


    # tratamiento empresa no tenga tipo nif <> 31
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['nif'] != 31
    cond3 = resultado['Grupo de cuentas'] == 'K001'

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



    # Acreedor tenga Ramo diligenciado
    cond1 = resultado['Ramo'].isnull()

    resultado['ramo_vacio'] = np.where(cond1, True, False)

        
    # Crear una columna 'error_personaFisica' basada en condiciones
    resultado['error_personaFisica'] = False  # Inicializar con un valor por defecto

    # Aplicar condiciones
    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] == 13) & (resultado['Persona física'].isnull()), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] != 13) & (resultado['nif'] == 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] != 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True


    # Seleccionar columnas específicas
    vista = ['Acreedor','tratamiento_x_claseImpto', 
            'tratamiento_x_nif', 'tratamiento_x_medMag','error_nif5',
            'error_telefono', 'error_telefono_vacio', 'error_calle', 
            'error_personaFisica', 'ramo_vacio']

    resultado_seleccionado = resultado[vista]

    resultado_seleccionado.to_csv(f'{path.ruta_process}/result_lfa1.csv', index=False)


def provider_count_error ():
    
    path = folder_paths()
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_process}result_lfa1.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_lfa1_error = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Acreedor': str})
    
    tratamiento_x_claseImpto = df_lfa1_error['tratamiento_x_claseImpto'].sum()
    
    tratamiento_x_nif = df_lfa1_error['tratamiento_x_nif'].sum()
    
    tratamiento_x_medMag = df_lfa1_error['tratamiento_x_medMag'].sum()
    
    error_nif5 = df_lfa1_error['error_nif5'].sum()
    
    error_telefono = df_lfa1_error['error_telefono'].sum() + df_lfa1_error['error_telefono_vacio'].sum()
    
    error_calle = df_lfa1_error['error_calle'].sum()
    
    error_personaFisica = df_lfa1_error['error_personaFisica'].sum()
    
    ramo_vacio = df_lfa1_error['ramo_vacio'].sum()
    
    
    conteo_registros = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'Campo': ['Clase impuestos', 'Nif', 'Medios Magneticos', 'Nif 5', 'Telefono', 'Calle (direccion)', 'Persona Fisica', 'Ramo'],
    'conteo': [tratamiento_x_claseImpto, tratamiento_x_nif, tratamiento_x_medMag, error_nif5, error_telefono, error_calle, error_personaFisica, ramo_vacio],
    'Descripcion': ['Empresas que cuentan con clase de impuestos de PN', 'Empresas con tipo de Nif diferente a RUT', 'Empresas con medios magneticos diligenciados', 'Acreedors con Nif 5 vacio', 'Acreedors con telefono vacio, espacios o guiones', 'Acreedors con caracteres especiales en direccion', 'Acreedors con check de PF mal diligenciado', 'El campo Ramo (Actividad Economica) se encuentra vacio.']
    }
    
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv(f'{path.ruta_process}/lfa1_count.csv', index=False)


def user_filter():
    
    path = folder_paths()
    
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_temp}lfa1.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    lfa1 = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Tratamiento': str, 'Número fiscal 5': str, 'Teléfono 1': str},  # Tipos de datos
        na_values=['NA', 'N/A']  # Valores a considerar como NaN
    )

    lfa1_user = pd.DataFrame(lfa1)

    cond1 = lfa1['Creado por'] == 'USERRFC8'
    cond2 = lfa1['Grupo de cuentas'] == 'K004'

    lfa1_user['creado_por'] = np.where(cond1 | cond2,'system','user')

    df_user = lfa1_user[lfa1_user['creado_por'] == 'user']
    
    lfa1 = df_user    

    lfa1_renamed =  lfa1.rename(columns={'Tipo NIF': 'nif'})

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
    lfa1_renamed = pd.merge(lfa1_renamed, nif_renamed, on='nif', how='left')

    # Seleccionar columnas específicas
    validacionNif = ['Acreedor','nif', 'descripcion']
    resultado_seleccionado = lfa1_renamed[validacionNif]


    lfa1_renamed =  lfa1_renamed.rename(columns={'Clase de impuesto': 'claseImp'})

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
    resultado = pd.merge(lfa1_renamed, impuesto_renamed, on='claseImp', how='left')
    resultado['tipoPerona'] = resultado['descripcion impuesto'].str[:2]


    # tratamiento empresa no tenga clase de impuestos pn
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['tipoPerona'] == 'PN'

    resultado['tratamiento_x_claseImpto'] = np.where(cond1 & cond2, True, False)


    # tratamiento empresa no tenga tipo nif <> 31
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['nif'] != 31
    cond3 = resultado['Grupo de cuentas'] == 'K001'

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



    # Acreedor tenga Ramo diligenciado
    cond1 = resultado['Ramo'].isnull()

    resultado['ramo_vacio'] = np.where(cond1, True, False)

        
    # Crear una columna 'error_personaFisica' basada en condiciones
    resultado['error_personaFisica'] = False  # Inicializar con un valor por defecto

    # Aplicar condiciones
    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] == 13) & (resultado['Persona física'].isnull()), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] != 13) & (resultado['nif'] == 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] != 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True


    # Seleccionar columnas específicas
    vista = ['Acreedor','tratamiento_x_claseImpto', 
            'tratamiento_x_nif', 'tratamiento_x_medMag','error_nif5',
            'error_telefono', 'error_telefono_vacio', 'error_calle', 
            'error_personaFisica', 'ramo_vacio']

    resultado_seleccionado = resultado[vista]

    resultado_seleccionado.to_csv(f'{path.ruta_process}/result_lfa1_user.csv', index=False)
    

def sys_filter():
    
    path = folder_paths()
    
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_temp}lfa1.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    lfa1 = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Tratamiento': str, 'Número fiscal 5': str, 'Teléfono 1': str},  # Tipos de datos
        na_values=['NA', 'N/A']  # Valores a considerar como NaN
    )

    lfa1_user = pd.DataFrame(lfa1)

    cond1 = lfa1['Creado por'] == 'USERRFC8'
    cond2 = lfa1['Grupo de cuentas'] == 'K004'

    lfa1_user['creado_por'] = np.where(cond1 | cond2,'system','user')

    df_user = lfa1_user[lfa1_user['creado_por'] == 'system']
    
    lfa1 = df_user    

    lfa1_renamed =  lfa1.rename(columns={'Tipo NIF': 'nif'})

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
    lfa1_renamed = pd.merge(lfa1_renamed, nif_renamed, on='nif', how='left')

    # Seleccionar columnas específicas
    validacionNif = ['Acreedor','nif', 'descripcion']
    resultado_seleccionado = lfa1_renamed[validacionNif]


    lfa1_renamed =  lfa1_renamed.rename(columns={'Clase de impuesto': 'claseImp'})

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
    resultado = pd.merge(lfa1_renamed, impuesto_renamed, on='claseImp', how='left')
    resultado['tipoPerona'] = resultado['descripcion impuesto'].str[:2]


    # tratamiento empresa no tenga clase de impuestos pn
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['tipoPerona'] == 'PN'

    resultado['tratamiento_x_claseImpto'] = np.where(cond1 & cond2, True, False)


    # tratamiento empresa no tenga tipo nif <> 31
    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['nif'] != 31
    cond3 = resultado['Grupo de cuentas'] == 'K001'

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



    # Acreedor tenga Ramo diligenciado
    cond1 = resultado['Ramo'].isnull()

    resultado['ramo_vacio'] = np.where(cond1, True, False)

        
    # Crear una columna 'error_personaFisica' basada en condiciones
    resultado['error_personaFisica'] = False  # Inicializar con un valor por defecto

    # Aplicar condiciones
    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] == 13) & (resultado['Persona física'].isnull()), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] != 13) & (resultado['nif'] == 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] != 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True


    # Seleccionar columnas específicas
    vista = ['Acreedor','tratamiento_x_claseImpto', 
            'tratamiento_x_nif', 'tratamiento_x_medMag','error_nif5',
            'error_telefono', 'error_telefono_vacio', 'error_calle', 
            'error_personaFisica', 'ramo_vacio']

    resultado_seleccionado = resultado[vista]

    resultado_seleccionado.to_csv(f'{path.ruta_process}/result_lfa1_system.csv', index=False)


def provider_count_error_system():
    
    
    path = folder_paths()
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_process}result_lfa1_system.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_lfa1_error = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Acreedor': str})
    
    tratamiento_x_claseImpto = df_lfa1_error['tratamiento_x_claseImpto'].sum()
    
    tratamiento_x_nif = df_lfa1_error['tratamiento_x_nif'].sum()
    
    tratamiento_x_medMag = df_lfa1_error['tratamiento_x_medMag'].sum()
    
    error_nif5 = df_lfa1_error['error_nif5'].sum()
    
    error_telefono = df_lfa1_error['error_telefono'].sum() + df_lfa1_error['error_telefono_vacio'].sum()
    
    error_calle = df_lfa1_error['error_calle'].sum()
    
    error_personaFisica = df_lfa1_error['error_personaFisica'].sum()
    
    ramo_vacio = df_lfa1_error['ramo_vacio'].sum()
    
    
    conteo_registros = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'Campo': ['Clase impuestos', 'Nif', 'Medios Magneticos', 'Nif 5', 'Telefono', 'Calle (direccion)', 'Persona Fisica', 'Ramo'],
    'conteo': [tratamiento_x_claseImpto, tratamiento_x_nif, tratamiento_x_medMag, error_nif5, error_telefono, error_calle, error_personaFisica, ramo_vacio],
    'Descripcion': ['Empresas que cuentan con clase de impuestos de PN', 'Empresas con tipo de Nif diferente a RUT', 'Empresas con medios magneticos diligenciados', 'Acreedores con Nif 5 vacio', 'Acreedores con telefono vacio, espacios o guiones', 'Acreedores con caracteres especiales en direccion', 'Acreedores con check de PF mal diligenciado', 'El campo Ramo (Actividad Economica) se encuentra vacio.']
    }
    
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv(f'{path.ruta_process}/lfa1_count_system.csv', index=False)


def provider_count_error_user():
    
    
    path = folder_paths()
    # Ruta al archivo CSV
    ruta_csv = f'{path.ruta_process}result_lfa1_user.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_lfa1_error = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Acreedor': str})
    
    tratamiento_x_claseImpto = df_lfa1_error['tratamiento_x_claseImpto'].sum()
    
    tratamiento_x_nif = df_lfa1_error['tratamiento_x_nif'].sum()
    
    tratamiento_x_medMag = df_lfa1_error['tratamiento_x_medMag'].sum()
    
    error_nif5 = df_lfa1_error['error_nif5'].sum()
    
    error_telefono = df_lfa1_error['error_telefono'].sum() + df_lfa1_error['error_telefono_vacio'].sum()
    
    error_calle = df_lfa1_error['error_calle'].sum()
    
    error_personaFisica = df_lfa1_error['error_personaFisica'].sum()
    
    ramo_vacio = df_lfa1_error['ramo_vacio'].sum()
    
    
    conteo_registros = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'Campo': ['Clase impuestos', 'Nif', 'Medios Magneticos', 'Nif 5', 'Telefono', 'Calle (direccion)', 'Persona Fisica', 'Ramo'],
    'conteo': [tratamiento_x_claseImpto, tratamiento_x_nif, tratamiento_x_medMag, error_nif5, error_telefono, error_calle, error_personaFisica, ramo_vacio],
    'Descripcion': ['Empresas que cuentan con clase de impuestos de PN', 'Empresas con tipo de Nif diferente a RUT', 'Empresas con medios magneticos diligenciados', 'Acreedores con Nif 5 vacio', 'Acreedores con telefono vacio, espacios o guiones', 'Acreedores con caracteres especiales en direccion', 'Acreedores con check de PF mal diligenciado', 'El campo Ramo (Actividad Economica) se encuentra vacio.']
    }
    
    conteo_registros = pd.DataFrame(conteo_registros)
    conteo_registros.to_csv(f'{path.ruta_process}/lfa1_count_user.csv', index=False)


def provider_combiner():
    path = folder_paths()
    
    ruta_csv = f'{path.ruta_process}lfa1_count.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_lfa1_count = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Acreedor': str})

    ruta_csv = f'{path.ruta_process}lfa1_count_system.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_lfa1_count_system = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Acreedor': str})

    ruta_csv = f'{path.ruta_process}lfa1_count_user.csv'
    
    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    df_lfa1_count_user = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Acreedor': str})
   
    df_total = pd.DataFrame({
        'id': [],
        'campo':[],
        'conteo_user': [],
        'conteo_system': [],
        'total':[],
        'Descripcion': []
    })
    
    df_total['id'] = df_lfa1_count['id']
    df_total['campo'] = df_lfa1_count['Campo']
    df_total['total'] = df_lfa1_count['conteo']
    df_total['conteo_user'] = df_lfa1_count_user['conteo']
    df_total['conteo_system'] = df_lfa1_count_system['conteo']
    df_total['Descripcion'] = df_lfa1_count['Descripcion']

    df_total.to_csv(f'{path.ruta_final}/lfa1_count.csv', index=False)



def sys_user_crea():
    
    path = folder_paths()
    
    """USER SYSTEM COMPARISON"""
    
    data = {
    'Provider': [],
    'creado_por': []
    }
    
    df_userXsystem = pd.DataFrame(data)
    
    ruta_lfa1 = f'{path.ruta_temp}lfa1.csv'
    df_lfa1 = pd.read_csv(ruta_lfa1)
    
    df_userXsystem['Provider'] = df_lfa1['Acreedor']
    
    # la cantidad de clientes creados automaticamente

    cond1 = df_lfa1['Creado por'] == 'USERRFC8'
    cond2 = df_lfa1['Grupo de cuentas'] == 'K004'

    df_userXsystem['creado_por'] = np.where(cond1 | cond2,'system','user')
    
    create_system = df_userXsystem['creado_por'].str.contains('system', case=False, na=False)
    create_user = df_userXsystem['creado_por'].str.contains('user', case=False, na=False)
    
    # Aplicar el filtro al DataFrame
    create_system = df_userXsystem[create_system].count()
    create_user = df_userXsystem[create_user].count()
    
    prov_system_crea = create_system['creado_por']
    prov_user_crea = create_user['creado_por']
    
    return(prov_system_crea, prov_user_crea)
    
    """END"""
    
# La funcion provider() debe ser utilizada para ejecutar todas las demas funciones.
def provider():
    
    # Llamar a la función
    provider_processor()
    provider_count_error ()
    sys_filter()
    user_filter()
    provider_count_error_system()
    provider_count_error_user()
    
    provider_combiner()


provider()



