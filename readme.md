Partes del flujo de data para generar indicadores de calidad:

librerias requeridas:
et-xmlfile==1.1.0
numpy==2.1.0
openpyxl==3.1.5
pandas==2.2.2
psutil==6.0.0
python-dateutil==2.9.0.post0
pytz==2024.1
six==1.16.0
tzdata==2024.1

logica del proceso:

1- se extrae la informacion de SAP con el script: runVbs.vbs
2- Mediante scripts se convierte la informacion a CSV para ser procesada
3- se cargan los modelos en un data frame mediante pandas
4- En proceso...

Pendientes:

Crear lista de tablas maestras de comparacion
Tipo de nif
Clase de impuestos

se debede validar que
tratamiento empresa no tenga clase de impuestos pn OK
tratamiento empresa no tenga tipo nif <> 31 OK
tratamiento empresa no tenga medios magneticos (nombre3 y nombre4) OK
nif 5 no este vacio
los numeros de telefono no tengan guiones (-)
las direcciones no tengan caracteres especiales (# - grados N`)
check de persona fisica = a nif 13 & clase imp 13

![image](https://github.com/user-attachments/assets/3370451a-e09b-4c7c-8a8d-e8516b99f5b7)
