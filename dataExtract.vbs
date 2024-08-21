If Not IsObject(application) Then
   Set SapGuiAuto  = GetObject("SAPGUI")
   Set application = SapGuiAuto.GetScriptingEngine
End If
If Not IsObject(connection) Then
   Set connection = application.Children(0)
End If
If Not IsObject(session) Then
   Set session    = connection.Children(0)
End If
If IsObject(WScript) Then
   WScript.ConnectObject session,     "on"
   WScript.ConnectObject application, "on"
End If

' Crear un nuevo objeto Excel
Dim client

client = Array("kna1","knb1","knvv")
clientSize = UBound(client) - LBound(client) + 1
For i=0 To UBound(client)


'Enter transacction
session.findById("wnd[0]/tbar[0]/okcd").text = "/nzse16n"
session.findById("wnd[0]").sendVKey 0

'Select Table to load
session.findById("wnd[0]/usr/ctxtGD-TAB").text = client(i)

'Select the number of entries requiered
session.findById("wnd[0]/usr/txtGD-MAX_LINES").text = "20"
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/tbar[1]/btn[8]").press

'Export the results into Excel format
session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton "&MB_EXPORT"
session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem "&XXL"
session.findById("wnd[1]/tbar[0]/btn[0]").press

'Select the directory where the file is going to be downloaded
session.findById("wnd[1]/usr/ctxtDY_PATH").text = "D:\Usuarios\cdlondono\Downloads\04. Proyectos\PYTHON\DataQuality-env\data\raw"
session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = client(i) & ".xlsx"
session.findById("wnd[1]/tbar[0]/btn[0]").press
' session.findById("wnd[0]/tbar[0]/btn[12]").press
' session.findById("wnd[0]/tbar[0]/btn[12]").press




Next 'i

' Dim objEcxcel
' Dim objSheet
' Set objExcel = GetObject(,"Excel.Application")
' Set objSheet = objExcel

' ' Cerrar Excel
' objExcel.Quit
