"""UN045 - ENDORSEMENT PROCESSING (POL-ENDORSE).

Reached from UN021 (POLICY HEADER) via Enter - covers the "Review Endorsement"
macro step: operator picks whether they are reviewing Policy Renewal
Adjustments or Endorsements, keys a "Number in Selection", then enters the
Effective Date / Period of Cover / Ren fields for the adjustment before
returning to the policy header.

Field-entry pattern follows UN034 exactly: a flat dict of fields with
row/col/width/value, Tab cycles focus, arrow keys move the cursor within a
field, typed characters overwrite in place, Enter submits/navigates onward,
F3=Exit, F12=Previous (back to UN021).
"""
from .base import TerminalScreen, spaced, COLS

_BLANK_POLICY = {
    "policy_branch": "02",
    "policy_type": "HHR",
    "policy_num": "0000001",
    "policy_desc": "Sample Contents Cover",
}


class UN045(TerminalScreen):
    def __init__(self, master, navigate, policy=None, back_target: str | None = None, **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.policy = policy or _BLANK_POLICY
        self.back_target = back_target

        self.fields = {
            "pra_flag":            {"row": 7,  "col": 48, "width": 1, "value": ""},
            "endorsements_flag":   {"row": 8,  "col": 48, "width": 1, "value": ""},
            "number_in_selection": {"row": 10, "col": 48, "width": 2, "value": ""},
            "effective_date":      {"row": 13, "col": 48, "width": 8, "value": ""},
            "period_from":         {"row": 14, "col": 48, "width": 8, "value": ""},
            "period_to":           {"row": 14, "col": 60, "width": 8, "value": ""},
            "ren_code":            {"row": 15, "col": 48, "width": 2, "value": "02"},
        }
        self.focused_field = "number_in_selection"
        self.cursor_pos = len(self.fields["number_in_selection"]["value"])
        self.render()

    def render(self):
        self.clear()
        p = self.policy
        self.draw_header("UN045", date_str="24/04/26", time_str="11:16")

        self.write(2, 0, "Policy adjustments", tag="green")
        title = spaced("ENDORSEMENT PROCESSING")
        self.write(2, (COLS - len(title)) // 2, title, tag="green")
        self.write(3, 0, "_" * COLS, tag="green")

        self.write(4, 0, "Policy . :", tag="green")
        self.write(4, 11, f"{p['policy_branch']} {p['policy_type']} {p['policy_num']}  {p['policy_desc']}", tag="white")

        self.write(6, 4, "Please select the type of adjustment required :-", tag="green")

        self.write(7,  4, "1. Policy Renewal Adjustments . . . . . :", tag="green")
        self.write(8,  4, "2. Endorsements . . . . . . . . . . . . :", tag="green")

        self.write(10, 4, "Number in Selection . . . . . . . . . . :", tag="green")

        self.write(13, 4, "Effective Date . . . . . . . . . . . . . :", tag="green")
        self.write(14, 4, "Period of Cover . . . . . . . . . . . . . :", tag="green")
        self.write(14, 57, "To", tag="green")
        self.write(15, 4, "Ren . . . . . . . . . . . . . . . . . . . :", tag="green")

        self._draw_fields()

        self.write(22, 2,  "F3=Exit",      tag="cyan")
        self.write(22, 14, "F12=Previous", tag="cyan")
        self.write(23, 0,  "POL-ENDORSE",  tag="green")

    def _draw_fields(self):
        for key, f in self.fields.items():
            val = f["value"].ljust(f["width"], "_")
            self.write(f["row"], f["col"], val, tag="input")
        if self.focused_field:
            f = self.fields[self.focused_field]
            pos = min(self.cursor_pos, f["width"] - 1)
            self.paint(f["row"], f["col"] + pos, 1, "cursor")

    def _on_key(self, event):
        keysym = event.keysym
        if keysym == "Return":
            if self.fields["pra_flag"]["value"].strip():
                self.navigate("UN050")
            else:
                self.navigate("UN021")
            return
        if keysym == "F3":
            self.navigate("BACK")  # was EXIT (destroyed root) - BACK is a safe no-op if the nav stack is empty
            return
        if keysym == "F12":
            if self.back_target:
                self.navigate(self.back_target)
            else:
                self.navigate("UN021")
            return
        if self.focused_field is None:
            return
        f = self.fields[self.focused_field]
        if keysym == "BackSpace":
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                f["value"] = f["value"][:self.cursor_pos] + f["value"][self.cursor_pos + 1:]
        elif keysym == "Left":
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
        elif keysym == "Right":
            if self.cursor_pos < f["width"] - 1:
                self.cursor_pos += 1
        elif keysym == "Tab":
            keys = list(self.fields.keys())
            i = keys.index(self.focused_field)
            self.focused_field = keys[(i + 1) % len(keys)]
            self.cursor_pos = 0
        elif len(event.char) == 1 and event.char.isprintable():
            if self.cursor_pos < f["width"]:
                val = (f["value"] + " " * f["width"])[:f["width"]]
                val = val[:self.cursor_pos] + event.char + val[self.cursor_pos + 1:]
                f["value"] = val.rstrip()
                if self.cursor_pos < f["width"] - 1:
                    self.cursor_pos += 1
        self.render()
