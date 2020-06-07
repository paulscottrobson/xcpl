@echo off
pushd ..\runtime
call build.bat
popd
python testcg.py
