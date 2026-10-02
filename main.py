import builtins
import sys
import tkinter as tk
from tkinter import ttk

import characters
import terminologies
import locations

BG_MAIN = "black"
BG_SIDE = "gray10"
BG_PANEL = "gray15"
BG_HOVER = "gray25"
FG = "white"
FG_MUTED = "gray60"
ACCENT = "deep sky blue"
GREEN = "light green"
RED = "tomato"

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
root.title("FF's Database Project")
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


sidebar_outer = tk.Frame(root, bg=BG_SIDE, width=200)
sidebar_outer.grid(row=0, column=0, sticky="ns")
sidebar_outer.grid_propagate(False)
sidebar_outer.rowconfigure(0, weight=1)
sidebar_outer.columnconfigure(0, weight=1)

sidebar_canvas = tk.Canvas(sidebar_outer, bg=BG_SIDE, highlightthickness=0)
sidebar_scroll = ttk.Scrollbar(sidebar_outer, orient="vertical", command=sidebar_canvas.yview)
sidebar = tk.Frame(sidebar_canvas, bg=BG_SIDE)

sidebar_canvas.configure(yscrollcommand=sidebar_scroll.set)
sidebar_canvas.grid(row=0, column=0, sticky="nsew")
sidebar_scroll.grid(row=0, column=1, sticky="ns")

sidebar_window = sidebar_canvas.create_window((0, 0), window=sidebar, anchor="nw")

def _on_sidebar_configure(event):
    sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
    sidebar_canvas.itemconfig(sidebar_window, width=event.width)

sidebar.bind("<Configure>", lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all")))
sidebar_canvas.bind("<Configure>", _on_sidebar_configure)

def _on_sidebar_wheel(event):
    sidebar_canvas.yview_scroll(-1 * (event.delta // 120), "units")

sidebar_canvas.bind("<Enter>", lambda e: sidebar_canvas.bind_all("<MouseWheel>", _on_sidebar_wheel))
sidebar_canvas.bind("<Leave>", lambda e: sidebar_canvas.unbind_all("<MouseWheel>"))

main = tk.Frame(root, bg=BG_MAIN)
main.grid(row=0, column=1, sticky="nsew")
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

header_row = tk.Frame(main, bg=BG_MAIN)
header_row.pack(fill="x", padx=20, pady=(16, 10))

title_block = tk.Frame(header_row, bg=BG_MAIN)
title_block.pack(side="left", anchor="w")

tk.Label(title_block, text="Final Fall Bible", font=FONT_TITLE,
         bg=BG_MAIN, fg=FG).pack(anchor="w")
tk.Label(title_block, text="Have you ever world build with your life on the line?", font=FONT_UI,
         bg=BG_MAIN, fg=FG_MUTED).pack(anchor="w")

logo_img = tk.PhotoImage(file="logo.png")
logo_img = logo_img.subsample(3, 3)
logo_label = tk.Label(header_row, image=logo_img, bg=BG_MAIN)
logo_label.image = logo_img
logo_label.pack(side="right", anchor="e")
status = tk.Label(main, text="Ready", font=FONT_UI, bg=BG_SIDE, fg=FG_MUTED,
                  anchor="w", padx=14, pady=4)
status.pack(side="bottom", fill="x")

frame = tk.Frame(main, bg=BG_MAIN)
frame.pack(fill="both", expand=True, padx=(20, 0), pady=(0, 0))
frame.rowconfigure(1, weight=1)
frame.columnconfigure(0, weight=1)

panel_header = tk.Frame(frame, bg=BG_HOVER, height=34)
panel_header.grid(row=0, column=0, columnspan=2, sticky="ew")
panel_header.grid_propagate(False)
panel_title = tk.Label(panel_header, text="Output", bg=BG_HOVER, fg=FG_MUTED,
                       font=FONT_UI, anchor="w", padx=14)
panel_title.pack(fill="both", expand=True)

output = tk.Text(frame, font=FONT_MONO, bg=BG_PANEL, fg=FG, insertbackground=FG,
                 relief="flat", wrap="none", state="disabled", padx=14, pady=10)
ysb = ttk.Scrollbar(frame, orient="vertical", command=output.yview)
xsb = ttk.Scrollbar(frame, orient="horizontal", command=output.xview)
output.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
output.grid(row=1, column=0, sticky="nsew")
ysb.grid(row=1, column=1, sticky="ns")
xsb.grid(row=2, column=0, sticky="ew")

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
    make_button(row, "OK", submit, bg=ACCENT, hover="light sky blue", anchor="center",
                width=10, pady=4).pack(side="left", padx=6)
    make_button(row, "Cancel", cancel, bg=BG_HOVER, hover="gray35", anchor="center",
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
    panel_title.config(text=name)
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

log("Forgot something? Changing something?\n", "muted")
log("Pick an action from the sidebar and get to it then.\n", "muted")

root.mainloop()