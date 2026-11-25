"""The handbook-specific settings the template's acceptance tests read. Every other file in tests/ is the
template's and stays identical across plugins (see TEMPLATE_GUIDE.md)."""

from pathlib import Path

import contract

ROOT = Path(__file__).resolve().parents[1]

# Ids that are published or taken: a new plugin never reuses one (MASTER_PLAN section 4, "id check").
PUBLISHED_IDS = {
    "aiib-delegation-entitlement", "ec-mission-cabin-allowance", "ftr-city-pair-fare-selection",
    "gates-vendor-flight-ranking", "njc-cabin-meal-allowance", "sfc-travel-preapproval", "uc-g28-expense-audit",
    "un-staff-air-travel-audit", "vt-airfare-policy-booking", "wa-saam-travel-versioned-audit",
    "energy-corporate-flight-booking", "pharma-distributor-flight-booking", "shipping-company-flight-booking",
    "telecommunications-flight-booking", "preference-aware-flight-booking", "llm-context-compress",
    "weather-alert", "word-check", "arxiv-source",
}

# The frozen original's SHA256SUMS, when this checkout sits beside pilot_work/ (skipped elsewhere).
FROZEN_SHA256SUMS = ROOT.parents[1] / "pilot_work" / "originals" / "lsu-pm13" / "frozen" / "SHA256SUMS"

# Scenario mix by primary category (EDGE_CASES.md section 5.2; the 32-scenario row).
MIX = {"easy": 6, "boundary_twin": 8, "multi_rule": 5, "hidden_clause": 3, "distractor": 3, "refusal": 3, "flag": 4}

# Overlay minimums (EDGE_CASES.md section 5.3) for the rules this handbook has. PM-13 has no overnight-stop
# rule, so that overlay is not required.
OVERLAY_MINIMUMS = {
    "multi_leg": 3, "date_arithmetic": 2, "month_end": 1, "personal_travel": 1, "multi_traveller": 1,
    "dearer_option": 2, "upgrade_not_taken": 2, "outside_air_section": 2,
}

# Words a scenario id may not contain beyond the template's universal list: this handbook's rule and role
# terms.
ID_FORBIDDEN_TERMS = {
    "business", "economy", "coach", "premium", "first", "class", "spouse", "husband", "wife", "partner", "family",
    "child", "candidate", "interview", "housing", "student", "disability", "accommodation", "loyalty", "miles",
    "points", "status", "refundable", "penalty", "agency", "exemption", "fee", "seat", "legroom", "hawaii",
    "honolulu", "alaska", "international", "domestic", "foreign", "abroad", "risk", "advisory", "danger",
    "chancellor", "provost", "director", "supervisor", "fiscal", "president", "segment", "connection", "nonstop",
    "vacation", "holiday", "vegas", "toronto", "tokyo", "mexico", "seoul", "sydney", "zurich", "auckland", "late",
    "early", "sold", "credit", "guest", "visitor", "percent", "difference", "pay", "pays",
}

# The handbook-specific enums whose member words a scenario id may not contain either.
ID_CATEGORY_ENUMS = [contract.TravellerKind, contract.Campus, contract.Purpose, contract.Accommodation,
                     contract.Advisory, contract.AirlineReason, contract.ApprovalSubject]

# How many scenarios a degenerate agent may pass: one that always holds the right offer for approval, and
# one that always books the cheapest seat (with the right section). Economy at the lowest logical fare is this
# handbook's default (lines 399-401, 113-115), so the always-lowest agent passes the cases whose answer is the
# cheapest seat listed; set to what it passes (see README). The always-flag agent passes the two holds over
# unclear words (it is given the held offer); the two approval holds need APPROVAL_REQUIRED and the approver.
MAX_PASS_ALWAYS_FLAG = 2
MAX_PASS_ALWAYS_LOWEST = 0  # its approver NONE is never accepted on a booking (lines 232-237)

# Hand-built duration cases beyond the automatic both-sides tests: (rule, outbound scheduled minutes per
# flight, layovers, expected True / False). PM-13 measures each segment on its own and never adds segments or
# layovers, so there is no unclear case.
DURATION_CASES = [
    ("international-segment", [601], [], True),
    ("international-segment", [600], [], False),
    ("international-segment", [480, 480], [60], False),  # 960 minutes of flying, no segment over 600
    ("international-segment", [595, 120], [400], False),  # a long wait never counts
    ("international-segment", [300, 601], [90], True),  # one segment over 600 is enough for the measurement
    ("international-segment", [200, 200, 200], [100, 100], False),
]
