@echo off
pushd ..\runtime
call build.bat
popd
if errorlevel 1 goto exit
del /Q dump*.bin
rem python _testcg.py
rem python _exprtest.py
python instruction.py
if errorlevel 1 goto exit
..\bin\x16emu -debug -scale 2 -prg test.prg -run
:exit
