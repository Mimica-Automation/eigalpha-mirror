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
