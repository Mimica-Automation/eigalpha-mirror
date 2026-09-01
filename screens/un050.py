"""UN050 - RISK SELECTION (POL-RISKSEL).

Covers the recorded "Review <X> Option in Risk Selection" macros: the
recording repeatedly re-enters this same screen and writes "1" into one
coverage-option field at a time (Fine Art, BUS L/CV, Engineer CMD, GEN COVR,
TRAVEL TR1), then Exits/re-Enters for the next option - so this is modelled
as ONE screen with a flat list of toggle fields rather than one screen per
option.

Household is the one option with a real sub-screen behind it (situation
address / security alarm / sum insured / auto-rate) - selecting it (value
"1" + Enter while focused on that field) navigates to UN051 instead of just
toggling in place.

Field-entry pattern follows UN034/UN045: a flat dict of fields with
row/col/width/value, Tab cycles focus, arrow keys move the cursor, typed
characters overwrite in place. F2=Update commits the toggles in place
(covers the "Update Renewal Review" / "Update Policy Clauses" / "Update Risk
Statistics" macros, which are all just Enter+F2 after a coverage field edit
- folded into this screen rather than built as separate screens). F9=Post
moves on to UN052 (ADJUSTMENT CALC), covering the "Select Post" action that
follows the clause updates. F3=Exit, F12=Previous (back to whatever screen
routed here - out of scope for this task, e.g. UN045/UN021).
"""
from .base import TerminalScreen, spaced, COLS
from .dummy_data import DEFAULT_POLICY, DEFAULT_RISK_OPTIONS, RISK_OPTION_LABELS

_FIELD_ROW_START = 6
_FIELD_ROW_STEP = 2
_LABEL_COL = 8
_FIELD_COL = 40


class UN050(TerminalScreen):
    def __init__(self, master, navigate, policy=None, risk_options=None,
                 back_target: str | None = None, **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.policy = policy or dict(DEFAULT_POLICY)
        self.back_target = back_target

        values = risk_options if risk_options is not None else dict(DEFAULT_RISK_OPTIONS)
        self.fields = {}
        for i, (key, _label) in enumerate(RISK_OPTION_LABELS):
            self.fields[key] = {
                "row": _FIELD_ROW_START + i * _FIELD_ROW_STEP,
                "col": _FIELD_COL,
                "width": 1,
                "value": values.get(key, ""),
            }

        self.focused_field = RISK_OPTION_LABELS[0][0]
        self.cursor_pos = 0
        self.status = ""
        self.render()

    # ------------------------------------------------------------------
    def render(self):
        self.clear()
        p = self.policy
        self.draw_header("UN050", date_str="24/04/26", time_str="11:20")

        self.write(2, 0, "Renewal review", tag="green")
        title = spaced("RISK SELECTION")
        self.write(2, (COLS - len(title)) // 2, title, tag="green")
        self.write(3, 0, "_" * COLS, tag="green")

        self.write(4, 0, "Policy . :", tag="green")
        self.write(4, 11, f"{p['policy_branch']} {p['policy_type']} {p['policy_num']}  {p['policy_desc']}", tag="white")

        for i, (key, label) in enumerate(RISK_OPTION_LABELS):
            row = _FIELD_ROW_START + i * _FIELD_ROW_STEP
            dots = "." * (_FIELD_COL - _LABEL_COL - len(label) - 1)
            self.write(row, _LABEL_COL, f"{label} {dots}", tag="green")

        self._draw_fields()

        if self.status:
            self.write(19, 4, self.status, tag="yellow")

        self.write(21, 4, "Enter '1' against an option to select it; Enter on Household opens its detail screen.", tag="green")

        self.write(22, 2,  "F2=Update",   tag="cyan")
        self.write(22, 14, "F3=Exit",     tag="cyan")
        self.write(22, 24, "F9=Post",     tag="cyan")
        self.write(22, 34, "F12=Previous", tag="cyan")
        self.write(23, 0,  "POL-RISKSEL", tag="green")

    def _draw_fields(self):
        for key, f in self.fields.items():
            val = f["value"].ljust(f["width"], "_")
            tag = "hl_green" if f["value"] == "1" else "input"
            self.write(f["row"], f["col"], val, tag=tag)
        if self.focused_field:
            f = self.fields[self.focused_field]
            pos = min(self.cursor_pos, f["width"] - 1)
            self.paint(f["row"], f["col"] + pos, 1, "cursor")

    # ------------------------------------------------------------------
    def _on_key(self, event):
        keysym = event.keysym

        if keysym == "F3":
            self.navigate("BACK")  # was EXIT (destroyed root) - BACK is a safe no-op if the nav stack is empty
            return
        if keysym == "F12":
            if self.back_target:
                self.navigate(self.back_target)
            return
        if keysym == "F2":
            self.status = "Updated."
            self.render()
            return
        if keysym == "F9":
            self.status = ""
            self.navigate("UN052")
            return

        if self.focused_field is None:
            return
        f = self.fields[self.focused_field]

        if keysym == "Return":
            if self.focused_field == "household" and f["value"] == "1":
                self.navigate("UN051")
                return
            self.status = f"{dict(RISK_OPTION_LABELS)[self.focused_field]} option reviewed."
            self.render()
            return
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
