@echo off
call build.bat
if errorlevel 1 goto exit
..\bin\x16emu -debug -scale 2 -prg sour16.prg -run
:exit