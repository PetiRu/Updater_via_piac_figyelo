import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests, zipfile, io, os, subprocess, sys, re
from pathlib import Path
import shutil

# ----------------- Konfiguráció -----------------
GITHUB_ZIP_URL = "https://github.com/PetiRu/Updater_via_piac_figyelo/raw/main/zip/"
ZIP_OPTIONS = {
    "PISTI": [
        ("pisti_piac_figyelo_dax.zip", "DAX részvényeket tartalmaz"),
        ("pisti_piac_figyelo_full.zip", "Tartalmazza a német, angol, amerikai, kanadai tőzsdét")
    ],
    "KRISZTIAN": [
        ("krisztian_piac_figyelo_plus.zip", "Tartalmazza az angol, amerikai, német, kanadai tőzsdét")
    ]
}
DEFAULT_INSTALL_PATH = r"C:\Piac_Screener"
REQUIREMENTS_PATH = "/main/archive/refs/heads/requirements.txt"
INDITO_GITHUB_URL = "https://github.com/PetiRu/Updater_via_piac_figyelo/blob/1991dcf555409a288a3c2f32d6924ab0682e6f55/run/Indito"
INDITO_PATH = "Indito.py"
PYTHON_DOWNLOAD_URL = "https://www.python.org/ftp/python/3.13.6/python-3.13.6-amd64.exe"

# ----------------- Python ellenőrzés -----------------
def ensure_python():
    try:
        version_output = subprocess.check_output([sys.executable, "--version"], text=True)
        if "3.13" not in version_output:
            raise Exception("Python 3.13 nincs telepítve.")
    except Exception:
        msg = "Python 3.13 nincs telepítve. Letöltjük és telepítjük."
        print(msg)
        installer_path = Path("python_installer.exe")
        r = requests.get(PYTHON_DOWNLOAD_URL, stream=True)
        with open(installer_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        subprocess.run([str(installer_path), "/quiet", "InstallAllUsers=1", "PrependPath=1"])
        installer_path.unlink()
        messagebox.showinfo("Python telepítés", "Python 3.13 telepítve lett. Indítsd újra a telepítőt.")
        sys.exit(0)

# ----------------- GUI -----------------
class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Piac Screener Telepítő")
        self.user_var = tk.StringVar(value="")
        self.zip_var = tk.StringVar(value="")
        self.install_path = tk.StringVar(value=DEFAULT_INSTALL_PATH)

        tk.Label(root, text="Ki telepíti a szoftvert?").pack(pady=5)
        for user in ZIP_OPTIONS.keys():
            tk.Radiobutton(root, text=user, variable=self.user_var, value=user, command=self.update_zip_options).pack(anchor="w")

        tk.Label(root, text="Válassz verziót:").pack(pady=5)
        self.zip_menu = ttk.Combobox(root, textvariable=self.zip_var, state="readonly")
        self.zip_menu.pack(fill="x", padx=20)

        tk.Label(root, text="Telepítési hely:").pack(pady=5)
        path_frame = tk.Frame(root)
        path_frame.pack(fill="x", padx=20)
        tk.Entry(path_frame, textvariable=self.install_path).pack(side="left", fill="x", expand=True)
        tk.Button(path_frame, text="Tallózás", command=self.browse_path).pack(side="left", padx=5)

        tk.Button(root, text="Telepítés és Indítás", command=self.start_install).pack(pady=20)

        self.status_text = tk.StringVar(value="")
        tk.Label(root, textvariable=self.status_text, fg="blue").pack(pady=5)

    def update_zip_options(self):
        user = self.user_var.get()
        options = [f"{name} ({desc})" for name, desc in ZIP_OPTIONS.get(user, [])]
        self.zip_menu['values'] = options
        if options:
            self.zip_menu.current(0)

    def browse_path(self):
        folder = filedialog.askdirectory(initialdir=self.install_path.get())
        if folder:
            self.install_path.set(folder)

    def start_install(self):
        try:
            ensure_python()
        except Exception as e:
            messagebox.showerror("Hiba", f"Python ellenőrzés sikertelen: {e}")
            return

        user = self.user_var.get()
        zip_selection = self.zip_var.get()
        install_dir = self.install_path.get()

        if not user or not zip_selection:
            messagebox.showerror("Hiba", "Válassz felhasználót és verziót!")
            return

        zip_name = zip_selection.split()[0]
        self.status_text.set("ZIP letöltése...")
        self.root.update()

        try:
            # ZIP letöltés
            r = requests.get(GITHUB_ZIP_URL + zip_name)
            r.raise_for_status()
            self.status_text.set("ZIP kicsomagolása...")
            self.root.update()

            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                z.extractall(install_dir)

            # requirements.txt letöltés
            self.status_text.set("Requirements letöltése...")
            self.root.update()
            req_url = f"https://raw.githubusercontent.com/PetiRu/Updater_via_piac_figyelo/main/{REQUIREMENTS_PATH}"
            req_resp = requests.get(req_url)
            req_resp.raise_for_status()
            req_file = Path(install_dir) / "requirements.txt"
            req_file.write_text(req_resp.text, encoding="utf-8")

            # Pip frissítés és telepítés
            self.status_text.set("Pip frissítése...")
            self.root.update()
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

            self.status_text.set("Csomagok telepítése...")
            self.root.update()
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--prefer-binary", "-r", str(req_file)])

            # ----------------- Indito.exe letöltés -----------------
            self.status_text.set("Indító letöltése és futtatása...")
            self.root.update()
            indito_full_path = Path(install_dir) / INDITO_PATH
            if not indito_full_path.exists():
                r = requests.get(INDITO_GITHUB_URL, stream=True)
                r.raise_for_status()
                with open(indito_full_path, "wb") as f:
                    shutil.copyfileobj(r.raw, f)

            subprocess.Popen([str(indito_full_path)], shell=True)
            self.status_text.set("Telepítés kész!")
            messagebox.showinfo("Siker", "A telepítés sikeresen befejeződött és az Indító elindult.")

        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt: {e}")
            self.status_text.set("Hiba a telepítés során.")

# ----------------- Futtatás -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()
