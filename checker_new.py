import customtkinter as ctk
import threading
import time
import os
import subprocess
from PIL import Image
from tkinter import messagebox

# ─── НАСТРОЙКИ ───────────────────────────
ctk.set_appearance_mode("dark")

W, H = 920, 580
BG_COLOR = "#c0ff33"
PANEL_COLOR = "#1a001f"
CARD_COLOR = "#24002a"
ACCENT = "#7a2cff"
ACCENT_LIGHT = "#a970ff"
TEXT = "#e8dcff"
DANGER = "#ff4b4b"

NEED_UPDATE = True              # ← если True, чекер блокируется
UPDATER_EXE = "updater.exe"     # ← обновлятор рядом с exe

KEYWORDS = ["krnl","fluxus","synapse","injector","executor","cheat"]
SCAN_DIRS = [
    os.path.join(os.environ["USERPROFILE"], "Downloads"),
    os.environ.get("APPDATA",""),
    os.environ.get("LOCALAPPDATA",""),
    os.environ.get("TEMP","")
]

def resource_path(relative_path):
    import sys
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ─── ОКНО ───────────────────────────────
app = ctk.CTk()
app.geometry(f"{W}x{H}")
app.title("Odessa Cheat Checker")
app.configure(fg_color=BG_COLOR)
app.resizable(False, False)

# ─── ГЛАВНАЯ ПАНЕЛЬ ─────────────────────
main = ctk.CTkFrame(app, fg_color=PANEL_COLOR, corner_radius=28)
main.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.93, relheight=0.92)

content = ctk.CTkFrame(main, fg_color="transparent")
content.pack(expand=True, fill="both", padx=20, pady=20)

left = ctk.CTkFrame(content, fg_color="transparent")
left.pack(side="left", fill="y", padx=(0, 15))

right = ctk.CTkFrame(content, fg_color="transparent")
right.pack(side="right", expand=True, fill="both", padx=20, pady=20)

# ─── ЛОГ ────────────────────────────────
log = ctk.CTkTextbox(right, fg_color=CARD_COLOR, corner_radius=25,
                     text_color=TEXT, font=("Consolas",13))
log.pack(expand=True, fill="both", pady=(0,12))
log.insert("end","[INFO] Ready.\n")

progress = ctk.CTkProgressBar(right, progress_color=ACCENT,
                              fg_color="#320040", height=16, corner_radius=12)
progress.set(0)

# ─── СКАН ───────────────────────────────
def scan_files():
    found=[]
    for folder in SCAN_DIRS:
        if not os.path.exists(folder): continue
        for root, _, files in os.walk(folder):
            for f in files:
                if any(k in f.lower() for k in KEYWORDS):
                    found.append(os.path.join(root,f))
    return found

def start_scan():
    progress.pack(fill="x", pady=(0,12))
    def scan():
        log.delete("1.0","end")
        steps=["Initializing","Scanning directories","Analyzing","Finalizing"]
        for i,s in enumerate(steps):
            log.insert("end", f"[CHECK] {s}...\n")
            progress.set((i+1)/len(steps))
            time.sleep(0.7)
        results=scan_files()
        if not results:
            log.insert("end","\n[RESULT] ✔ No threats detected\n")
        else:
            log.insert("end",f"\n[RESULT] ⚠ Found {len(results)} files\n\n")
            for r in results:
                log.insert("end", r+"\n", "danger")
            log.tag_config("danger", foreground=DANGER)
    threading.Thread(target=scan, daemon=True).start()

# ─── OVERLAY ОБНОВЛЕНИЯ ──────────────────
def start_update():
    if os.path.exists(UPDATER_EXE):
        subprocess.Popen([UPDATER_EXE])
        app.destroy()
    else:
        messagebox.showerror("Ошибка", "updater.exe не найден")

if NEED_UPDATE:
    overlay = ctk.CTkFrame(app, fg_color="#000000")
    overlay.place(x=0, y=0, relwidth=1, relheight=1)
    overlay.lift()
    overlay.grab_set()

    box = ctk.CTkFrame(overlay, fg_color=PANEL_COLOR, corner_radius=28)
    box.place(relx=0.5, rely=0.5, anchor="center", width=480, height=260)

    ctk.CTkLabel(
        box, text="Требуется обновление",
        font=("Segoe UI Black",22), text_color=TEXT
    ).pack(pady=(35,10))

    ctk.CTkLabel(
        box,
        text="Для корректной работы чекера\nнеобходимо установить обновление",
        font=("Segoe UI",14),
        text_color="#bfa7ff",
        justify="center"
    ).pack(pady=10)

    ctk.CTkButton(
        box, text="ОБНОВИТЬ", command=start_update,
        corner_radius=30, height=55,
        font=("Segoe UI Semibold",16),
        fg_color=ACCENT, hover_color=ACCENT_LIGHT,
        text_color="white"
    ).pack(pady=25, ipadx=25)

app.mainloop()
