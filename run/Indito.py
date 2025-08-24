# -*- coding: utf-8 -*-
import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

# login.py elérési útja
login_path = Path(r"C:\Piac_Screener\login.py")

def run_login():
    if login_path.exists():
        try:
            subprocess.run([sys.executable, str(login_path)])
        except Exception as e:
            messagebox.showerror("Hiba", f"A login.py futtatása sikertelen: {e}")
    else:
        messagebox.showwarning("Figyelem", f"A login.py fájl nem található itt:\n{login_path}")

# GUI létrehozása
root = tk.Tk()
root.title("Login Indító")
root.geometry("300x150")

label = tk.Label(root, text="Nyomd meg a gombot a login.py futtatásához")
label.pack(pady=20)

button = tk.Button(root, text="Futtatás", command=run_login)
button.pack(pady=10)

root.mainloop()
