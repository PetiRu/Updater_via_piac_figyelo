import subprocess
import sys
from pathlib import Path


login_path = Path(r"C:\Piac_Screener\login.py")


if login_path.exists():

    subprocess.run([sys.executable, str(login_path)])
else:
    print(f"A login.py fajl nem találhato itt: {login_path}")
    input("Nyomj Entert a kilepeshez...")

