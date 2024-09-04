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

' Construir la fecha del primer día del mes siguiente
firstDayOfNextMonth = DateSerial(Year(Now), Month(Now), 1)
' Construir la fecha del primer día del mes anterior
firstDayOfLasttMonth = DateSerial(Year(Now), Month(Now) - 1, 1)
' Calcular el último día del mes actual restando un día al primer día del mes siguiente
lastDayOfMonth = DateAdd("d", -1, firstDayOfNextMonth)


Dim fechaInicialFormateada, fechaFinalFormateada
partesFecha = Split(firstDayOfLasttMonth, "/")
fechaInicialFormateada = partesFecha(0) & "." & partesFecha(1) & "." & partesFecha(2)

partesFecha = Split(lastDayOfMonth, "/")
fechaFinalFormateada = partesFecha(0) & "." & partesFecha(1) & "." & partesFecha(2)

tabla = Array("KNA1", "LFA1", "MARA", "KNB1", "LFB1")
'tabla = Array("LFB1")

For i=0 To UBound(tabla)


   'Enter transacction
      session.findById("wnd[0]/tbar[0]/okcd").text = "/nzse16n"
      session.findById("wnd[0]").sendVKey 0

   'Select Table to load
      session.findById("wnd[0]/usr/ctxtGD-TAB").text = tabla(i)

   'Select the number of entries requiered
      session.findById("wnd[0]/usr/txtGD-MAX_LINES").text = ""

      If tabla(i) = "KNA1" or tabla(i) = "LFA1" Then

         session.findById("wnd[0]/tbar[0]/btn[71]").press
         session.findById("wnd[1]/usr/sub:SAPLSPO4:0300/txtSVALD-VALUE[0,21]").text = "ERDAT"
         session.findById("wnd[1]").sendVKey 0
         session.findById("wnd[0]/tbar[0]/btn[71]").press
         session.findById("wnd[1]/usr/sub:SAPLSPO4:0300/txtSVALD-VALUE[0,21]").text = "ERDAT"
         session.findById("wnd[1]").sendVKey 0
         session.findById("wnd[0]/usr/tblSAPLZSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-LOW[2,0]").text = fechaInicialFormateada
         session.findById("wnd[0]/usr/tblSAPLZSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-HIGH[3,0]").text = fechaFinalFormateada
         session.findById("wnd[0]").sendVKey 0
         session.findById("wnd[0]/tbar[1]/btn[8]").press
         
      ElseIf tabla(i) = "MARA" Then
         session.findById("wnd[0]/tbar[0]/btn[71]").press
         session.findById("wnd[1]/usr/sub:SAPLSPO4:0300/txtSVALD-VALUE[0,21]").text = "ERSDA"
         session.findById("wnd[1]").sendVKey 0
         session.findById("wnd[0]/tbar[0]/btn[71]").press
         session.findById("wnd[1]/usr/sub:SAPLSPO4:0300/txtSVALD-VALUE[0,21]").text = "ERSDA"
         session.findById("wnd[1]").sendVKey 0
         session.findById("wnd[0]/usr/tblSAPLZSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-LOW[2,0]").text = "01.01.2023"
         session.findById("wnd[0]/usr/tblSAPLZSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-HIGH[3,0]").text = "05.01.2023"
         session.findById("wnd[0]").sendVKey 0
         session.findById("wnd[0]/tbar[1]/btn[8]").press

      ElseIf tabla(i) = "KNB1" Then
      session.findById("wnd[0]/tbar[0]/btn[71]").press
      session.findById("wnd[1]/usr/sub:SAPLSPO4:0300/txtSVALD-VALUE[0,21]").text = "ZZFEACT"
      session.findById("wnd[1]").sendVKey 0
      session.findById("wnd[0]/tbar[0]/btn[71]").press
      session.findById("wnd[1]/usr/sub:SAPLSPO4:0300/txtSVALD-VALUE[0,21]").text = "ZZFEACT"
      session.findById("wnd[1]").sendVKey 0
      session.findById("wnd[0]/usr/tblSAPLZSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-LOW[2,0]").text = "01.01.2023"
      session.findById("wnd[0]/usr/tblSAPLZSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-HIGH[3,0]").text = "05.01.2023"
      session.findById("wnd[0]").sendVKey 0
      session.findById("wnd[0]/tbar[1]/btn[8]").press

      ElseIf tabla(i) = "LFB1" Then
      session.findById("wnd[0]/tbar[0]/btn[71]").press
      session.findById("wnd[1]/usr/sub:SAPLSPO4:0300/txtSVALD-VALUE[0,21]").text = "ZZMMED_FACT"
      session.findById("wnd[1]").sendVKey 0
      session.findById("wnd[0]/tbar[0]/btn[71]").press
      session.findById("wnd[1]/usr/sub:SAPLSPO4:0300/txtSVALD-VALUE[0,21]").text = "ZZMMED_FACT"
      session.findById("wnd[1]").sendVKey 0
      session.findById("wnd[0]/usr/tblSAPLZSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-LOW[2,0]").text = "01.01.2023"
      session.findById("wnd[0]/usr/tblSAPLZSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-HIGH[3,0]").text = "05.01.2023"
      session.findById("wnd[0]").sendVKey 0
      session.findById("wnd[0]/tbar[1]/btn[8]").press

      End If


   'Export the results into Excel format
      session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton "&MB_EXPORT"
      session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem "&XXL"
      session.findById("wnd[1]/tbar[0]/btn[0]").press

   'Select the directory where the file is going to be downloaded
      session.findById("wnd[1]/usr/ctxtDY_PATH").text = "D:\Usuarios\cdlondono\Downloads\04. Proyectos\PYTHON\DataQuality-env\data\raw"
      session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = LCase(tabla(i)) & ".xlsx"
      session.findById("wnd[1]/tbar[0]/btn[0]").press


   
Next 'i