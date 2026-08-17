Dim ruta, WshShell
ruta = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d """ & ruta & """ && .\venv\Scripts\python.exe bot.py >> bot.log 2>&1", 0, False
Set WshShell = Nothing
WScript.Echo "Bot iniciado en segundo plano. Revisa bot.log para ver actividad."
