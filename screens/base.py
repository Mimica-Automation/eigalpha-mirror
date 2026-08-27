"""Shared terminal grid widget: 24 rows x 80 columns, monospace, tag-based coloring."""
import tkinter as tk
from tkinter import font as tkfont

BG_BLACK   = "#000000"
FG_GREEN   = "#25E025"
FG_CYAN    = "#25E0E0"
FG_WHITE   = "#F0F0F0"
FG_YELLOW  = "#E0E025"
HL_GREEN   = "#00B000"
HL_CYAN    = "#00C0C0"
HL_PINK    = "#E070B0"
BLACK_TEXT = "#000000"

ROWS = 24
COLS = 80


def make_term_font(root):
    for family in ("Consolas", "Lucida Console", "Courier New"):
        try:
            f = tkfont.Font(root=root, family=family, size=14, weight="bold")
            if f.actual("family").lower().startswith(family.split()[0].lower()):
                return f
        except tk.TclError:
            continue
    return tkfont.Font(root=root, family="TkFixedFont", size=14, weight="bold")


class TerminalScreen(tk.Frame):
    """Fixed 24x80 monochrome-green terminal grid with tag overlays."""

    def __init__(self, master, on_key=None, **kw):
        super().__init__(master, bg=BG_BLACK, **kw)
        self.on_key = on_key
        self.font = make_term_font(self)

        self.text = tk.Text(
            self,
            width=COLS,
            height=ROWS,
            bg=BG_BLACK,
            fg=FG_GREEN,
            insertbackground=FG_GREEN,
            font=self.font,
            bd=0,
            padx=8,
            pady=6,
            wrap="none",
            highlightthickness=0,
            takefocus=1,
            cursor="arrow",
        )
        self.text.pack(fill="both", expand=True)

        blank = "\n".join([" " * COLS for _ in range(ROWS)])
        self.text.insert("1.0", blank)
        self.text.configure(state="disabled")

        self.text.tag_configure("green",       foreground=FG_GREEN)
        self.text.tag_configure("cyan",        foreground=FG_CYAN)
        self.text.tag_configure("white",       foreground=FG_WHITE)
        self.text.tag_configure("yellow",      foreground=FG_YELLOW)
        self.text.tag_configure("hl_green",    background=HL_GREEN, foreground=BLACK_TEXT)
        self.text.tag_configure("hl_cyan",     background=HL_CYAN,  foreground=BLACK_TEXT)
        self.text.tag_configure("hl_cyanbox",  background=HL_CYAN,  foreground=BLACK_TEXT)
        self.text.tag_configure("hl_cyanpanel",background=HL_CYAN)
        self.text.tag_configure("panel_dark",  background=BG_BLACK, foreground=FG_GREEN)
        self.text.tag_configure("cursor",      background=HL_PINK,  foreground=FG_WHITE)
        self.text.tag_configure("input",       foreground=FG_GREEN, underline=True)
        self.text.tag_configure("input_cyanbg",background=HL_CYAN,  foreground=FG_GREEN, underline=True)

        self.text.bind("<Key>", self._handle_key)
        self.text.bind("<FocusIn>", lambda e: None)

    def _handle_key(self, event):
        if self.on_key:
            self.on_key(event)
        return "break"

    def focus_terminal(self):
        self.text.focus_set()

    def write(self, row, col, text, tag="green"):
        if row < 0 or row >= ROWS:
            return
        if col < 0:
            return
        max_len = COLS - col
        if max_len <= 0:
            return
        text = text[:max_len]
        start = f"{row+1}.{col}"
        end   = f"{row+1}.{col+len(text)}"
        self.text.configure(state="normal")
        self.text.delete(start, end)
        self.text.insert(start, text, tag)
        self.text.configure(state="disabled")

    def paint(self, row, col, length, tag):
        start = f"{row+1}.{col}"
        end   = f"{row+1}.{col+length}"
        self.text.configure(state="normal")
        self.text.tag_add(tag, start, end)
        self.text.configure(state="disabled")

    def clear(self):
        blank = "\n".join([" " * COLS for _ in range(ROWS)])
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", blank)
        for t in ("green","cyan","white","yellow","hl_green","hl_cyan",
                  "hl_cyanbox","hl_cyanpanel","panel_dark","cursor","input","input_cyanbg"):
            self.text.tag_remove(t, "1.0", "end")
        self.text.configure(state="disabled")

    def draw_header(self, screen_code, date_str="22/04/26", time_str="15:34"):
        self.write(0, 0, screen_code, tag="green")
        title = "< <  P R O D U C T I O N  > >"
        title_col = (COLS - len(title)) // 2
        self.write(0, title_col, title, tag="green")
        right = f"{date_str}   {time_str}"
        self.write(0, COLS - len(right), right, tag="green")
        self.write(1, 0, "_" * COLS, tag="green")


def spaced(text):
    """Turn 'PRODUCTION' into 'P R O D U C T I O N ' (widely-spaced letter style)."""
    return " ".join(text)
