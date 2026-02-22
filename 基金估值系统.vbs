Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)
batPath = fso.BuildPath(scriptPath, "启动服务.bat")

WshShell.Run chr(34) & batPath & chr(34), 0
Set WshShell = Nothing
