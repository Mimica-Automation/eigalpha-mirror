"""UN489 - LIST OF REVISION LIST AUDIT MESSAGES."""
from .base import TerminalScreen, COLS


class UN489(TerminalScreen):
    def __init__(self, master, navigate, policy, **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.policy = policy
        self.render()

    def render(self):
        self.clear()
        p = self.policy
        self.draw_header("UN489", date_str="22/04/26", time_str="15:34")

        title = f"LIST OF REVISION LIST AUDIT MESSAGES FOR POLICY . : {p['policy_branch']} {p['policy_type']} {p['policy_num']}"
        self.write(2, 0, title, tag="green")
        self.write(3, 0, "_" * COLS, tag="green")

        self.write(6, 0, "Loc  Rsk  Pcl  Sev  Message", tag="green")

        for i, m in enumerate(p["audit_messages"]):
            row = 7 + i
            line = f"{m['loc']:<4} {m['rsk']:<4} {m['pcl']:<4} {m['sev']:<4} {m['message']}"
            self.write(row, 0, line, tag="green")

        self.write(21, COLS - 6, "Bottom", tag="green")
        self.write(23, 0, "F12=Previous", tag="cyan")

    def _on_key(self, event):
        if event.keysym == "F3":
            self.navigate("BACK")  # was EXIT (destroyed root) - BACK is a safe no-op if the nav stack is empty
        elif event.keysym == "F12":
            self.navigate("BACK")
