import tkinter as tk
from tkinter import ttk, messagebox
from stocks1 import get_tsx_composite
from stocks import get_sp500_stocks
from stocks3 import get_ftse_stocks
from stocks2 import get_dax_stocks
from stocks4 import get_china_stocks
from rules import check_stochastic_buy, LOG_FILE
from colorama import init, Fore, Style
import os
import webbrowser
import subprocess
import sys
from updater import fetch_version, update_all, get_local_version, save_local_version
from docs_updater import update_docs

init(autoreset=True)

# ---------------- Verziófrissítés -----------------
def check_for_updates():
    local_version = get_local_version()
    version_data = fetch_version()
    if not version_data:
        messagebox.showinfo("Info", "Nem sikerült lekérni a verziót a GitHub-ról.")
        return

    github_version = version_data.get("version", "0.0")
    if github_version != local_version:
        if messagebox.askyesno("Frissítés", f"Új verzió elérhető: {github_version} (jelenlegi: {local_version})\nSzeretnéd frissíteni?"):
            update_all()
            update_docs()
            save_local_version(github_version)
            messagebox.showinfo("Info", "Frissítés kész.")
    else:
        messagebox.showinfo("Info", f"Minden fájl naprakész (verzió: {local_version})")

# ---------------- Stochastic elemzés -----------------
def run_analysis():
    stocks = get_sp500_stocks() + get_tsx_composite() + get_ftse_stocks() + get_dax_stocks() + get_china_stocks()
    found = []
    yellow_found = []
    errors = 0

    for name, yfinance_ticker, tradingview_ticker in stocks:
        result = check_stochastic_buy(name, yfinance_ticker)
        if result is None:
            errors += 1
            continue

        value, crossed_today = result
        if value is None:
            errors += 1
            continue

        if value < 16 and crossed_today:
            found.append((name, yfinance_ticker, tradingview_ticker, value))
        elif 0 <= value <= 16:
            yellow_found.append((name, yfinance_ticker, tradingview_ticker, value))

    show_results(found, yellow_found, errors)

# ---------------- GUI -----------------
def show_results(found, yellow_found, errors):
    window = tk.Tk()
    window.title("Stochastic %D Találatok")

    tree = ttk.Treeview(window, columns=("Név", "YFinance Ticker", "Stochastic %D", "TradingView Ticker"), show="headings")
    tree.heading("Név", text="Név")
    tree.heading("YFinance Ticker", text="YFinance Ticker")
    tree.heading("Stochastic %D", text="Stochastic %D")
    tree.heading("TradingView Ticker", text="TradingView Ticker")

    for name, yfinance_ticker, tradingview_ticker, val in found:
        tree.insert("", tk.END, values=(name, yfinance_ticker, val, tradingview_ticker), tags=("green",))
    for name, yfinance_ticker, tradingview_ticker, val in yellow_found:
        tree.insert("", tk.END, values=(name, yfinance_ticker, val, tradingview_ticker), tags=("yellow",))

    tree.tag_configure("green", background="lightgreen")
    tree.tag_configure("yellow", background="yellow")
    tree.pack(fill="both", expand=True)

    label = tk.Label(window, text=f"{len(found)} TALÁLAT, {len(yellow_found)} SÁRGA TALÁLAT, {errors} Hiba", fg="blue")
    label.pack(pady=5)

    frame = tk.Frame(window)
    frame.pack(pady=10)

    tk.Button(frame, text="Újrakeresés", command=lambda:[window.destroy(), run_analysis()]).pack(side="left", padx=5)
    tk.Button(frame, text="Log megnyitása", command=open_log).pack(side="left", padx=5)
    tk.Button(frame, text="Indikátor GUI", command=run_indicator_gui).pack(side="left", padx=5)
    tk.Button(frame, text="Kilépés", command=window.destroy).pack(side="left", padx=5)

    def on_double_click(event):
        item = tree.selection()
        if item:
            tradingview_ticker = tree.item(item, "values")[3]
            url = f"https://www.tradingview.com/symbols/{tradingview_ticker}/"
            webbrowser.open(url)

    tree.bind("<Double-1>", on_double_click)
    window.mainloop()

# ---------------- Log -----------------
def open_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("Log fájl létrehozva.\n")
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    messagebox.showinfo("Error Log", content)

# ---------------- Indikátor GUI -----------------
def run_indicator_gui():
    subprocess.Popen([sys.executable, "indicator.py"])

# ---------------- Fő program -----------------
if __name__ == "__main__":
    check_for_updates()
    run_analysis()

