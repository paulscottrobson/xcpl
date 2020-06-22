@echo off
64tass -c -q sour16.asm -L sour16.lst -o sour16.prg -l sour16.lbl
if errorlevel 1 goto exit
python parse.py
if errorlevel 1 goto exit
copy sour16.py  ..\compiler >NUL
copy codegen.py ..\compiler >NUL
:exit