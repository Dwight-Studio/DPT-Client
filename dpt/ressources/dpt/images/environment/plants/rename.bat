for %%f in (*_*.txt) do call :ProcessFile %%f

:ProcessFile
set str=%1
rename str=%str: (=_%
goto :eof