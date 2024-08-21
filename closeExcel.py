import psutil

def cerrar_excel():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'EXCEL.EXE':
            try:
                proc.terminate()
                proc.wait()  # Espera a que el proceso termine
                print("Excel cerrado.")
            except psutil.NoSuchProcess:
                print("El proceso ya no existe.")
            except psutil.AccessDenied:
                print("No se tiene permiso para cerrar el proceso.")
            except psutil.TimeoutExpired:
                print("No se pudo cerrar el proceso en el tiempo esperado.")
            except Exception as e:
                print(f"Error al cerrar el proceso: {e}")


