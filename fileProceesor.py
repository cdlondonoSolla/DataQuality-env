import pandas as pd

# Ruta al archivo CSV
ruta_csv = 'data/temp/kna1.csv'

# Cargar el archivo CSV en un DataFrame con opciones adicionales
df = pd.read_csv(
    ruta_csv,
    sep=',',  # Delimitador
    header=0,  # Primera fila como encabezado
    dtype={'Columna1': str, 'Columna2': float},  # Tipos de datos
    na_values=['NA', 'N/A']  # Valores a considerar como NaN
)

# Mostrar las primeras filas del DataFrame
print(df.head())
