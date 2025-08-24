import os
import sys
from pathlib import Path
import subprocess

# ----------------- Modulok ellenőrzése és telepítése -----------------
def ensure_module(module_name):
    try:
        __import__(module_name)
    except ImportError:
        print(f"A '{module_name}' modul hiányzik. Telepítés...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"'{module_name}' telepítve.")
        __import__(module_name)

ensure_module("pythoncom")
ensure_module("win32com.client")

import pythoncom
import win32com.client

# ----------------- Parancsikon létrehozása -----------------
login_path = Path(r"C:\Piac_Screener\login.py")
if not login_path.exists():
    print(f"A login.py fájl nem található itt: {login_path}")
    input("Nyomj Entert a kilépéshez...")
    sys.exit(1)

desktop = Path.home() / "Desktop"
shortcut_path = desktop / "Piac figyelő.lnk"

try:
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.Targetpath = sys.executable
    shortcut.Arguments = f'"{login_path}"'
    shortcut.WorkingDirectory = str(login_path.parent)
    shortcut.IconLocation = str(sys.executable)
    shortcut.save()
    print(f"Parancsikon sikeresen létrehozva: {shortcut_path}")

    # ----------------- Önmaga törlése -----------------
    script_path = Path(__file__)
    os.remove(script_path)
    print(f"Az Indito.py fájl törölve: {script_path}")

except Exception as e:
    print(f"Hiba történt: {e}")
    input("Nyomj Entert a kilépéshez...")
