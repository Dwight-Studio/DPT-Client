ECHO OFF
setlocal ENABLEDELAYEDEXPANSION
cd dpt/ressources
for /R %%f in (*.*) do call :ProcessFile %%f
PAUSE
goto :eof

:ProcessFile
For %%A in ("%*") do (
    Set Folder=%%~dpA
    Set Name=%%~nxA
)
set str=%Name%
set str=%str:(=%
set str=%str:)=%
set str=%str: =_%
set str=%str:__=_%
if "%Folder%%str%" neq "%*" (
  echo "%* -> %str%"
  if exist "%Folder%%str%" del "%Folder%%str%"
  rename "%*" "%str%"
)
goto :eof
