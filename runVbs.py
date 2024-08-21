import subprocess

# Ruta al archivo VBScript
vbs_file = 'dataExtract.vbs'

# Ejecutar el archivo VBScript
result = subprocess.run(['cscript.exe', vbs_file], capture_output=True, text=True)

# Imprimir la salida del script
print("Salida estándar:")
print(result.stdout)

# Imprimir errores (si los hay)
print("Errores:")
print(result.stderr)

print("Terminó la ejecución del script VBScript.")