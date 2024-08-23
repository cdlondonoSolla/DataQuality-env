import pandas as pd
import numpy as np
import re

def file_processor():
    """
        Para el manejo de este archivo se define como regla general

            error = true
            ok = false

        Siempre que las validaciones arrojen True significa que hay datos sin calidad.
    """

    # Ruta al archivo CSV
    ruta_csv = 'data/temp/kna1.csv'

    # Cargar el archivo CSV en un DataFrame con opciones adicionales
    kna1 = pd.read_csv(
        ruta_csv,
        sep=',',  # Delimitador
        header=0,  # Primera fila como encabezado
        dtype={'Tratamiento': str, 'Número fiscal 5': str, 'Teléfono 1': str},  # Tipos de datos
        na_values=['NA', 'N/A']  # Valores a considerar como NaN
    )

    kna1_renamed =  kna1.rename(columns={'Tipo NIF': 'nif'})

    # Ruta al archivo CSV
    ruta_csv = 'data/generalTabes/nif.csv'

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
    ruta_csv = 'data\generalTabes\claseImpuesto.csv'

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

    resultado['tratamiento_x_nif'] = np.where(cond1 & cond2,True,False)

    # tratamiento empresa no tenga medios magneticos (nombre1 y nombre2)

    cond1 = resultado['Tratamiento'] == 'Empresa'
    cond2 = resultado['Nombre 3'] == 'NaN'
    cond3 = resultado['Nombre 4'] == 'NaN'

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

    # tratamiento empresa no tenga medios magneticos (nombre1 y nombre2)

        
    # Crear una columna 'error_personaFisica' basada en condiciones
    resultado['error_personaFisica'] = False  # Inicializar con un valor por defecto

    # Aplicar condiciones
    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] == 13) & (resultado['Persona física'].isnull()), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] != 13) & (resultado['nif'] == 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True

    resultado.loc[(resultado['claseImp'] == 13) & (resultado['nif'] != 13) & (resultado['Persona física'] == 'X'), 'error_personaFisica'] = True


    # Seleccionar columnas específicas
    vista = ['Cliente','tratamiento_x_claseImpto', 'tratamiento_x_claseImpto', 
            'tratamiento_x_nif', 'tratamiento_x_medMag','error_nif5',
            'error_telefono', 'error_telefono_vacio', 'error_calle', 
            'error_personaFisica']

    resultado_seleccionado = resultado[vista]

    resultado_seleccionado.to_csv('data/final/result_kna1.csv', index=False)


