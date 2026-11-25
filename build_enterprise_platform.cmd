@echo off
setlocal
set "ROOT=%~dp0"
set "APP_NAME=%~1"
if "%APP_NAME%"=="" set "APP_NAME=EnterprisePlatform"
set "OUTPUT_DIR=%~2"
if "%OUTPUT_DIR%"=="" set "OUTPUT_DIR=%ROOT%dist"

python -m pip install -r "%ROOT%backend\requirements-desktop.txt"
if errorlevel 1 exit /b 1

pushd "%ROOT%frontend"
call npm.cmd run build
if errorlevel 1 (
    popd
    exit /b 1
)
popd

python -m PyInstaller --clean --noconfirm --onefile --windowed ^
    --name "%APP_NAME%" ^
    --paths "%ROOT%backend" ^
    --add-data "%ROOT%frontend\dist;frontend\dist" ^
    --distpath "%OUTPUT_DIR%" ^
    --workpath "%ROOT%build\pyinstaller" ^
    --specpath "%ROOT%build\spec" ^
    "%ROOT%desktop_launcher.py"
if errorlevel 1 exit /b 1

echo Built: "%OUTPUT_DIR%\%APP_NAME%.exe"
