"""Shared menu-screen base used by MASTERMENU / EIGMTA-REN / INQUIRYS.

All three share the same skeleton:
    Row 0-1: 2-line header  (EIGALPHA / <subcode>   EIGL / INTA)   with PRODUCTION banner
    Row 2  : centered title
    Row 3  : underscore divider
    Rows N : numbered options
    Row X  : "Selection [n] . . . . . . . . . . ."
    Rows 22-23: F1=Help  F3=Exit  F4=Prompt  F12=Cancel  F24=More keys
"""
from .base import TerminalScreen, spaced, COLS


class MenuScreen(TerminalScreen):
    """Generic numbered-list menu screen. Subclasses define the wiring."""

    subcode: str = ""
    title: str = ""
    options: list[tuple[int, str]] = []
    option_rows: list[int] = []
    routes: dict[int, str] = {}
    selection_row: int = 20
    date_str: str = "24/04/26"
    time_str: str = "11:02:56"
    initial_selection: str = ""

    def __init__(self, master, navigate, back_target: str | None = None, **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.back_target = back_target
        self.selection = self.initial_selection
        self.render()

    def render(self):
        self.clear()
        self._draw_header()

        title = spaced(self.title)
        self.write(2, (COLS - len(title)) // 2, title, tag="green")
        self.write(3, 0, "_" * COLS, tag="green")

        rows = self.option_rows or list(range(5, 5 + 2 * len(self.options), 2))
        for (num, text), row in zip(self.options, rows):
            label = f"{num:>2}. {text}"
            self.write(row, 10, label, tag="green")

        self._draw_selection()
        self._draw_footer()

    def _draw_header(self):
        self.write(0, 0, "EIGALPHA", tag="green")
        self.write(1, 0, self.subcode, tag="green")
        self.write(0, 16, "EIGL", tag="green")
        self.write(1, 16, "INTA", tag="green")
        banner = "< <  P R O D U C T I O N  > >"
        self.write(0, (COLS - len(banner)) // 2, banner, tag="green")
        right = f"{self.date_str}   {self.time_str}"
        self.write(0, COLS - len(right), right, tag="green")

    def _draw_selection(self):
        label = "Selection"
        dots = "." * 40
        self.write(self.selection_row, 2, label, tag="green")
        val = self.selection or " "
        self.write(self.selection_row, 12, val, tag="green")
        self.paint(self.selection_row, 12 + len(val), 1, "cursor")
        self.write(self.selection_row, 14 + len(val), dots[: COLS - 14 - len(val)], tag="green")

    def _draw_footer(self):
        self.write(22, 2,  "F1=Help",       tag="cyan")
        self.write(22, 14, "F3=Exit",       tag="cyan")
        self.write(22, 26, "F4=Prompt",     tag="cyan")
        self.write(22, 40, "F12=Cancel",    tag="cyan")
        self.write(22, 55, "F24=More keys", tag="cyan")

    def _on_key(self, event):
        keysym = event.keysym
        if keysym == "Return":
            if self.selection.isdigit():
                target = self.routes.get(int(self.selection))
                if target:
                    self.navigate(target)
                    return
            self._flash_invalid()
        elif keysym in ("F3",):
            self.navigate("BACK")  # was EXIT (destroyed root) - BACK is a safe no-op if the nav stack is empty
        elif keysym in ("F12", "F1", "F4"):
            if keysym == "F12" and self.back_target:
                self.navigate(self.back_target)
        elif keysym == "BackSpace":
            self.selection = self.selection[:-1]
            self._redraw_selection()
        elif len(event.char) == 1 and event.char.isdigit():
            if len(self.selection) < 2:
                self.selection += event.char
                self._redraw_selection()

    def _redraw_selection(self):
        self._clear_selection_row()
        self._draw_selection()

    def _clear_selection_row(self):
        self.write(self.selection_row, 0, " " * COLS, tag="green")

    def _flash_invalid(self):
        self.write(23, 2, "Invalid selection. Choose an available option.", tag="yellow")
        self.text.after(1500, lambda: self.write(23, 2, " " * 60, tag="green"))
