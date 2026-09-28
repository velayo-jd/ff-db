import builtins
import sys
import tkinter as tk
from tkinter import ttk

import characters
import terminologies
import locations

BG_MAIN = "#1e1e2e"
BG_SIDE = "#181825"
BG_PANEL = "#242438"
BG_HOVER = "#313147"
FG = "#cdd6f4"
FG_MUTED = "#7f849c"
ACCENT = "#89b4fa"
GREEN = "#a6e3a1"
RED = "#f38ba8"

FONT_UI = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SECTION = ("Segoe UI", 9, "bold")
FONT_MONO = ("Consolas", 11)

SECTIONS = {
    "Characters": [
        ("Add", characters.add_character),
        ("View all", characters.view_characters),
        ("Search", characters.search_character),
        ("Update", characters.update_character),
        ("Delete", characters.delete_character),
    ],
    "Terminologies": [
        ("Add", terminologies.add_terminology),
        ("View all", terminologies.view_terminologies),
        ("Update", terminologies.update_terminology),
        ("Delete", terminologies.delete_terminology),
    ],
    "Locations": [
        ("Add", locations.add_location),
        ("View all", locations.view_locations),
        ("Search", locations.search_location),
        ("Update", locations.update_locations),
        ("Delete", locations.delete_location),
    ],
}


class Cancelled(Exception):
    pass


root = tk.Tk()
root.title("Final Fall Lore Database")
root.geometry("1150x680")
root.minsize(900, 500)
root.configure(bg=BG_MAIN)


def make_button(parent, text, command, bg=BG_SIDE, hover=BG_HOVER, anchor="w", **kw):
    b = tk.Button(parent, text=text, command=command, bg=bg, fg=FG,
                  activebackground=hover, activeforeground=FG, relief="flat",
                  bd=0, font=FONT_UI, anchor=anchor, cursor="hand2", **kw)
    b.bind("<Enter>", lambda e: b.config(bg=hover))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


sidebar = tk.Frame(root, bg=BG_SIDE, width=200)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

main = tk.Frame(root, bg=BG_MAIN)
main.grid(row=0, column=1, sticky="nsew")
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

tk.Label(main, text="Final Fall Lore Database", font=FONT_TITLE,
         bg=BG_MAIN, fg=FG).pack(anchor="w", padx=20, pady=(16, 0))
tk.Label(main, text="Pick an action from the sidebar", font=FONT_UI,
         bg=BG_MAIN, fg=FG_MUTED).pack(anchor="w", padx=20, pady=(0, 10))

status = tk.Label(main, text="Ready", font=FONT_UI, bg=BG_SIDE, fg=FG_MUTED,
                  anchor="w", padx=14, pady=4)
status.pack(side="bottom", fill="x")

frame = tk.Frame(main, bg=BG_MAIN)
frame.pack(fill="both", expand=True, padx=(20, 0), pady=(0, 0))
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

output = tk.Text(frame, font=FONT_MONO, bg=BG_PANEL, fg=FG, insertbackground=FG,
                 relief="flat", wrap="none", state="disabled", padx=14, pady=10)
ysb = ttk.Scrollbar(frame, orient="vertical", command=output.yview)
xsb = ttk.Scrollbar(frame, orient="horizontal", command=output.xview)
output.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
output.grid(row=0, column=0, sticky="nsew")
ysb.grid(row=0, column=1, sticky="ns")
xsb.grid(row=1, column=0, sticky="ew")

output.tag_config("prompt", foreground=ACCENT)
output.tag_config("answer", foreground=GREEN)
output.tag_config("error", foreground=RED)
output.tag_config("muted", foreground=FG_MUTED)


def log(text, tag=None):
    output.config(state="normal")
    output.insert("end", text, tag)
    output.see("end")
    output.config(state="disabled")


def clear_output():
    output.config(state="normal")
    output.delete("1.0", "end")
    output.config(state="disabled")


class TextRedirect:
    def write(self, s):
        log(s)

    def flush(self):
        pass


def gui_input(prompt=""):
    text = prompt.strip() or "Input:"
    result = {"value": None}

    dlg = tk.Toplevel(root)
    dlg.title("Input")
    dlg.configure(bg=BG_PANEL)
    dlg.transient(root)
    dlg.resizable(False, False)

    tk.Label(dlg, text=text, bg=BG_PANEL, fg=FG, font=FONT_UI,
             wraplength=440, justify="left").pack(padx=22, pady=(20, 8), anchor="w")

    entry = tk.Entry(dlg, width=54, font=FONT_UI, bg=BG_MAIN, fg=FG,
                     insertbackground=FG, relief="flat")
    entry.pack(padx=22, pady=4, ipady=7)

    def submit(_=None):
        result["value"] = entry.get()
        dlg.destroy()

    def cancel(_=None):
        dlg.destroy()

    row = tk.Frame(dlg, bg=BG_PANEL)
    row.pack(pady=(12, 18))
    make_button(row, "OK", submit, bg=ACCENT, hover="#a6c8ff", anchor="center",
                width=10, pady=4).pack(side="left", padx=6)
    make_button(row, "Cancel", cancel, bg=BG_HOVER, hover="#3d3d59", anchor="center",
                width=10, pady=4).pack(side="left", padx=6)

    entry.bind("<Return>", submit)
    dlg.bind("<Escape>", cancel)
    dlg.protocol("WM_DELETE_WINDOW", cancel)

    dlg.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - dlg.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - dlg.winfo_height()) // 2
    dlg.geometry(f"+{x}+{y}")

    dlg.wait_visibility()
    dlg.grab_set()
    entry.focus_set()
    root.wait_window(dlg)

    if result["value"] is None:
        raise Cancelled

    log(f"{text} ", "prompt")
    log(f"{result['value']}\n", "answer")
    return result["value"]


builtins.input = gui_input
sys.stdout = TextRedirect()


def run(name, func):
    clear_output()
    status.config(text=f"Running: {name}")
    try:
        func()
    except Cancelled:
        log("\nCancelled.\n", "muted")
    except Exception as e:
        log(f"\nError: {e}\n", "error")
    finally:
        status.config(text="Ready")


for title, actions in SECTIONS.items():
    tk.Label(sidebar, text=title.upper(), font=FONT_SECTION, bg=BG_SIDE,
             fg=FG_MUTED, anchor="w").pack(fill="x", padx=18, pady=(18, 4))
    for label, func in actions:
        make_button(sidebar, label, lambda n=f"{title} - {label}", f=func: run(n, f),
                    padx=18, pady=6).pack(fill="x")


def on_close():
    for module in (characters, terminologies, locations):
        try:
            module.db.close()
        except Exception:
            pass
    root.destroy()


make_button(sidebar, "Exit", on_close, padx=18, pady=8).pack(side="bottom", fill="x", pady=10)
root.protocol("WM_DELETE_WINDOW", on_close)

log("Welcome to the Final Fall Lore Database.\n", "muted")
log("Pick an action from the sidebar to get started.\n", "muted")

root.mainloop()