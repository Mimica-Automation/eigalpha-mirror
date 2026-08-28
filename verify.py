"""Headless verification: instantiate app, drive keys, assert navigation and content."""
import os
import sys
import tkinter as tk
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import ProClientApp


def ev(keysym, char=""):
    return SimpleNamespace(keysym=keysym, char=char)


def digit(d):
    return SimpleNamespace(keysym=d, char=d)


def dump(w):
    return w.text.get("1.0", "end-1c")


def screen_name(app):
    return type(app.current_screen).__name__


def main():
    root = tk.Tk(); root.withdraw()
    app = ProClientApp(root); root.update_idletasks()

    assert screen_name(app) == "MASTERMENU"
    body = dump(app.current_screen)
    compact = body.replace(" ", "")
    assert "INSUREPLUS" in compact, "MASTERMENU title missing"
    assert "Underwriting"       in body
    assert "Cash"                in body
    assert "Special Functions"   in body
    assert "Inquiry Menu"        in body
    assert "Reprint Selected Notices" in body
    print("[ok] MASTERMENU rendered")

    app.current_screen._on_key(digit("1"))
    app.current_screen._on_key(ev("Return"))
    root.update_idletasks()
    assert screen_name(app) == "EIGMTA_REN"
    body = dump(app.current_screen); compact = body.replace(" ", "")
    assert "MidTermQuotations"       in compact
    assert "Endorsements"            in body
    assert "PolicyRenewalReview"     in compact
    assert "IndividualPolicyRevisionList" in compact
    print("[ok] MASTERMENU + 1 -> EIGMTA-REN")

    app.current_screen._on_key(digit("3"))
    app.current_screen._on_key(ev("Return"))
    root.update_idletasks()
    assert screen_name(app) == "UN034"
    body = dump(app.current_screen); compact = body.replace(" ", "")
    assert "Renewalreview" in compact
    assert "KEYDATA"       in compact
    assert "POL-RENREV"    in body
    assert "465469"        in body
    print("[ok] EIGMTA-REN + 3 -> UN034")

    app.current_screen._on_key(ev("Return"))
    root.update_idletasks()
    assert screen_name(app) == "UN021"
    body = dump(app.current_screen)
    assert "POLICY HEADER"  in body
    assert "0000001"    in body
    assert "Mr J Doe"   in body
    print("[ok] UN034 Enter -> UN021")

    app.current_screen._on_key(ev("F9"))
    root.update_idletasks()
    assert screen_name(app) == "UN489"
    body = dump(app.current_screen)
    assert "Subject to Survey Clause H0054 exists"        in body
    assert "Renewal method (02) requires manual review"   in body
    print("[ok] UN021 F9 -> UN489")

    app.current_screen._on_key(ev("F12"))
    root.update_idletasks()
    assert screen_name(app) == "UN021", "F12 from UN489 should return to UN021"
    print("[ok] UN489 F12 -> UN021")

    app.current_screen._on_key(ev("F12"))
    root.update_idletasks()
    assert screen_name(app) == "UN034", "F12 from UN021 should return to UN034"
    print("[ok] UN021 F12 -> UN034")

    app.current_screen._on_key(ev("F12"))
    root.update_idletasks()
    assert screen_name(app) == "EIGMTA_REN"
    app.current_screen._on_key(ev("F12"))
    root.update_idletasks()
    assert screen_name(app) == "MASTERMENU"
    print("[ok] F12 chain back to MASTERMENU")

    app.current_screen._on_key(digit("4"))
    app.current_screen._on_key(ev("Return"))
    root.update_idletasks()
    assert screen_name(app) == "INQUIRYS"
    body = dump(app.current_screen); compact = body.replace(" ", "")
    assert "SuperInquiry" in compact
    assert "PolicyInquiry" in compact
    assert "Campaign/AdvertInquiry" in compact
    print("[ok] MASTERMENU + 4 -> INQUIRYS")

    app.current_screen._on_key(digit("1"))
    app.current_screen._on_key(ev("Return"))
    root.update_idletasks()
    assert screen_name(app) == "IN001"
    body = dump(app.current_screen); compact = body.replace(" ", "")
    assert "SUPERINQUIRY" in compact
    print("[ok] INQUIRYS + 1 -> IN001")

    app.current_screen._on_key(ev("Return"))
    root.update_idletasks()
    assert screen_name(app) == "UN021"
    print("[ok] IN001 Enter -> UN021 (via INQUIRYS path)")

    app.current_screen._on_key(ev("F12"))
    root.update_idletasks()
    assert screen_name(app) == "IN001", "F12 from UN021 should go back to IN001 in this branch"
    app.current_screen._on_key(ev("F12"))
    root.update_idletasks()
    assert screen_name(app) == "INQUIRYS"
    app.current_screen._on_key(ev("F12"))
    root.update_idletasks()
    assert screen_name(app) == "MASTERMENU"
    print("[ok] F12 chain back to MASTERMENU (INQUIRYS branch)")

    def type_text(screen, text):
        for c in text:
            screen._on_key(SimpleNamespace(keysym=c, char=c))

    # -- UN045 / UN050-UN054 (renewal-adjustments + risk-selection continuation) --
    app.current_screen._on_key(digit("1")); app.current_screen._on_key(ev("Return")); root.update_idletasks()
    app.current_screen._on_key(digit("3")); app.current_screen._on_key(ev("Return")); root.update_idletasks()
    app.current_screen._on_key(ev("Return")); root.update_idletasks()
    assert screen_name(app) == "UN021"

    app.current_screen._on_key(ev("Return")); root.update_idletasks()
    assert screen_name(app) == "UN045", screen_name(app)
    print("[ok] UN021 Enter -> UN045")

    app.current_screen.focused_field = "endorsements_flag"
    app.current_screen.cursor_pos = 0
    type_text(app.current_screen, "1")
    app.current_screen._on_key(ev("Return")); root.update_idletasks()
    assert screen_name(app) == "UN021", f"expected UN021 (Path B route), got {screen_name(app)}"
    print("[ok] UN045 (endorsements route) Enter -> UN021 (Path B)")

    app.current_screen._on_key(ev("F8")); root.update_idletasks()
    assert app.current_screen.page == 2
    app.current_screen._on_key(ev("F2")); root.update_idletasks()
    assert app.current_screen.instalments_posted is True
    body = dump(app.current_screen)
    assert "Instalments posted." in body
    app.current_screen._on_key(ev("F7")); root.update_idletasks()
    assert app.current_screen.page == 1
    print("[ok] UN021 page2 F2 -> Post Instalments, F7 -> back to page 1")

    app.current_screen._on_key(ev("Return")); root.update_idletasks()
    app.current_screen.focused_field = "pra_flag"
    app.current_screen.cursor_pos = 0
    type_text(app.current_screen, "1")
    app.current_screen._on_key(ev("Return")); root.update_idletasks()
    assert screen_name(app) == "UN050", f"expected UN050 (Path A route), got {screen_name(app)}"
    print("[ok] UN045 (pra_flag route) Enter -> UN050 (Path A)")

    app.current_screen.focused_field = "household"
    app.current_screen.cursor_pos = 0
    type_text(app.current_screen, "1")
    app.current_screen._on_key(ev("Return")); root.update_idletasks()
    assert screen_name(app) == "UN051", screen_name(app)
    app.current_screen._on_key(ev("F12")); root.update_idletasks()
    assert screen_name(app) == "UN050", screen_name(app)
    print("[ok] UN050 <-> UN051 (household option)")

    app.current_screen._on_key(ev("F9")); root.update_idletasks()
    assert screen_name(app) == "UN052", screen_name(app)
    app.current_screen._on_key(ev("F3")); root.update_idletasks()
    assert screen_name(app) == "UN053", screen_name(app)
    print("[ok] UN050 F9 -> UN052 F3 -> UN053")

    app.current_screen._on_key(ev("F7")); root.update_idletasks()
    app.current_screen._on_key(ev("Return")); root.update_idletasks()
    app.current_screen._on_key(ev("F5")); root.update_idletasks()
    app.current_screen._on_key(ev("F2")); root.update_idletasks()
    app.current_screen._on_key(ev("F9")); root.update_idletasks()
    assert screen_name(app) == "UN054", screen_name(app)
    print("[ok] UN053 post-flow -> UN054")

    app.current_screen._on_key(digit("3")); app.current_screen._on_key(ev("Return")); root.update_idletasks()
    assert app.current_screen.stage == "policy_entry"
    type_text(app.current_screen, "02 HHR 0000001")
    app.current_screen._on_key(ev("Return")); root.update_idletasks()
    assert screen_name(app) == "UN021", screen_name(app)
    print("[ok] UN054 policy entry -> UN021")

    app.navigate("MASTERMENU")
    root.update_idletasks()
    assert screen_name(app) == "MASTERMENU", screen_name(app)
    print("[ok] reset to MASTERMENU for exit test")

    app.current_screen._on_key(ev("F3"))
    root.update_idletasks()
    try:
        root.winfo_exists(); alive = True
    except tk.TclError:
        alive = False
    assert not alive, "F3 on MASTERMENU should exit"
    print("[ok] MASTERMENU F3 -> exit")

    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
