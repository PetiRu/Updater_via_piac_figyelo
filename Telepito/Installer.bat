@echo off
setlocal

REM --- 1. Ellenőrizzük van-e python ---
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Python nincs telepítve, letöltöm...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe -OutFile python-installer.exe"
    echo [INFO] Telepítem a Pythont...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
)

REM --- 2. Letöltjük a requirements.txt-t a GitHub-ról ---
echo [INFO] requirements.txt letöltése...
powershell -Command "Invoke-WebRequest -Uri https://raw.githubusercontent.com/PetiRu/Updater_via_piac_figyelo/main/requirements.txt -OutFile requirements.txt"

REM --- 3. Telepítjük a csomagokat ---
echo [INFO] Csomagok telepítése...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM --- 4. Elindítjuk a programot ---
echo [INFO] Indítás...
python main.py

pause

