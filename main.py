"""EIGALPHA - Pro Client mirror. Launch: python main.py"""
import json
import os
import tkinter as tk

from screens.base import BG_BLACK
from screens.mastermenu import MASTERMENU
from screens.eigmta_ren import EIGMTA_REN
from screens.inquirys import INQUIRYS
from screens.un034 import UN034
from screens.in001 import IN001
from screens.un021 import UN021
from screens.un045 import UN045
from screens.un050 import UN050
from screens.un051 import UN051
from screens.un052 import UN052
from screens.un053 import UN053
from screens.un054 import UN054
from screens.un489 import UN489

HERE = os.path.dirname(os.path.abspath(__file__))


def load_policy():
    # EIGALPHA_POLICY_FILE lets an automation/test pick which dummy policy
    # record to run against (e.g. data/policy_complaint.json for the
    # complaint-handling scenario) without touching this file.
    filename = os.environ.get("EIGALPHA_POLICY_FILE", "policy.json")
    path = filename if os.path.isabs(filename) else os.path.join(HERE, "data", filename)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


class ProClientApp:
    START = "MASTERMENU"

    def __init__(self, root):
        self.root = root
        self.policy = load_policy()

        root.title("EIGALPHA - Pro Client")
        root.geometry("1100x720")
        root.configure(bg="#F0F0F0")
        try:
            root.state("zoomed")
        except tk.TclError:
            pass

        self._build_menu()
        self._build_toolbar()

        self.terminal_container = tk.Frame(root, bg=BG_BLACK)
        self.terminal_container.pack(fill="both", expand=True)

        self._build_statusbar()

        self.current_screen = None
        self.nav_stack: list[str] = []
        self.navigate(self.START)

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        for label in ("File", "Edit", "View", "Connection", "Options", "Tools", "Help"):
            m = tk.Menu(menubar, tearoff=False)
            if label == "File":
                m.add_command(label="Exit", command=self.root.destroy)
            else:
                m.add_command(label="(not implemented in demo)", state="disabled")
            menubar.add_cascade(label=label, menu=m, underline=0)
        self.root.config(menu=menubar)

    def _build_toolbar(self):
        bar = tk.Frame(self.root, bg="#ECECEC", height=32, bd=1, relief="raised")
        bar.pack(fill="x", side="top")
        icons = [
            ("⌂",         "Home"),
            ("\U0001F5A5", "Connect"),
            ("✂",          "Cut"),
            ("\U0001F4CB", "Copy"),
            ("\U0001F4CE", "Paste"),
            ("↶",         "Undo"),
            ("\U0001F5A8", "Print"),
            ("\U0001F4C4", "Doc"),
            ("\U0001F3A8", "Colors"),
            ("\U0001F4C1", "Open"),
            ("\U0001F4C2", "Folder"),
            ("✏",         "Edit"),
            ("\U0001F4BE", "Save"),
            ("\U0001F4F7", "Snap"),
            ("F7",         "F7"),
            ("?",          "Help"),
        ]
        for glyph, _tip in icons:
            tk.Label(bar, text=glyph, font=("Segoe UI", 11), width=3, bg="#ECECEC", relief="flat").pack(side="left", padx=1, pady=2)

    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg="#ECECEC", height=22, bd=1, relief="sunken")
        bar.pack(fill="x", side="bottom")
        tk.Label(bar, text="Connected", bg="#ECECEC", anchor="w", padx=6, font=("Segoe UI", 9)).pack(side="left")
        tk.Label(bar, text="10,34",     bg="#ECECEC", anchor="e", padx=6, font=("Segoe UI", 9)).pack(side="right")
        tk.Label(bar, text="MW",        bg="#ECECEC", anchor="e", padx=6, font=("Segoe UI", 9)).pack(side="right")
        tk.Label(bar, text="SA",        bg="#ECECEC", anchor="e", padx=6, font=("Segoe UI", 9)).pack(side="right")

    def navigate(self, target):
        if target == "EXIT":
            self.root.destroy()
            return
        if target == "BACK":
            if not self.nav_stack:
                return
            target = self.nav_stack.pop()
            push_new = False
        else:
            if self.current_screen is not None:
                self.nav_stack.append(self._current_name())
            push_new = True

        if self.current_screen is not None:
            self.current_screen.destroy()

        if target == "MASTERMENU":
            self.current_screen = MASTERMENU(self.terminal_container, self.navigate, back_target="EXIT")
        elif target == "EIGMTA-REN":
            self.current_screen = EIGMTA_REN(self.terminal_container, self.navigate, back_target="BACK")
        elif target == "INQUIRYS":
            self.current_screen = INQUIRYS(self.terminal_container, self.navigate, back_target="BACK")
        elif target == "UN034":
            self.current_screen = UN034(self.terminal_container, self.navigate, back_target="BACK")
        elif target == "IN001":
            self.current_screen = IN001(self.terminal_container, self.navigate)
        elif target == "UN021":
            self.current_screen = UN021(self.terminal_container, self.navigate, self.policy)
        elif target == "UN045":
            self.current_screen = UN045(self.terminal_container, self.navigate, policy=self.policy, back_target="UN021")
        elif target == "UN050":
            self.current_screen = UN050(self.terminal_container, self.navigate, policy=self.policy, back_target="UN045")
        elif target == "UN051":
            self.current_screen = UN051(self.terminal_container, self.navigate, policy=self.policy, back_target="UN050")
        elif target == "UN052":
            self.current_screen = UN052(self.terminal_container, self.navigate, policy=self.policy, back_target="UN050")
        elif target == "UN053":
            self.current_screen = UN053(self.terminal_container, self.navigate, policy=self.policy, back_target="UN052")
        elif target == "UN054":
            self.current_screen = UN054(self.terminal_container, self.navigate, back_target="MASTERMENU")
        elif target == "UN489":
            self.current_screen = UN489(self.terminal_container, self.navigate, self.policy)
        else:
            raise ValueError(f"Unknown screen: {target}")

        self.current_screen.pack(fill="both", expand=True)
        self.current_screen.focus_terminal()
        self._current = target

    def _current_name(self):
        return getattr(self, "_current", None)


def main():
    root = tk.Tk()
    ProClientApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
