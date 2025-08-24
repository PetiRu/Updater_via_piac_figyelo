import subprocess
import os
import sys

# A login.py elérési útja
login_path = r"C:\Piac_Screener\login.py"

if os.path.exists(login_path):
    # Python futtatása a login.py-vel
    subprocess.run([sys.executable, login_path], check=True)
else:
    print(f"A login.py fájl nem található itt: {login_path}")
    input("Nyomj Entert a kilépéshez...")
