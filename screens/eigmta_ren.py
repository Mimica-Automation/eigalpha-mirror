"""EIGMTA-REN - Mid Term Changes (Endorsements) & Renewals Menu for EIG."""
from .menu import MenuScreen


class EIGMTA_REN(MenuScreen):
    subcode = "EIGMTA-REN"
    title = "Mid Term Changes (Endorsements) & Renewals Menu for EIG"
    time_str = "11:02:58"

    options = [
        (1, "Mid Term Quotations"),
        (2, "Endorsements (Mid-term changes)"),
        (3, "Policy Renewal Review"),
        (4, "Policy Renewal"),
        (5, "Policy Renewal Adjustments"),
        (6, "Individual Policy Revision List"),
    ]
    option_rows = [5, 7, 10, 12, 14, 16]
    routes = {
        3: "UN034",
    }
    initial_selection = ""

    def render(self):
        super().render()
        from .base import COLS
        centered = self.title
        row2_col = (COLS - len(" ".join(centered))) // 2
        self.write(2, 0, " " * COLS, tag="green")
        self.write(2, row2_col, " ".join(centered), tag="green")
