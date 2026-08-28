"""UN053 - POST POLICY ADJUSTMENTS (POL-POSTADJ).

Covers the "Post Policy Adjustments" macro - a short confirm/post flow
rather than a full screen of fields, per the task brief ("a single screen
with a short pop-up-style confirmation dialog is enough, don't over-build").

The recording's F6 keypress means two different things depending on where
in the flow it lands ("Abandon Target Shortcut (F6)" then later "Swap Modes
Shortcut (F6)") - this is modelled as real 3270-style context-sensitive
function keys: self.mode switches between "adjustment" and "policy", and
the F6 label/action (and the rest of the footer) changes to match, redrawn
each time.

Flow implemented:
  F7=Post Adjustments  -> opens a Yes/No confirmation pop-up
  Enter (while pop-up shown) = "Ok in Pop Up Message" -> dismiss, mark posted
  F3=Update & Exit     -> commits current mode, re-renders (stays put -
                           the recording calls this twice, at adjustment
                           and policy level)
  Shift+F2              -> jump back into UN052 (Adj Calc) mid-flow
  F6                    -> "Abandon Target" in adjustment mode (discards the
                           pending adjustment, stays here) / "Swap Modes" in
                           policy mode (flips mode adjustment<->policy)
  F5=End Policy         -> switches to policy mode
  F2=Post               -> posts the policy-level adjustments (only
                           meaningful in policy mode, after End Policy)
  F3(final)/F9=Next     -> once posted, exits onward to UN054 (Submit Policy
                           Renewal Review / Selection Panel)
"""
from .base import TerminalScreen, spaced, COLS
from .dummy_data import DEFAULT_POLICY


class UN053(TerminalScreen):
    def __init__(self, master, navigate, policy=None,
                 back_target: str | None = "UN052", **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.policy = policy or dict(DEFAULT_POLICY)
        self.back_target = back_target

        self.mode = "adjustment"   # "adjustment" | "policy"
        self.popup = False
        self.adjustments_posted = False
        self.policy_posted = False
        self.status = ""
        self.render()

    # ------------------------------------------------------------------
    def render(self):
        self.clear()
        p = self.policy
        self.draw_header("UN053", date_str="24/04/26", time_str="11:30")

        self.write(2, 0, "Renewal review", tag="green")
        title = spaced("POST POLICY ADJUSTMENTS")
        self.write(2, (COLS - len(title)) // 2, title, tag="green")
        self.write(3, 0, "_" * COLS, tag="green")

        self.write(4, 0, "Policy . :", tag="green")
        self.write(4, 11, f"{p['policy_branch']} {p['policy_type']} {p['policy_num']}  {p['policy_desc']}", tag="white")

        self.write(6, 4, f"Mode . . . . . . . . :", tag="green")
        self.write(6, 27, "POLICY" if self.mode == "policy" else "ADJUSTMENT", tag="cyan")

        self.write(8, 4, "Adjustments posted . :", tag="green")
        self.write(8, 27, "YES" if self.adjustments_posted else "NO", tag="hl_green" if self.adjustments_posted else "yellow")
        self.write(9, 4, "Policy posted  . . . :", tag="green")
        self.write(9, 27, "YES" if self.policy_posted else "NO", tag="hl_green" if self.policy_posted else "yellow")

        if self.popup:
            self._render_popup()

        if self.status:
            self.write(17, 4, self.status, tag="yellow")

        self._render_footer()
        self.write(23, 0, "POL-POSTADJ", tag="green")

    def _render_popup(self):
        box_row = 12
        self.write(box_row, 20, " " * 40, tag="hl_cyanpanel")
        self.write(box_row + 1, 20, " Post adjustments for this policy?     ", tag="hl_cyanpanel")
        self.write(box_row + 2, 20, " Press Enter for OK                    ", tag="hl_cyanpanel")
        self.write(box_row + 3, 20, " " * 40, tag="hl_cyanpanel")

    def _render_footer(self):
        if self.popup:
            self.write(22, 2, "Enter=Ok", tag="cyan")
            return

        self.write(22, 2,  "F7=Post Adjustments", tag="cyan")
        self.write(22, 23, "F3=Update & Exit",    tag="cyan")
        self.write(22, 41, "Shift+F2=Adj Calc",   tag="cyan")

        if self.mode == "adjustment":
            self.write(22, 60, "F6=Abandon Target", tag="cyan")
        else:
            self.write(22, 60, "F6=Swap Modes", tag="cyan")

        self.write(23, 12, "F5=End Policy", tag="cyan")
        self.write(23, 27, "F2=Post",       tag="cyan")
        if self.policy_posted:
            self.write(23, 37, "F9=Next", tag="cyan")

    # ------------------------------------------------------------------
    def _on_key(self, event):
        keysym = event.keysym

        if self.popup:
            if keysym == "Return":
                self.popup = False
                self.adjustments_posted = True
                self.status = "Adjustments posted."
                self.render()
            return

        if keysym == "F7":
            self.popup = True
            self.render()
            return
        if keysym == "F3":
            self.status = f"{self.mode.capitalize()} level updated."
            self.render()
            return
        if keysym in ("Shift_F2", "F14"):
            self.navigate("UN052")
            return
        if keysym == "F6":
            if self.mode == "adjustment":
                self.adjustments_posted = False
                self.status = "Target abandoned."
            else:
                self.mode = "adjustment"
                self.status = "Swapped to adjustment mode."
            self.render()
            return
        if keysym == "F5":
            self.mode = "policy"
            self.status = "Policy ended for this adjustment cycle."
            self.render()
            return
        if keysym == "F2":
            if self.mode == "policy" and self.adjustments_posted:
                self.policy_posted = True
                self.status = "Policy adjustments posted."
            else:
                self.status = "Nothing to post yet."
            self.render()
            return
        if keysym in ("F9",) and self.policy_posted:
            self.navigate("UN054")
            return
        if keysym == "F12":
            if self.back_target:
                self.navigate(self.back_target)
            return
