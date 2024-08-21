Dim objEcxcel
Dim objSheet
Set objExcel = GetObject(,"Excel.Application")
Set objSheet = objExcel.ActiveWorkbook

' Cerrar Excel
objExcel.Quit