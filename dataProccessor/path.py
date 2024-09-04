class Paths:

    def __init__(self):
    
        # Llamamos la funcion para procesar archivos temp
        self.ruta_temp = 'D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/temp/'
        self.ruta_general_tables = 'D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/generalTabes'
        self.ruta_raw = 'D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/process/raw'
        
        self.ruta_final = 'D:/Usuarios/cdlondono/OneDrive - Corporativo/ETL/DataQuality/final/'
        

def folder_paths():
    return Paths()