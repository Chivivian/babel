@echo off
setlocal

REM Babel Translator - One Command Translation
REM Usage: translate.bat document.pdf --all-languages

REM Use full path to uv
set UV_PATH=%USERPROFILE%\.local\bin\uv.exe

REM Run from script directory
cd /d "%~dp0"
"%UV_PATH%" run python translate.py %*
