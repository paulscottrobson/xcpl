@echo off
pushd ..\runtime
call build.bat
popd
if errorlevel 1 goto exit
del /Q dump*.bin 2>NUL
del /Q xc.zip 2>NUL
rem python _testcg.py
rem python _exprtest.py
rem python instruction.py
rem python filecomp.py
zip -q -9 xc.zip *.py
copy xc.zip ..\bin >NUL
python xc.zip -p test.xp
if errorlevel 1 goto exit
..\bin\x16emu -debug -scale 2 -prg test.prg -run
:exit
