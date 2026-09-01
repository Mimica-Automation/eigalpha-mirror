"""UN021 - POLICY HEADER screen.

Extended (on top of the original read-only UN021) to cover these additional
macro steps:

  * "Research and Submit Company's Location in System" - adds "Location
    option" and "Additional insureds" as two more fields inside the same
    F2 update overlay (appended after cmd/comment, not inserted between
    them, so Path B's existing cmd/comment-only flow is unaffected).

  * "Update Policy Header" - F2 (relabelled from the previously-unimplemented
    "F2=CMX" to "F2=Update") drops the screen into an inline edit mode with
    two free-text fields: a one-line "Cmd" field and a "Text" (header
    comment) field. Pressing F2 again while editing is the "Select Update"
    action: it commits both values back onto the policy record and
    re-renders the screen showing the committed text. F12 while editing
    cancels the edit instead of navigating back (F12's normal
    navigate-back-to-previous-screen behaviour is preserved outside of edit
    mode).

  * "Select Next Screen" - F8 pages to a second POLICY HEADER screen showing
    renewal instalment / payment detail, in the same visual style as page 1.
    F7 on page 2 pages back to page 1 ("Previous Screen").

Also adds: pressing Enter on page 1 (outside of edit mode) navigates onward
to UN045 (ENDORSEMENT PROCESSING), covering the "Review Endorsement" macro
step that follows Policy Header in the recorded process.

All previously-existing behaviour (F9=Referral Messages, F3=Exit,
F12=Previous) is unchanged.
"""
from .base import TerminalScreen, spaced, COLS


class UN021(TerminalScreen):
    def __init__(self, master, navigate, policy, **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.policy = policy

        # -- paging --
        self.page = 1
        self.instalments_posted = False

        # -- inline update ("F2=Update" / "Select Update") state --
        self.update_mode = False
        self.update_fields = {
            "cmd":     {"row": 16, "col": 27, "width": 10, "value": ""},
            "comment": {"row": 17, "col": 27, "width": 45, "value": ""},
            # Appended after cmd/comment (not inserted between them) so Path B's
            # existing flow - which only ever types into "cmd" then presses F2,
            # never Tabs - sees no behavior change. Covers the "Research and
            # Submit Company's Location in System" macro's Location Option /
            # Additional Insureds fields, reusing this same F2 overlay rather
            # than a new key binding.
            "location_option":   {"row": 19, "col": 27, "width": 2, "value": policy.get("location_option", "")},
            "additional_insureds_edit": {"row": 20, "col": 27, "width": 1, "value": ""},
        }
        self.update_focus = "cmd"
        self.update_cursor = 0

        self.render()

    # ------------------------------------------------------------------
    # rendering
    # ------------------------------------------------------------------
    def render(self):
        self.clear()
        p = self.policy
        self.draw_header("UN021", date_str="22/04/26", time_str="15:34")

        self.write(2, 0,  "POLICY HEADER", tag="green")
        self.write(2, 16, "Policy . :", tag="green")
        self.write(2, 27, f"{p['policy_branch']} {p['policy_type']} {p['policy_num']}  {p['policy_desc']}", tag="white")

        self.write(3, 0,  " AGENT  ", tag="hl_green")
        self.write(3, 16, "Client . :", tag="green")
        self.write(3, 27, f"{p['client_no']} {p['client_name']}", tag="white")

        self.write(4, 0,  " ACTIVE ", tag="hl_green")
        self.write(4, 16, "Agent  . :", tag="green")
        self.write(4, 27, f"{p['agent_no']} {p['agent_name']}", tag="white")

        if self.page == 1:
            self._render_page1()
        else:
            self._render_page2()

        if self.update_mode:
            self._render_update_overlay()

        self._render_footer()

    def _render_page1(self):
        p = self.policy
        self.write(5, 0,  f"Application received? {p['application_received']}", tag="green")

        self.write(6, 0,  "Name of insured . :", tag="green")
        self.write(6, 20, p["name_of_insured"], tag="white")
        self.write(6, 55, "Status   . :", tag="green")
        self.write(6, 68, p["status"], tag="white")

        self.write(7, 0,  "Pol.Booklet:", tag="green")
        self.write(7, 13, p["pol_booklet"], tag="white")
        self.write(7, 55, "Date     . :", tag="green")
        self.write(7, 68, p["status_date"], tag="white")

        self.write(8, 0,  " Addl insureds exist ", tag="hl_green")
        self.write(8, 25, "Additional insureds . .", tag="green")
        self.write(8, 49, p["additional_insureds"], tag="yellow")
        self.write(8, 51, "Broker pend flag . :", tag="green")
        self.write(8, 72, p["broker_pend_flag"] or " ", tag="white")

        self.write(9, 0,  "Period of cover  from", tag="green")
        self.write(9, 22, f"{p['period_from']} To {p['period_to']} At {p['period_at']}", tag="white")
        self.write(9, 57, "Renew for:", tag="green")
        self.write(9, 68, p["renew_for"], tag="white")

        self.write(10, 0, "Original incept date . :", tag="green")
        self.write(10, 25, p["original_incept"], tag="white")
        self.write(10, 42, "Replaces policy . :", tag="green")

        self.write(11, 0, "UW", tag="green")
        self.write(11, 4, p["uw_code"], tag="white")
        self.write(11, 8, p["uw_desc"], tag="green")
        self.write(11, 47, "Trans source:", tag="green")
        self.write(11, 61, p["trans_source"], tag="white")

        self.write(12, 0, "Comment . . . . . . . :", tag="green")
        comment = p.get("header_comment", "")
        self.write(12, 24, comment, tag="yellow" if comment else "white")

        self.write(13, 0, f"Ren {p['ren_code']}   {p['ren_desc']}", tag="green")

        self.write(14, 0, "Type of documents . :", tag="green")
        self.write(14, 22, p["type_of_docs_code"], tag="white")
        self.write(14, 27, p["type_of_docs_desc"], tag="green")

        self.write(15, 0, "Payment method . . :", tag="green")
        self.write(15, 21, p["payment_method_code"], tag="white")
        self.write(15, 26, p["payment_method_desc"], tag="green")
        self.write(15, 55, "No.instalments . :", tag="green")
        self.write(15, 74, p["no_instalments"], tag="white")

        if not self.update_mode:
            self.write(16, 0, "Last Cmd  . . . . . . :", tag="green")
            self.write(16, 24, p.get("cmd_last", ""), tag="white")

        self.write(19, 55, "Inst Bill Option . :", tag="cyan")
        self.write(19, 76, p["inst_bill_option"], tag="white")

        self.write(20, 16, "Coinsurance . :", tag="cyan")
        self.write(20, 32, p["coinsurance"], tag="white")
        self.write(20, 35, "Bus.Desc:", tag="cyan")
        self.write(20, 45, p["bus_desc"], tag="white")
        self.write(20, 48, "Blackboard . :", tag="cyan")
        self.write(20, 63, p["blackboard"], tag="yellow")
        self.write(20, 66, "Diary . :", tag="cyan")
        self.write(20, 76, p["diary"], tag="white")

        self.write(21, 0,  " Claims  ", tag="hl_green")
        self.write(21, 55, " Policy  ", tag="hl_cyanbox")
        self.write(21, 65, " B/Board ", tag="hl_green")

    def _render_page2(self):
        p = self.policy
        title = spaced("INSTALMENT / PAYMENT DETAIL")
        self.write(6, (COLS - len(title)) // 2, title, tag="green")
        self.write(6, 0, "Page 2", tag="cyan")

        self.write(8,  0, "Instalment plan . . . . . . :", tag="green")
        self.write(8,  30, p.get("instalment_plan", ""), tag="white")

        self.write(9,  0, "Instalment amount . . . . . :", tag="green")
        self.write(9,  30, p.get("instalment_amount", ""), tag="white")

        self.write(10, 0, "Next instalment due . . . . :", tag="green")
        self.write(10, 30, p.get("next_instalment_date", ""), tag="white")

        self.write(11, 0, "Instalments paid to date . . :", tag="green")
        self.write(11, 31, p.get("instalments_paid", ""), tag="white")

        self.write(12, 0, "Direct debit reference . . . :", tag="green")
        self.write(12, 31, p.get("dd_reference", ""), tag="white")

        self.write(13, 0, "Collection day . . . . . . . :", tag="green")
        self.write(13, 31, p.get("collection_day", ""), tag="white")

        if self.instalments_posted:
            self.write(15, 0, "Instalments posted.", tag="yellow")

    def _render_update_overlay(self):
        # Clear rows 16-20 first (they may have page1 content underneath -
        # "Last Cmd", "Inst Bill Option", "Coinsurance" etc.)
        for row in range(16, 21):
            self.write(row, 0, " " * COLS, tag="green")

        self.write(16, 0, "Cmd  . . . . . . . . . :", tag="cyan")
        self.write(17, 0, "Text . . . . . . . . . :", tag="cyan")
        self.write(19, 0, "Location option  . . . :", tag="cyan")
        self.write(20, 0, "Additional insureds  . :", tag="cyan")
        self.write(18, 0, "(Type text, TAB to switch field, F2=Select Update, F12=Cancel)", tag="yellow")

        for key, f in self.update_fields.items():
            val = f["value"].ljust(f["width"], "_")
            self.write(f["row"], f["col"], val, tag="input")

        f = self.update_fields[self.update_focus]
        pos = min(self.update_cursor, f["width"] - 1)
        self.paint(f["row"], f["col"] + pos, 1, "cursor")

    def _render_footer(self):
        if self.update_mode:
            self.write(22, 2,  "F2=Select Update", tag="cyan")
            self.write(22, 20, "F3=Exit",          tag="cyan")
            self.write(23, 2,  "F12=Cancel",       tag="cyan")
            return

        if self.page == 2:
            self.write(22, 2,  "F2=Post Instalments", tag="cyan")
            self.write(22, 24, "F3=Exit",             tag="cyan")
            self.write(22, 34, "F7=Previous Screen",  tag="cyan")
            self.write(23, 2,  "F12=Previous",        tag="cyan")
            return

        self.write(22, 2,  "F2=Update",         tag="cyan")
        self.write(22, 13, "F3=Exit",           tag="cyan")
        self.write(22, 22, "F5=Policy history", tag="cyan")
        self.write(22, 42, "F6=Quotation",      tag="cyan")
        self.write(22, 56, "F7=Letter",         tag="cyan")
        self.write(22, 67, "F8=Next Screen",    tag="cyan")

        self.write(23, 0,  "F9=Referral Messages", tag="cyan")
        self.write(23, 22, "F10=Last claim",       tag="cyan")
        self.write(23, 42, "F11=Case",             tag="cyan")
        self.write(23, 58, "F12=Previous",         tag="cyan")

    # ------------------------------------------------------------------
    # key handling
    # ------------------------------------------------------------------
    def _on_key(self, event):
        if self.update_mode:
            self._handle_update_key(event)
            return

        keysym = event.keysym
        if keysym == "F9":
            self.navigate("UN489")
        elif keysym == "F3":
            # "Select Exit" from POLICY HEADER returns to its immediate parent
            # menu (EIGMTA-REN) within the same session - matches the
            # recording: F3, then "Select Return to Menu" (Enter), then typing
            # "3" (Policy Renewal Review, EIGMTA-REN's own route to UN034) and
            # a policy number to land back on a fresh UN021. navigate("EXIT")
            # destroys the entire Tk root window instead, silently killing the
            # mirror mid-run whenever "Submitting the Policy Renewal Review"
            # pressed F3 here - and MASTERMENU (the top-level menu) isn't
            # right either: it has no route for "3", so the automation's next
            # keypresses would dead-end and its final F12 would hit
            # MASTERMENU's own back_target="EXIT", destroying root anyway.
            self.navigate("EIGMTA-REN")
        elif keysym == "F12":
            self.navigate("BACK")
        elif keysym == "F2" and self.page == 1:
            self._enter_update_mode()
        elif keysym == "F8" and self.page == 1:
            self.page = 2
            self.render()
        elif keysym == "F7" and self.page == 2:
            self.page = 1
            self.render()
        elif keysym == "F2" and self.page == 2:
            self.instalments_posted = True
            self.render()
        elif keysym == "Return" and self.page == 1:
            self.navigate("UN045")

    def _enter_update_mode(self):
        self.update_mode = True
        self.update_focus = "cmd"
        self.update_cursor = len(self.update_fields["cmd"]["value"])
        self.render()

    def _handle_update_key(self, event):
        keysym = event.keysym

        if keysym == "F2":
            # "Select Update": commit all fields back onto the policy record.
            self.policy["cmd_last"] = self.update_fields["cmd"]["value"]
            self.policy["header_comment"] = self.update_fields["comment"]["value"]
            self.policy["location_option"] = self.update_fields["location_option"]["value"]
            if self.update_fields["additional_insureds_edit"]["value"]:
                self.policy["additional_insureds"] = self.update_fields["additional_insureds_edit"]["value"]
            self.update_mode = False
            self.render()
            return
        if keysym == "F3":
            self.navigate("BACK")  # was EXIT (destroyed root) - BACK is a safe no-op if the nav stack is empty
            return
        if keysym == "F12":
            # Cancel the in-progress edit (discard, do not navigate away).
            self.update_fields["cmd"]["value"] = ""
            self.update_fields["comment"]["value"] = ""
            self.update_fields["additional_insureds_edit"]["value"] = ""
            self.update_mode = False
            self.render()
            return

        f = self.update_fields[self.update_focus]
        if keysym == "Tab":
            keys = list(self.update_fields.keys())
            i = keys.index(self.update_focus)
            self.update_focus = keys[(i + 1) % len(keys)]
            self.update_cursor = 0
        elif keysym == "BackSpace":
            if self.update_cursor > 0:
                self.update_cursor -= 1
                f["value"] = f["value"][:self.update_cursor] + f["value"][self.update_cursor + 1:]
        elif keysym == "Left":
            if self.update_cursor > 0:
                self.update_cursor -= 1
        elif keysym == "Right":
            if self.update_cursor < f["width"] - 1:
                self.update_cursor += 1
        elif len(event.char) == 1 and event.char.isprintable():
            if self.update_cursor < f["width"]:
                val = (f["value"] + " " * f["width"])[:f["width"]]
                val = val[:self.update_cursor] + event.char + val[self.update_cursor + 1:]
                f["value"] = val.rstrip()
                if self.update_cursor < f["width"] - 1:
                    self.update_cursor += 1
        self.render()
