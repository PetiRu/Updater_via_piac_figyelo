import os
import sys
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import messagebox

# ----------------- Modulok ellenőrzése -----------------
def ensure_module(module_name):
    try:
        __import__(module_name)
    except ImportError:
        status_text.set(f"A '{module_name}' modul hiányzik. Telepítés...")
        root.update()
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        status_text.set(f"'{module_name}' telepítve.")
        root.update()
        __import__(module_name)

# ----------------- Parancsikon létrehozása -----------------
def create_shortcut():
    try:
        import pythoncom
        import win32com.client
    except ImportError:
        ensure_module("pythoncom")
        ensure_module("pywin32")  # win32com benne van

    login_path = Path(r"C:\Piac_Screener\login.py")
    if not login_path.exists():
        messagebox.showerror("Hiba", f"A login.py fájl nem található itt: {login_path}")
        root.destroy()
        sys.exit(1)

    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "Piac figyelő.lnk"

    status_text.set("Parancsikon létrehozása...")
    root.update()

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.Targetpath = sys.executable
    shortcut.Arguments = f'"{login_path}"'
    shortcut.WorkingDirectory = str(login_path.parent)
    shortcut.IconLocation = str(sys.executable)
    shortcut.save()

    status_text.set(f"Parancsikon sikeresen létrehozva: {shortcut_path}")
    root.update()

    # ----------------- Önmaga törlése -----------------
    script_path = Path(__file__)
    try:
        os.remove(script_path)
    except Exception as e:
        messagebox.showwarning("Figyelmeztetés", f"Önmaga törlése sikertelen: {e}")
    root.destroy()

# ----------------- GUI -----------------
root = tk.Tk()
root.title("Indító telepítés")

status_text = tk.StringVar(value="Indítás...")
tk.Label(root, textvariable=status_text, padx=20, pady=20).pack()

root.after(100, create_shortcut)
root.mainloop()
