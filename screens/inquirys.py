"""INQUIRYS - Inquiry Menu."""
from .menu import MenuScreen
from .base import COLS


class INQUIRYS(MenuScreen):
    subcode = "INQUIRYS"
    title = "Inquiry Menu"
    time_str = "11:02:55"

    options = [
        (1,  "Super Inquiry           - ?"),
        (2,  "Policy Inquiry          - ?P"),
        (3,  "Locality Risk Exposure Inquiry"),
        (4,  "Payment History Inquiry"),
        (5,  "Receipt History Inquiry"),
        (6,  "Postcode Master Inquiry"),
        (7,  "Postcode Subsidence Inquiry"),
        (8,  "INDMTHD  - Indexation Methods Table Inquiry"),
        (9,  "Agent Inquiry"),
        (10, "Campaign/Advert Inquiry"),
    ]
    option_rows = [5, 6, 7, 9, 10, 12, 13, 14, 16, 18]
    routes = {
        1: "IN001",
    }
    initial_selection = ""
    selection_row = 20

    def render(self):
        super().render()
        title = self.title
        self.write(2, 0, " " * COLS, tag="green")
        self.write(2, 10, title, tag="green")
