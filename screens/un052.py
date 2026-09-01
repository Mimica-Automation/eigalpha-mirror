"""UN052 - ADJUSTMENT CALC (POL-ADJCALC).

Covers the "Review Premium Summary" macro: a paged review of the policy's
premium adjustments. Shift+F2 toggles "Adj Calc" (calculation) mode on this
same screen (the recording jumps into/out of it repeatedly rather than it
being a separate screen). F8/F9 page Prev/Next through the adjustment list.
Digit + Enter selects one adjustment (covers "Select Adjustment 1").
Shift+F1 is a generic recalculate/refresh (seen once in the recording with
no further detail - implemented as a harmless status refresh).

F3=Update & Exit hands off to UN053 (POST POLICY ADJUSTMENTS) - the
recording alternates between this screen and that one via Shift+F2 / F3.
F6=Abandon Target returns to wherever this screen was entered from (whatever
screen is passed as back_target - either UN050 or UN053, matching the
reciprocal jumps seen in the recording) without committing anything.
F12=Previous also returns to back_target.
"""
from .base import TerminalScreen, spaced, COLS
from .dummy_data import DEFAULT_POLICY, DEFAULT_ADJUSTMENTS


class UN052(TerminalScreen):
    def __init__(self, master, navigate, policy=None, adjustments=None,
                 back_target: str | None = "UN050", **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.policy = policy or dict(DEFAULT_POLICY)
        self.back_target = back_target
        self.adjustments = adjustments if adjustments is not None else list(DEFAULT_ADJUSTMENTS)

        self.index = 0
        self.selection = ""
        self.calc_mode = False
        self.status = ""
        self.render()

    # ------------------------------------------------------------------
    def render(self):
        self.clear()
        p = self.policy
        self.draw_header("UN052", date_str="24/04/26", time_str="11:25")

        self.write(2, 0, "Renewal review", tag="green")
        title = spaced("ADJUSTMENT CALC")
        self.write(2, (COLS - len(title)) // 2, title, tag="green")
        self.write(3, 0, "_" * COLS, tag="green")

        self.write(4, 0, "Policy . :", tag="green")
        self.write(4, 11, f"{p['policy_branch']} {p['policy_type']} {p['policy_num']}  {p['policy_desc']}", tag="white")

        mode_label = "CALC MODE" if self.calc_mode else "REVIEW MODE"
        self.write(4, 60, mode_label, tag="hl_cyan" if self.calc_mode else "cyan")

        adj = self.adjustments[self.index]
        self.write(7, 4, f"Adjustment {self.index + 1} of {len(self.adjustments)}", tag="green")
        self.write(9, 8,  "Description . . . . :", tag="green")
        self.write(9, 32, adj["desc"], tag="white")
        self.write(10, 8, "Label . . . . . . . :", tag="green")
        self.write(10, 32, adj["label"], tag="white")
        self.write(11, 8, "Premium . . . . . . :", tag="green")
        self.write(11, 32, adj["premium"], tag="hl_green" if adj["label"] == self.selection else "white")

        self.write(14, 8, "Select adjustment number", tag="green")
        val = self.selection or " "
        self.write(14, 34, val, tag="green")
        self.paint(14, 34 + len(val), 1, "cursor")
        self.write(14, 36, "." * 30, tag="green")

        if self.status:
            self.write(17, 4, self.status, tag="yellow")

        self.write(22, 2,  "F8=Prev",           tag="cyan")
        self.write(22, 12, "F9=Next",           tag="cyan")
        self.write(22, 22, "Shift+F2=Adj Calc", tag="cyan")
        self.write(22, 42, "F3=Update & Exit",  tag="cyan")
        self.write(22, 61, "F6=Abandon Target", tag="cyan")
        self.write(23, 0,  "POL-ADJCALC", tag="green")
        self.write(23, 20, "F12=Previous", tag="cyan")

    # ------------------------------------------------------------------
    def _on_key(self, event):
        keysym = event.keysym

        if keysym == "F8":
            self.index = max(0, self.index - 1)
            self.status = ""
            self.render()
            return
        if keysym == "F9":
            self.index = min(len(self.adjustments) - 1, self.index + 1)
            self.status = ""
            self.render()
            return
        if keysym in ("Shift_F2", "F14"):
            # Terminal emulators typically deliver Shift+F2 as one of these
            # keysyms depending on platform/binding; handle both.
            self.calc_mode = not self.calc_mode
            self.status = "Adj Calc mode ON." if self.calc_mode else "Adj Calc mode OFF."
            self.render()
            return
        if keysym in ("Shift_F1", "F13"):
            self.status = "Premium figures refreshed."
            self.render()
            return
        if keysym == "F3":
            self.status = ""
            self.navigate("UN053")
            return
        if keysym == "F6":
            if self.back_target:
                self.navigate(self.back_target)
            return
        if keysym == "F12":
            if self.back_target:
                self.navigate(self.back_target)
            return
        if keysym == "Return":
            if self.selection.isdigit():
                sel_idx = int(self.selection) - 1
                if 0 <= sel_idx < len(self.adjustments):
                    self.index = sel_idx
                    self.selection = self.adjustments[sel_idx]["label"]
                    self.status = f"{self.selection} selected."
                else:
                    self.status = "Invalid adjustment number."
            self.render()
            return
        if keysym == "BackSpace":
            self.selection = self.selection[:-1]
            self.render()
            return
        if len(event.char) == 1 and event.char.isdigit():
            if len(self.selection) < 2:
                self.selection += event.char
                self.render()
