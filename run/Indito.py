import subprocess
import sys
from pathlib import Path

# login.py elérési útja
login_path = Path(r"C:\Piac_Screener\login.py")

# Ellenőrzés, hogy létezik-e
if login_path.exists():
    # Futtatás Python interpreterrel
    subprocess.run([sys.executable, str(login_path)])
else:
    print(f"A login.py fájl nem található itt: {login_path}")
    input("Nyomj Entert a kilépéshez...")

