param([string]$part)
$fc = "$env:LOCALAPPDATA\Programs\FreeCAD 1.1\bin\freecadcmd.exe"
$root = "C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
$log = "$root\cr_scratch\step6_build_$part.log"
$err = "$root\cr_scratch\step6_build_$part.err"
$p = Start-Process -FilePath $fc -ArgumentList "`"$root\build_parts\$part.py`"" -WorkingDirectory $root -RedirectStandardOutput $log -RedirectStandardError $err -WindowStyle Hidden -PassThru
"$part PID=$($p.Id) start=$(Get-Date -Format HH:mm:ss) log=$log"
