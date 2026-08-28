"""IN001 - SUPER INQUIRY screen."""
from .base import TerminalScreen, spaced, COLS


class IN001(TerminalScreen):
    """Super Inquiry: user types policy fields, presses Enter to jump to UN021."""

    def __init__(self, master, navigate, **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.fields = {
            "name":         {"row": 4, "col": 30, "width": 24, "value": ""},
            "dob":          {"row": 4, "col": 68, "width": 11, "value": ""},
            "phone":        {"row": 5, "col": 30, "width": 24, "value": ""},
            "ss":           {"row": 5, "col": 68, "width": 11, "value": ""},
            "postcode":     {"row": 6, "col": 30, "width": 5,  "value": ""},
            "address":      {"row": 6, "col": 68, "width": 11, "value": ""},
            "pol_branch":   {"row": 9, "col": 30, "width": 2,  "value": "02"},
            "pol_type":     {"row": 9, "col": 37, "width": 3,  "value": "HHR"},
            "pol_num":      {"row": 9, "col": 45, "width": 6,  "value": "000001"},
            "prev_policy":  {"row":10, "col": 30, "width": 20, "value": "GBS"},
            "risk_index":   {"row":11, "col": 30, "width": 13, "value": ""},
            "policy_status":{"row":11, "col": 68, "width": 1,  "value": ""},
            "locality":     {"row":12, "col": 30, "width": 13, "value": ""},
            "postcode2":    {"row":12, "col": 68, "width": 5,  "value": ""},
            "claim":        {"row":14, "col": 30, "width": 14, "value": ""},
            "client":       {"row":16, "col": 30, "width": 6,  "value": "680391"},
            "agent_branch": {"row":18, "col": 30, "width": 2,  "value": "CY"},
            "agent_num":    {"row":18, "col": 37, "width": 6,  "value": "121020"},
        }
        self.focused_field = "prev_policy"
        self.cursor_pos = 0
        self.render()

    def render(self):
        self.clear()
        self.draw_header("IN001", date_str="22/04/26", time_str="15:32")

        title = spaced("SUPER INQUIRY")
        self.write(2, (COLS - len(title)) // 2, title, tag="green")

        self.write(4, 14, "Name . . .", tag="green")
        self.write(4, 55, "AND/OR DOB . . .", tag="green")
        self.write(5, 8,  "OR  Phone no . .", tag="green")
        self.write(5, 55, "OR SS number . .", tag="green")
        self.write(6, 14, "Postcode . .", tag="green")
        self.write(6, 36, "+", tag="green")
        self.write(6, 55, "AND address . .", tag="green")

        self.write(7,  0, " " * COLS, tag="hl_cyanpanel")
        title_bp = "Branch & policy status filter permitted"
        self.write(7, (COLS - len(title_bp)) // 2, title_bp, tag="hl_cyanbox")

        self.write(9,  10, "I+ Policy . . .", tag="green")
        self.write(9,  33, "+", tag="green")
        self.write(9,  41, "+", tag="green")
        self.write(10, 10, "Prev policy no .", tag="green")
        self.write(11, 10, "Risk index . . .", tag="green")
        self.write(11, 55, "Policy status . :", tag="green")
        self.write(12, 10, "Locality . . . .", tag="green")
        self.write(12, 55, "Postcode . . . .", tag="green")
        self.write(12, 74, "+", tag="green")

        self.write(14, 14, "Claim . . .", tag="green")
        self.write(16, 14, "Client . . .", tag="green")
        self.write(18, 14, "Agent . . .",  tag="green")
        self.write(18, 33, "+", tag="green")

        self.write(19, COLS - 20, "Enter = Policy", tag="cyan")

        self.write(21, 20, " Roll keys ", tag="hl_cyanbox")
        self.write(22, 20, " Move box  ", tag="hl_cyanbox")

        self.write(21, 36, "F2=Policy",    tag="cyan")
        self.write(21, 52, "F5=Claim",     tag="cyan")
        self.write(21, 66, "F6=Client",    tag="cyan")
        self.write(22, 2,  "F3/12=Exit",   tag="cyan")
        self.write(22, 36, "F7=Agent",     tag="cyan")
        self.write(22, 52, "F8=Debtors",   tag="cyan")
        self.write(22, 66, "F9=Diary",     tag="cyan")
        self.write(23, 2,  "F4=Prompt",    tag="cyan")
        self.write(23, 36, "F10=Referrals",tag="cyan")

        self._draw_fields()

    def _draw_fields(self):
        for key, f in self.fields.items():
            val = (f["value"] + " " * f["width"])[:f["width"]]
            base_tag = "input"
            display = val.replace(" ", "_") if not f["value"] else f["value"].ljust(f["width"], "_")
            self.write(f["row"], f["col"], display, tag=base_tag)
        if self.focused_field:
            f = self.fields[self.focused_field]
            pos = min(self.cursor_pos, f["width"] - 1)
            ch = (f["value"] + " " * f["width"])[pos]
            if ch == " ":
                ch = "_"
            self.paint(f["row"], f["col"] + pos, 1, "cursor")

    def _on_key(self, event):
        keysym = event.keysym
        if keysym == "Return":
            self.navigate("UN021")
            return
        if keysym == "F3":
            self.navigate("EXIT")
            return
        if keysym == "F12":
            self.navigate("BACK")
            return
        if keysym == "F9":
            return
        if self.focused_field is None:
            return
        f = self.fields[self.focused_field]
        if keysym == "BackSpace":
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                f["value"] = f["value"][:self.cursor_pos] + f["value"][self.cursor_pos+1:]
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
                val = val[:self.cursor_pos] + event.char + val[self.cursor_pos+1:]
                f["value"] = val.rstrip()
                if self.cursor_pos < f["width"] - 1:
                    self.cursor_pos += 1
        self._draw_fields()
