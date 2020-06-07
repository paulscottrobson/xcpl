@echo off
pushd ..\runtime
call build.bat
popd
del dump*.bin >NUL
rem python _testcg.py
python _exprtest.py
..\bin\x16emu -debug -scale 2 -prg test.prg -run

