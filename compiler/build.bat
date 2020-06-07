@echo off
pushd ..\runtime
call build.bat
popd
rem python testcg.py
python exprtest.py
..\bin\x16emu -debug -scale 2 -prg test.prg -run

