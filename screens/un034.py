"""UN034 - Renewal review KEY DATA (POL-RENREV)."""
from .base import TerminalScreen, spaced, COLS


class UN034(TerminalScreen):
    def __init__(self, master, navigate, back_target: str | None = None, **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.back_target = back_target
        self.fields = {
            "pol_branch":  {"row": 6, "col": 30, "width": 2,  "value": "02"},
            "pol_type":    {"row": 6, "col": 37, "width": 3,  "value": "HHR"},
            "pol_num":     {"row": 6, "col": 45, "width": 6,  "value": "465469"},
            "insured":     {"row": 9, "col": 30, "width": 20, "value": ""},
            "client_name": {"row":12, "col": 30, "width": 20, "value": ""},
            "client_no":   {"row":15, "col": 30, "width":  7, "value": ""},
            "branch":      {"row":18, "col": 12, "width":  3, "value": ""},
            "product":     {"row":18, "col": 50, "width":  4, "value": ""},
            "endorsed":    {"row":21, "col": 45, "width":  1, "value": ""},
        }
        self.focused_field = "pol_num"
        self.cursor_pos = len(self.fields["pol_num"]["value"])
        self.render()

    def render(self):
        self.clear()
        self.draw_header("UN034", date_str="24/04/26", time_str="11:03:00")

        self.write(2, 0, "Renewal review", tag="green")
        title = spaced("KEY DATA")
        self.write(2, (COLS - len(title)) // 2, title, tag="green")

        self.write(4, 4, "To obtain a specific policy you may enter one of the following fields :-", tag="green")

        self.write(6,  10, "Policy number . .", tag="green")
        self.write(6,  33, "+", tag="green")
        self.write(6,  41, "+", tag="green")
        self.write(6,  55, "( Blank = policies for all", tag="green")
        self.write(7,  55, "                 branches )", tag="green")
        self.write(8,   4, "OR", tag="green")
        self.write(9,  10, "Insured name . . .", tag="green")
        self.write(11,  4, "OR", tag="green")
        self.write(12, 10, "Client name . . .", tag="green")
        self.write(14,  4, "OR", tag="green")
        self.write(15, 10, "Client number . .", tag="green")

        self.write(17, 4, "To review by scroll screen enter the branch and if you want to review", tag="green")
        self.write(18, 4, "policies for a specific product within the branch - the product type", tag="green")
        self.write(19, 4, "Branch . :", tag="green")
        self.write(19, 17, "+", tag="green")
        self.write(19, 42, "Product . :", tag="green")
        self.write(19, 56, "+", tag="green")

        self.write(20, 4, "Enter an X in the next field if you wish to see only policies that have been", tag="green")
        self.write(21, 4, "endorsed since entering the renewal cycle . :", tag="green")

        self._reposition_fields()
        self._draw_fields()

        self.write(22, 2,  "F3=Exit",     tag="cyan")
        self.write(22, 14, "F4=Prompt",   tag="cyan")
        self.write(22, 26, "F12=Previous",tag="cyan")
        self.write(23, 0, "POL-RENREV", tag="green")

    def _reposition_fields(self):
        self.fields["branch"]["row"] = 19
        self.fields["branch"]["col"] = 15
        self.fields["product"]["row"] = 19
        self.fields["product"]["col"] = 54
        self.fields["endorsed"]["row"] = 21
        self.fields["endorsed"]["col"] = 50

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
            self.navigate("UN021")
            return
        if keysym == "F3":
            self.navigate("BACK")  # was EXIT (destroyed root) - BACK is a safe no-op if the nav stack is empty
            return
        if keysym == "F12" and self.back_target:
            self.navigate(self.back_target)
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
        self.render()
