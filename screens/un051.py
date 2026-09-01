"""UN051 - HOUSEHOLD OPTION DETAIL (POL-HHOLD).

Reached from UN050 (RISK SELECTION) when the Household option field holds
"1" and Enter is pressed. Covers the "Review Household Option in Risk
Selection" macro: situation address number, security alarm description
(e.g. "RD1"), alarm signalling method date, full value / sum insured, and an
"Auto Rate" action that fills in a computed (dummy) premium.

F4 on the alarm fields is a lightweight stand-in for the real "prompt"
popup (shows a one-line hint of valid codes inline rather than a full
overlay window - decorative only, matches the level of the rest of this
mirror). F2=Update commits and returns to UN050 (mirrors "Select Update").
F3=Exit, F12=Previous also return to UN050.
"""
from .base import TerminalScreen, spaced, COLS
from .dummy_data import DEFAULT_POLICY, DEFAULT_HOUSEHOLD

_ALARM_HINT = "Valid codes: RD1=Remote Dual Path  RS1=Remote Single Path  NA=None"
_DATE_HINT = "Enter signalling method effective date as DD/MM/YY"


class UN051(TerminalScreen):
    def __init__(self, master, navigate, policy=None, household=None,
                 back_target: str | None = "UN050", **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.policy = policy or dict(DEFAULT_POLICY)
        self.back_target = back_target

        values = household if household is not None else dict(DEFAULT_HOUSEHOLD)
        self.fields = {
            "situation_address_num":  {"row": 6,  "col": 40, "width": 2,  "value": values.get("situation_address_num", "")},
            "security_alarm_desc":    {"row": 8,  "col": 40, "width": 3,  "value": values.get("security_alarm_desc", "")},
            "alarm_signalling_date":  {"row": 10, "col": 40, "width": 8,  "value": values.get("alarm_signalling_date", "")},
            "full_value_sum_insured": {"row": 12, "col": 40, "width": 10, "value": values.get("full_value_sum_insured", "")},
        }
        self.auto_rated_premium = values.get("auto_rated_premium", "")

        self.focused_field = "situation_address_num"
        self.cursor_pos = len(self.fields["situation_address_num"]["value"])
        self.hint = ""
        self.render()

    # ------------------------------------------------------------------
    def render(self):
        self.clear()
        p = self.policy
        self.draw_header("UN051", date_str="24/04/26", time_str="11:22")

        self.write(2, 0, "Risk selection", tag="green")
        title = spaced("HOUSEHOLD OPTION DETAIL")
        self.write(2, (COLS - len(title)) // 2, title, tag="green")
        self.write(3, 0, "_" * COLS, tag="green")

        self.write(4, 0, "Policy . :", tag="green")
        self.write(4, 11, f"{p['policy_branch']} {p['policy_type']} {p['policy_num']}  {p['policy_desc']}", tag="white")

        self.write(6,  8, "Situation address number . . . . . . :", tag="green")
        self.write(8,  8, "Security alarm description . . . . . :", tag="green")
        self.write(10, 8, "Alarm signalling method (eff. date) .:", tag="green")
        self.write(12, 8, "Full value / sum insured . . . . . . :", tag="green")

        self._draw_fields()

        self.write(14, 8, "Auto Rate", tag="hl_green")
        self.write(14, 20, "premium . . . :", tag="green")
        self.write(14, 36, self.auto_rated_premium or "(not rated)", tag="white" if self.auto_rated_premium else "yellow")

        if self.hint:
            self.write(17, 4, self.hint, tag="yellow")

        self.write(22, 2,  "F2=Update",  tag="cyan")
        self.write(22, 13, "F3=Exit",    tag="cyan")
        self.write(22, 23, "F4=Prompt",  tag="cyan")
        self.write(22, 34, "F6=Auto Rate", tag="cyan")
        self.write(22, 47, "F12=Previous", tag="cyan")
        self.write(23, 0,  "POL-HHOLD", tag="green")

    def _draw_fields(self):
        for key, f in self.fields.items():
            val = f["value"].ljust(f["width"], "_")
            self.write(f["row"], f["col"], val, tag="input")
        if self.focused_field:
            f = self.fields[self.focused_field]
            pos = min(self.cursor_pos, f["width"] - 1)
            self.paint(f["row"], f["col"] + pos, 1, "cursor")

    # ------------------------------------------------------------------
    def _on_key(self, event):
        keysym = event.keysym

        if keysym == "F3":
            self.navigate("EXIT")
            return
        if keysym == "F12":
            if self.back_target:
                self.navigate(self.back_target)
            return
        if keysym == "F2":
            self.hint = "Updated."
            self.render()
            return
        if keysym == "F6":
            sum_insured = self.fields["full_value_sum_insured"]["value"] or "150,000"
            self.auto_rated_premium = "1,148.60"
            self.hint = f"Auto-rated on sum insured {sum_insured}."
            self.render()
            return
        if keysym == "F4":
            if self.focused_field == "security_alarm_desc":
                self.hint = _ALARM_HINT
            elif self.focused_field == "alarm_signalling_date":
                self.hint = _DATE_HINT
            else:
                self.hint = ""
            self.render()
            return
        if keysym == "Return":
            self.hint = ""
            self.render()
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
