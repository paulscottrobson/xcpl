@echo off
pushd ..\runtime
call build.bat
popd
if errorlevel 1 goto exit
del /Q dump*.bin 2>NUL
rem python _testcg.py
rem python _exprtest.py
rem python instruction.py
rem python filecomp.py
python compiler.py test.x
if errorlevel 1 goto exit
..\bin\x16emu -debug -scale 2 -prg test.prg -run
:exit
