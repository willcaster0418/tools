Set objShell = Wscript.CreateObject("Wscript.Shell")
'HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default
'HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Servers
'delete 라이브러리\문서\Default.rdp
objShell.RegDelete "HKCU\Software\Microsoft\Terminal Server Client\Default"
objShell.RegDelete "HKCU\Software\Microsoft\Terminal Server Client\Servers"
  
Set objShell = CreateObject("WScript.Shell")
Set colEnvPath = objShell.Environment("Process")
userprofile = colEnvPath("userprofile")
strFile = userprofile+"\documents\Default.rdp"

SET objFSO = CreateObject("Scripting.FileSystemObject")

If objFSO.FileExists(strFile) Then
    objFSO.DeleteFile(strFile)
End If