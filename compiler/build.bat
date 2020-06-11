@echo off
pushd ..\runtime
call build.bat
popd
del /Q dump*.bin
#python _testcg.py
#python _exprtest.py
python instruction.py
..\bin\x16emu -debug -scale 2 -prg test.prg -run

