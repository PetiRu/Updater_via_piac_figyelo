import subprocess
import sys
import os
from tkinter import messagebox, Tk

def run_login_py(install_path=r"C:\Piac_Screener"):
    # Ellenőrizzük, hogy a login.py létezik-e
    login_path = os.path.join(install_path, "login.py")
    if os.path.exists(login_path):
        try:
            # Elindítjuk a login.py-t az aktuális Python futtatóval
            subprocess.Popen([sys.executable, login_path], cwd=install_path)
            root = Tk()
            root.withdraw()  # Ne jelenjen meg fő ablak
            messagebox.showinfo("Info", "A login.py elindítva.")
            root.destroy()
        except Exception as e:
            root = Tk()
            root.withdraw()
            messagebox.showerror("Hiba", f"Hiba a login.py indítása közben:\n{e}")
            root.destroy()
    else:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Hiba", "Nem található a login.py a telepítési mappában.")
        root.destroy()

if __name__ == "__main__":
    run_login_py()
