"""UN021 - POLICY HEADER screen."""
from .base import TerminalScreen


class UN021(TerminalScreen):
    def __init__(self, master, navigate, policy, **kw):
        super().__init__(master, on_key=self._on_key, **kw)
        self.navigate = navigate
        self.policy = policy
        self.render()

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

        self.write(13, 0, f"Ren {p['ren_code']}   {p['ren_desc']}", tag="green")

        self.write(14, 0, "Type of documents . :", tag="green")
        self.write(14, 22, p["type_of_docs_code"], tag="white")
        self.write(14, 27, p["type_of_docs_desc"], tag="green")

        self.write(15, 0, "Payment method . . :", tag="green")
        self.write(15, 21, p["payment_method_code"], tag="white")
        self.write(15, 26, p["payment_method_desc"], tag="green")
        self.write(15, 55, "No.instalments . :", tag="green")
        self.write(15, 74, p["no_instalments"], tag="white")

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

        self.write(22, 0,  "F2=CMX", tag="cyan")
        self.write(22, 10, "F3=Exit", tag="cyan")
        self.write(22, 22, "F5=Policy history", tag="cyan")
        self.write(22, 42, "F6=Quotation", tag="cyan")
        self.write(22, 58, "F7=Letter", tag="cyan")

        self.write(23, 0,  "F9=Referral Messages", tag="cyan")
        self.write(23, 22, "F10=Last claim", tag="cyan")
        self.write(23, 42, "F11=Case", tag="cyan")
        self.write(23, 58, "F12=Previous", tag="cyan")

    def _on_key(self, event):
        if event.keysym == "F9":
            self.navigate("UN489")
        elif event.keysym == "F3":
            self.navigate("EXIT")
        elif event.keysym == "F12":
            self.navigate("BACK")
