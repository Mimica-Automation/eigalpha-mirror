"""MASTERMENU - INSURE PLUS top-level menu."""
from .menu import MenuScreen


class MASTERMENU(MenuScreen):
    subcode = "MASTERMENU"
    title = "INSURE PLUS"
    time_str = "11:02:56"

    options = [
        (1, "Underwriting"),
        (2, "Cash"),
        (3, "Special Functions"),
        (4, "Inquiry Menu"),
        (5, "Reprint Selected Notices"),
    ]
    option_rows = [5, 7, 9, 11, 15]
    routes = {
        1: "EIGMTA-REN",
        4: "INQUIRYS",
    }
    initial_selection = ""
