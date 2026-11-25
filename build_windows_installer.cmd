@echo off
setlocal
set "ROOT=%~dp0"
set "PAYLOAD_DIR=%ROOT%build\windows-installer-payload"

call "%ROOT%build_enterprise_platform.cmd" EnterprisePlatform "%PAYLOAD_DIR%"
if errorlevel 1 exit /b 1

set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" (
    where ISCC.exe >nul 2>nul
    if errorlevel 1 (
        echo Inno Setup 6 is required. Install it from https://jrsoftware.org/isinfo.php
        exit /b 1
    )
    set "ISCC=ISCC.exe"
)

"%ISCC%" "%ROOT%packaging\windows\EnterprisePlatform.iss"
if errorlevel 1 exit /b 1

echo Built: "%ROOT%dist\EnterprisePlatform-Setup.exe"
