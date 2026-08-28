"""Dummy data for the M2 (Risk Selection / Premium Adjustment / Post) screens.

Nothing here is real production data - it is invented, plausible-looking
filler consistent with the existing mirror's dummy identity (policy
02 HHR 0000001, client "Mr J Doe", agent "Sample Insurance Brokers Ltd").

None of these fields exist on the base UN021 policy record used elsewhere in
the mirror, so they live in their own small dicts here rather than being
bolted onto the shared `policy` dict. A caller wiring these screens into the
main app can either pass these dicts straight through or copy/merge them
into whatever per-policy store it already keeps.
"""

# -- shared policy identity, same shape/keys as UN045's _BLANK_POLICY -------
DEFAULT_POLICY = {
    "policy_branch": "02",
    "policy_type": "HHR",
    "policy_num": "0000001",
    "policy_desc": "Sample Contents Cover",
}

# -- UN050 RISK SELECTION ---------------------------------------------------
# value "1" = option selected/reviewed, "" = not selected.
DEFAULT_RISK_OPTIONS = {
    "fine_art":     "",
    "bus_lcv":      "",
    "household":    "1",
    "engineer_cmd": "",
    "gen_covr":     "",
    "travel_tr1":   "",
}

RISK_OPTION_LABELS = [
    ("fine_art",     "Fine Art"),
    ("bus_lcv",      "BUS L/CV"),
    ("household",    "Household"),
    ("engineer_cmd", "Engineer CMD"),
    ("gen_covr",     "GEN COVR"),
    ("travel_tr1",   "TRAVEL TR1"),
]

# -- UN051 HOUSEHOLD OPTION DETAIL ------------------------------------------
DEFAULT_HOUSEHOLD = {
    "situation_address_num": "01",
    "security_alarm_desc":   "RD1",
    "alarm_signalling_date": "01/01/26",
    "full_value_sum_insured": "150,000",
    "auto_rated_premium":    "",
}

# -- UN052 ADJUSTMENT CALC ---------------------------------------------------
DEFAULT_ADJUSTMENTS = [
    {"label": "Adjustment 1", "desc": "Renewal premium recalculation", "premium": "540.00"},
    {"label": "Adjustment 2", "desc": "Sum insured uplift",            "premium": "612.50"},
    {"label": "Adjustment 3", "desc": "Excess amendment",              "premium": "498.75"},
]
