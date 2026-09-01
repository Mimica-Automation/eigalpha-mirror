"""UN054 - QUOTATIONS & NEW BUSINESS MENU FOR EIG / Selection Panel (POL-SUBMIT).

Covers the "Submit Policy Renewal Review" macro. Subclasses MenuScreen
(same numbered-option skeleton as MASTERMENU/EIGMTA-REN/INQUIRYS) but:

  * the bottom prompt reads "Selection Panel" instead of "Selection" (the
    recording's field is literally called that), and
  * it accepts a 3-letter command ("OVC") typed into that same prompt, in
    addition to a plain digit route - covers the "Select OVC in EIGALPHA"
    action, which returns to the master/overview menu.

Route 3 ("Policy Renewal Review") does not jump straight to another screen:
picking it switches this same screen into a "policy_entry" panel state that
prompts for a policy number inline (mirrors "Write: Policy Number in
EIGALPHA" immediately following the "3 in Selection Panel" + Enter in the
recording) before navigating on to UN021 (POLICY HEADER, already provided by
the base mirror - out of scope for this task).

"Write: Quotations & New Business Menu for EIG" from the recording is
modelled as this screen's fixed `title` - i.e. this *is* that menu.
"""
from .menu import MenuScreen
from .base import spaced, COLS


class UN054(MenuScreen):
    subcode = "POL-SUBMIT"
    title = "QUOTATIONS & NEW BUSINESS MENU"
    options = [
        (1, "Mid Term Quotations"),
        (2, "Endorsements"),
        (3, "Policy Renewal Review"),
        (4, "Individual Policy Revision List"),
    ]
    routes = {3: "__POLICY_ENTRY__"}
    selection_row = 20
    date_str = "24/04/26"
    time_str = "11:35"

    def __init__(self, master, navigate, back_target: str | None = "MASTERMENU", **kw):
        self.stage = "top"           # "top" | "policy_entry"
        self.policy_number = ""
        super().__init__(master, navigate, back_target=back_target, **kw)

    # ------------------------------------------------------------------
    def render(self):
        if self.stage == "policy_entry":
            self._render_policy_entry()
            return
        super().render()

    def _render_policy_entry(self):
        self.clear()
        self._draw_header()

        title = spaced(self.title)
        self.write(2, (COLS - len(title)) // 2, title, tag="green")
        self.write(3, 0, "_" * COLS, tag="green")

        self.write(8, 10, "3. Policy Renewal Review", tag="green")
        self.write(10, 10, "Policy number . . . . :", tag="green")
        val = self.policy_number.ljust(11, "_")
        self.write(10, 34, val, tag="input")
        self.paint(10, 34 + min(len(self.policy_number), 10), 1, "cursor")

        self.write(22, 2,  "F1=Help",    tag="cyan")
        self.write(22, 14, "F3=Exit",    tag="cyan")
        self.write(22, 26, "F12=Cancel", tag="cyan")

    # ------------------------------------------------------------------
    def _draw_selection(self):
        label = "Selection Panel"
        dots = "." * 34
        self.write(self.selection_row, 2, label, tag="green")
        val = self.selection or " "
        self.write(self.selection_row, 18, val, tag="green")
        self.paint(self.selection_row, 18 + len(val), 1, "cursor")
        self.write(self.selection_row, 20 + len(val), dots[: COLS - 20 - len(val)], tag="green")

    def _clear_selection_row(self):
        self.write(self.selection_row, 0, " " * COLS, tag="green")

    def _redraw_selection(self):
        self._clear_selection_row()
        self._draw_selection()

    # ------------------------------------------------------------------
    def _on_key(self, event):
        keysym = event.keysym

        if self.stage == "policy_entry":
            self._on_key_policy_entry(event)
            return

        if keysym == "Return":
            sel = self.selection.strip().upper()
            if sel == "OVC":
                self.navigate(self.back_target or "MASTERMENU")
                return
            if sel.isdigit():
                target = self.routes.get(int(sel))
                if target == "__POLICY_ENTRY__":
                    self.stage = "policy_entry"
                    self.policy_number = ""
                    self.render()
                    return
                if target:
                    self.navigate(target)
                    return
            self._flash_invalid()
            return
        if keysym == "F3":
            self.navigate("BACK")  # was EXIT (destroyed root) - BACK is a safe no-op if the nav stack is empty
            return
        if keysym == "F12":
            if self.back_target:
                self.navigate(self.back_target)
            return
        if keysym == "BackSpace":
            self.selection = self.selection[:-1]
            self._redraw_selection()
            return
        if len(event.char) == 1 and (event.char.isdigit() or event.char.isalpha()):
            if len(self.selection) < 3:
                self.selection += event.char.upper()
                self._redraw_selection()

    def _on_key_policy_entry(self, event):
        keysym = event.keysym
        if keysym == "Return":
            if self.policy_number:
                self.navigate("UN021")
            return
        if keysym == "F3":
            self.navigate("BACK")  # was EXIT (destroyed root) - BACK is a safe no-op if the nav stack is empty
            return
        if keysym == "F12":
            self.stage = "top"
            self.selection = ""
            self.render()
            return
        if keysym == "BackSpace":
            self.policy_number = self.policy_number[:-1]
            self.render()
            return
        if len(event.char) == 1 and (event.char.isdigit() or event.char.isalpha() or event.char == " "):
            if len(self.policy_number) < 11:
                self.policy_number += event.char
                self.render()
