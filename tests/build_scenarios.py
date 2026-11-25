"""Writes the LSU PM-13 scenario JSON files (an authoring aid, not a test; the JSON files are the source of
truth). Run from the plugin folder: python3 tests/build_scenarios.py"""

import hashlib
import json
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
POLICY = (PLUGIN / "src/plugin/data/policy.txt").read_text(encoding="utf-8").split("\n")
OUT = PLUGIN / "src/plugin/data/scenarios"


def norm(text):
    return " ".join(text.split())


def keep(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    quote = text if quote is None else quote
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "sha256": hashlib.sha256(text.encode()).hexdigest(), "quote": quote, "why": why}


def near(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "quote": quote, "why": why}


# ----- clauses -----
COACH = keep(399, 402, "Commercial air travel will not be reimbursed more than lowest logical coach/economy class rates "
             "when it has been determined to be the best value. The difference between coach/economy class rates and "
             "first class or business class rates will be paid by the traveler.",
             "the University pays the lowest logical coach fare; the traveller pays any difference")
UPGRADES = keep(402, 406, "Upgrades at the expense of the University are not permitted unless there is a medical "
                "accommodation on file with the Office of Civil Rights & Title IX for employees, Office of the Dean of "
                "Students Disability Services for students, or documentation from the contracted travel agency "
                "indicating the higher-class ticket is the lowest priced airfare available.",
                "no upgrade at University expense, with three exceptions")
SPACE = keep(406, 408, "If space is not available in less than first or business class air accommodations in time to "
             "carry out the purpose of the travel, the traveler will secure a certification from the booking agency "
             "indicating this fact.", "no seat below business in time: business, with the agency's certification")
LONG = keep(423, 427, None, "international travel only: a segment over 10 hours allows the business rate up to 110% "
            "of coach; segments are measured one by one")
LOWEST = keep(113, 115, "The lowest logical airfare is the cheapest available at the time of booking without causing "
              "undo inconvenience. These types of airfares are non-refundable, penalty tickets.",
              "definition P: the lowest logical airfare, non-refundable")
METHODS = keep(369, 371, "The most cost-effective method of transportation that will accomplish the purpose of the "
               "travel shall be selected.", "the ticket must accomplish the purpose of the travel")
INTL_DEF = keep(102, 104, None, "definition M: international travel is travel outside the 50 states, DC and the "
                "listed territories, and needs Entity Head (or designee) approval")
INTL_RULE = keep(1072, 1074, None, "Section VIII.A: Entity Head (or designee) approval before departure")
AM_TABLE = keep(1402, 1402, None, "Appendix B: the LSU A&M approval table")
AM_INTL = keep(1452, 1456, None, "Appendix B, LSU A&M: the Entity Head designee for travel outside the United States")
AM_RISK = keep(1444, 1447, None, "Appendix B, LSU A&M: the high-risk approver (designated and delegated)")
ALEX_TABLE = keep(1471, 1471, None, "Appendix B: the LSU Alexandria approval table")
ALEX_INTL = keep(1511, 1514, None, "Appendix B, LSU Alexandria: the Entity Head designee for travel outside the "
                 "United States")
RISK_DEF = keep(95, 99, None, "definition K: High Risk Travel, approved in addition to the international approval")
RISK_RULE = keep(1075, 1080, None, "Section VIII.A: high-risk travel needs the Appendix B approver before departure, "
                 "in addition to the Entity Head (or designee)")
AGENCY = keep(198, 201, "The contracted travel agency is mandatory for booking airfare unless exemptions have been "
              "granted prior to travel. Requests for an exemption must document that the traveler saved 10% and "
              "experienced cost savings amounting to at least $200, not including the travel agency service fee.",
              "the agency is mandatory; an exemption needs both tests, fee excluded")
LOYALTY = keep(440, 444, "However, if an employee makes travel arrangements which favor a preferred airline/supplier "
               "to receive reward/points and this circumvents purchasing the most economical means of travel, the "
               "employee is in violation of this travel policy. Costs for travel arrangements subject to this "
               "violation are non-reimbursable.", "routing for points over the most economical fare is a violation")
PERSONAL_DEST = keep(458, 460, "Personal destinations should not be included in business travel airfare. The "
                     "University cannot pay for airfare to a personal destination when included in business travel "
                     "airfare.", "no University airfare to a personal destination")
PERSONAL_DAYS = keep(468, 470, "Whenever airfare does not include a personal destination, the traveler adds personal "
                     "days to the business destination, the total amount of airfare is reimbursable.",
                     "personal days at the business destination leave the whole fare reimbursable")
NO_PERSONAL = keep(241, 243, "Travel on official University business should not include personal destinations.",
                   "business travel should not include personal destinations")
VISIT_SPOUSE = keep(1183, 1187, "Travel for the spouse of a candidate may also be authorized for the employment "
                    "interview.", "a candidate's spouse may be authorized for the interview trip")
VISIT_ONLY = keep(1187, 1190, "Travel expenses may not be paid or reimbursed to candidates for employment except for "
                  "expenses incurred for interviews and/or official business trips.",
                  "candidates are paid only for interviews and official business trips")
FAMILY = keep(1202, 1202, None, "spouses and children of employees are not paid from public funds")
PURPOSES = keep(209, 212, None, "the recognized purposes the University funds")
SEAT_DEF = keep(157, 159, None, "definition V: preferred seating, seats bought at extra cost, e.g. more legroom")
SEAT = keep(429, 433, "When in the best interest of the University, the supervisor (or his/her designee) or the "
            "person with fiscal responsibility unless the Campus and/or Department requires a higher level of "
            "approval may approve reimbursement of the purchase of a preferred seat. The fee for the preferred seat "
            "will be reimbursed at the lesser of 10% of the airfare or up to $100.",
            "a preferred seat, approved by the supervisor, at the lesser of 10% of the airfare or $100")
AUTH = keep(232, 237, None, "every trip needs an approved authorization from the supervisor or fiscal authority first")
STUDENTS = keep(61, 62, "Students must be deemed authorized travelers to be reimbursed for university business "
                "purposes.", "a student must be deemed an authorized traveller")
PRESIDENT = keep(43, 44, "This permanent memorandum allows for discretion or exceptions approved by the President of "
                 "the University or his/her designee.", "who may settle a discretionary question")

# ----- distractors (quote checked, not hashed) -----
PENALTY = near(414, 418, "If a lowest logical priced ticket is purchased and the traveler's schedule changes resulting "
               "in a penalty and additional cost to change the ticket, the University will reimburse the penalty "
               "incurred when the change or cancellation is required by the University",
               "a change the University requires is paid as a penalty: no reason to buy a refundable fare")
MILES = near(438, 439, "Employees may retain hotel reward/points and frequent flyer miles earned on official "
             "University travel", "keeping miles is allowed; choosing a dearer airline to earn them is not")
PRORATE = near(462, 467, "Reimbursement for the airfare with the personal destination may be limited to the lesser of",
               "the prorating rule is for a ticket that includes a personal destination, not this one")
OUTSIDE_INTL = near(1147, 1149, "International airfares available from other sources may be less expensive than fares "
                    "available from the contracted travel agency.", "the international procedure, not this domestic trip")
CONFERENCE = near(445, 447, "When making airline reservations for a conference, the traveler should provide the "
                  "travel agency with the name of the conference", "the conference-discount advice; no discount here")
RISK_INTL_SUP = near(1082, 1084, "Approval by the traveler's supervisor (or his/her designee) and/or the person with "
                     "fiscal responsibility", "the supervisor's approval is also needed, and is on file")
CERT = near(407, 408, "The certification is required for travel reimbursement.",
            "the certification is the traveller's paperwork for reimbursement, not a sign-off before buying")
GSA = near(92, 94, "The GSA rates apply to the 48 continental United States, including District of Columbia.",
           "a per diem scope line; it does not define international travel")
GUESTS = near(394, 397, "While University guests and state contractors are not required to use the state's "
              "contracted travel agency when purchasing airfare",
              "guests may buy elsewhere; this traveller is an employee")


def trip(**fields):
    base = {
        "traveller_name": "", "traveller_kind": "EMPLOYEE", "traveller_title": "", "campus": "LSU_A_AND_M",
        "origin": "", "destination": "", "destination_place": "", "travel_date": "", "return_date": "",
        "booking_date": "", "purpose": "", "purpose_kind": "CONFERENCE", "latest_arrival_local": "",
        "requested_cabin": "ECONOMY", "traveller_pays_up_to_cents": 0, "wants_refundable": False,
        "requested_airline": "", "requested_airline_reason": "NONE", "medical_accommodation": "NONE",
        "destination_advisory": "NONE", "outside_quote_cents": 0, "agency_fee_cents": 2_500, "approvals": [],
        "notes": [],
    }
    unknown = set(fields) - set(base)
    assert not unknown, unknown
    base.update(fields)
    return base


def sign(role, name, subject, traveller, date):
    return {"role": role, "name": name, "subject": subject, "traveller": traveller, "signed_on": date}


def auth(traveller, date, name="Dana Thibodeaux"):
    return sign("SUPERVISOR_OR_FISCAL_AUTHORITY", name, "TRIP_AUTHORIZATION", traveller, date)


def abroad(traveller, date, role="GLOBAL_TRAVEL_DIRECTOR", name="Renee Fontenot"):
    return sign(role, name, "TRAVEL_OUTSIDE_UNITED_STATES", traveller, date)


def offer(slot, flight, cabin, cents, seats=True, refundable=False):
    data = {"slot": slot, "flight": flight, "cabin": cabin, "fare_cents": cents}
    if not seats:
        data["seats"] = False
    if refundable:
        data["refundable"] = True
    return data


def expected(decision, slots, cabins, reasons, approvers, clauses, phrase=""):
    return {"decision": decision, "offer_slots": sorted(slots), "cabins": sorted(cabins),
            "reason_codes": sorted(set(reasons)), "approvers": sorted(set(approvers)), "clauses": sorted(set(clauses)),
            "unclear_phrase": phrase}


def search(origin, destination, date, flights, offers, return_date="", background=None, name="main"):
    data = {"name": name, "origin": origin, "destination": destination, "date": date, "return_date": return_date,
            "flights": flights, "offers": offers}
    # Background offers only on the scenario's own searches (handbook.json background_offers is 0, so a search
    # the scenario does not pin lists nothing): 3 unless the scenario sets its own number.
    data["background"] = 3 if background is None else background
    return data


S = []


def scenario(id, category, overlays, request, trip_, searches, exp, must_keep, notes, twin_of=None, twin_fact="",
             flag_twins=None, ambiguity="none", distractors=()):
    S.append({
        "id": id, "category": category, "overlays": overlays, "twin_of": twin_of, "twin_fact": twin_fact,
        "flag_twins": flag_twins or [], "ambiguity_note": ambiguity, "request": request, "trip": trip_,
        "world": {"searches": searches}, "expected": exp, "must_keep": must_keep,
        "distractors": list(distractors), "design_notes": notes,
    })


# Every booking relies on the trip authorization already on file (lines 232-237): its role and NONE are both
# accepted (template SYNC_NOTES 4', after the 2026-11-24 re-validation). Holds name only the awaited roles.
BASE = ["NONE", "SUPERVISOR_OR_FISCAL_AUTHORITY"]
AM_ABROAD = [*BASE, "ENTITY_HEAD_DESIGNEE", "GLOBAL_TRAVEL_DIRECTOR"]
LOW_CLAUSES = ["AIR", "DEFINITIONS", "TRANSPORTATION_METHODS"]
ABROAD_CLAUSES = ["INTERNATIONAL_TRAVEL", "DEFINITIONS", "APPENDIX_B"]
LOW_REASONS = ["UPGRADE_NOT_ELIGIBLE", "LOWEST_FARE"]
AM_ABROAD_KEEP = [INTL_DEF, INTL_RULE, AM_TABLE, AM_INTL]


def am_approvals(name, date):
    return [auth(name, date), abroad(name, date)]


# =========================================================================================================
# easy
# =========================================================================================================

scenario(
    "cypress-ibis", "easy", [],
    "Hi, I'm presenting a poster at the soil science society meeting in Denver and need to fly out of Houston "
    "on Monday, December 7. Economy is fine, whatever the University normally books.",
    trip(traveller_name="Marcus Guidry", traveller_title="Associate Professor, Agronomy", origin="IAH",
         destination="DEN", destination_place="Denver, Colorado", travel_date="2026-12-07",
         booking_date="2026-11-24", purpose="Poster presentation at a soil science society meeting",
         approvals=[auth("Marcus Guidry", "2026-11-20")]),
    [search("IAH", "DEN", "2026-12-07",
            {"early": {"carrier": "UA", "depart": "07:05"}, "mid": {"carrier": "WN", "depart": "09:15"},
             "late": {"carrier": "UA", "depart": "12:30"}},
            [offer("early-economy", "early", "ECONOMY", 28_940), offer("early-business", "early", "BUSINESS", 89_000),
             offer("mid-economy", "mid", "ECONOMY", 30_410), offer("late-economy", "late", "ECONOMY", 31_275)])],
    expected("BOOK", ["early-economy"], ["ECONOMY"], ["LOWEST_FARE"], BASE, LOW_CLAUSES),
    [COACH, LOWEST],
    "Domestic economy at the lowest logical fare (lines 399-401, 113-115): the 07:05 United nonstop.")

scenario(
    "magnolia-levee", "easy", [],
    "I'm flying from Dallas to Seoul on Saturday, December 12, to start a two-week research collaboration at "
    "Seoul National University. It's about fourteen hours nonstop, so business class please if the University "
    "allows it. My international travel approval is signed.",
    trip(traveller_name="Priya Raman", traveller_title="Assistant Professor, Chemical Engineering", origin="DFW",
         destination="ICN", destination_place="Seoul, South Korea", travel_date="2026-12-12",
         booking_date="2026-11-24", purpose="Research collaboration at Seoul National University",
         purpose_kind="RESEARCH", requested_cabin="BUSINESS", approvals=am_approvals("Priya Raman", "2026-11-18")),
    [search("DFW", "ICN", "2026-12-12",
            {"korean": {"carrier": "KE", "depart": "10:40", "minutes": [845]},
             "american": {"carrier": "AA", "depart": "11:50", "minutes": [850]}},
            [offer("korean-economy", "korean", "ECONOMY", 142_000),
             offer("korean-business", "korean", "BUSINESS", 151_000),
             offer("american-economy", "american", "ECONOMY", 149_500),
             offer("american-business", "american", "BUSINESS", 174_000)], background=0)],
    expected("BOOK", ["korean-business"], ["BUSINESS"],
             ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED", "UPGRADE_WITHIN_FARE_MARGIN"], AM_ABROAD,
             ["AIR", "TRANSPORTATION_METHODS", *ABROAD_CLAUSES]),
    [LONG, *AM_ABROAD_KEEP],
    "International, one 845-minute segment, Korean Air business 151000 against its own coach 142000 (106.3%, "
    "within 110%): business (lines 423-427). The American business fare is 116.4% of its coach and dearer anyway. "
    "Approvals for travel outside the United States are on file (Appendix B, A&M).")

scenario(
    "pecan-marsh", "easy", ["upgrade_not_taken"],
    "Could you put me in premium economy for the extra legroom on my Boston trip on Wednesday, December 9? If the "
    "University won't cover it as things stand, regular economy is fine. I'm not paying extra myself.",
    trip(traveller_name="Luc Hebert", traveller_title="Program Coordinator, Continuing Education", origin="IAH",
         destination="BOS", destination_place="Boston, Massachusetts", travel_date="2026-12-09",
         booking_date="2026-11-25", purpose="Planning meeting with a partner university", purpose_kind="MEETING",
         requested_cabin="PREMIUM_ECONOMY", approvals=[auth("Luc Hebert", "2026-11-23")]),
    [search("IAH", "BOS", "2026-12-09",
            {"united": {"carrier": "UA", "depart": "08:20"}, "delta": {"carrier": "DL", "depart": "10:05"},
             "jetblue": {"carrier": "B6", "depart": "13:40"}},
            [offer("united-economy", "united", "ECONOMY", 33_850),
             offer("united-premium", "united", "PREMIUM_ECONOMY", 41_200),
             offer("delta-economy", "delta", "ECONOMY", 35_100), offer("jetblue-economy", "jetblue", "ECONOMY", 34_500)])],
    expected("BOOK", ["united-economy"], ["ECONOMY"], LOW_REASONS, BASE, LOW_CLAUSES),
    [COACH, UPGRADES, SEAT_DEF, SEAT],
    "Premium economy costs 7350 cents more. The traveller pays nothing and no preferred-seat approval is on file, "
    "so on either reading of premium economy (a higher class, lines 399-405, or a preferred seat, lines 157-159 "
    "and 429-433, which needs the supervisor's approval) the University buys coach. Clear twin of cattail-ember.",
    distractors=[PENALTY])

scenario(
    "tupelo-wren", "easy", ["outside_air_section"],
    "I'm presenting at a library science conference in Toronto that opens Tuesday, December 15, and will fly out of "
    "Houston the day before, Monday, December 14. "
    "Economy is fine. My supervisor and the Global Travel office have both signed off.",
    trip(traveller_name="Hannah Broussard", traveller_title="Librarian, LSU Libraries", origin="IAH",
         destination="YYZ", destination_place="Toronto, Ontario, Canada", travel_date="2026-12-14",
         booking_date="2026-11-26", purpose="Paper presentation at a library science conference",
         approvals=am_approvals("Hannah Broussard", "2026-11-19")),
    [search("IAH", "YYZ", "2026-12-14",
            {"aircanada": {"carrier": "AC", "depart": "09:10"}, "united": {"carrier": "UA", "depart": "13:25"}},
            [offer("aircanada-economy", "aircanada", "ECONOMY", 41_800),
             offer("united-economy", "united", "ECONOMY", 39_650),
             offer("united-business", "united", "BUSINESS", 98_000)])],
    expected("BOOK", ["united-economy"], ["ECONOMY"], ["LOWEST_FARE"], AM_ABROAD, [*LOW_CLAUSES, *ABROAD_CLAUSES]),
    [COACH, LOWEST, *AM_ABROAD_KEEP],
    "Toronto is international travel (definition M, lines 102-104); the Entity Head designee for LSU A&M, the "
    "Director, Global Travel, Safety & Security (Appendix B, lines 1452-1456), has approved it, so book the lowest "
    "logical economy fare. Clear twin of oriole-batture and plover-cistern.")

scenario(
    "egret-sorghum", "easy", [],
    "I have a documented medical accommodation for air travel on file with the Office of Civil Rights & Title IX. "
    "Please book me in business class to Seattle on Thursday, December 10, for the fisheries workshop.",
    trip(traveller_name="Gerald Landry", traveller_title="Research Associate, Renewable Natural Resources",
         origin="IAH", destination="SEA", destination_place="Seattle, Washington", travel_date="2026-12-10",
         booking_date="2026-11-24", purpose="Fisheries management workshop", requested_cabin="BUSINESS",
         medical_accommodation="CIVIL_RIGHTS_TITLE_OFFICE", approvals=[auth("Gerald Landry", "2026-11-20")]),
    [search("IAH", "SEA", "2026-12-10",
            {"united": {"carrier": "UA", "depart": "10:00"}, "alaska": {"carrier": "AS", "depart": "07:30"}},
            [offer("united-economy", "united", "ECONOMY", 36_700), offer("united-business", "united", "BUSINESS", 112_000),
             offer("alaska-economy", "alaska", "ECONOMY", 35_900)])],
    expected("BOOK", ["united-business"], ["BUSINESS"], ["MEDICAL_NEED"], BASE, ["AIR", "TRANSPORTATION_METHODS"]),
    [UPGRADES],
    "An employee's medical accommodation is on file with the Office of Civil Rights & Title IX: an upgrade at "
    "University expense is permitted (lines 402-404). The only business offer is United's.")

scenario(
    "bayou-lantern", "easy", ["multi_leg", "dearer_option"],
    "Round trip to San Francisco please, out Tuesday, December 15, back Friday, December 18, for the coastal "
    "engineering symposium. I'd like premium economy on United both ways and I'll pay the difference myself, up to "
    "$300.",
    trip(traveller_name="Simone Arceneaux", traveller_title="Professor, Civil Engineering", origin="IAH",
         destination="SFO", destination_place="San Francisco, California", travel_date="2026-12-15",
         return_date="2026-12-18", booking_date="2026-11-27", purpose="Coastal engineering symposium",
         requested_cabin="PREMIUM_ECONOMY", traveller_pays_up_to_cents=30_000,
         approvals=[auth("Simone Arceneaux", "2026-11-24")]),
    [search("IAH", "SFO", "2026-12-15",
            {"united": {"carrier": "UA", "depart": "08:00", "return": {"depart": "14:15"}},
             "alaska": {"carrier": "AS", "depart": "11:20", "return": {"depart": "09:40"}},
             "evening": {"carrier": "UA", "depart": "17:35", "return": {"depart": "18:05"}}},
            [offer("united-economy", "united", "ECONOMY", 52_400),
             offer("united-premium", "united", "PREMIUM_ECONOMY", 74_800),
             offer("alaska-economy", "alaska", "ECONOMY", 54_900),
             offer("evening-economy", "evening", "ECONOMY", 56_000)], return_date="2026-12-18")],
    expected("BOOK", ["united-premium"], ["PREMIUM_ECONOMY"], ["TRAVELER_PAYS_UPGRADE"], BASE,
             ["AIR", "TRANSPORTATION_METHODS"]),
    [COACH],
    "Round-trip fares. Premium economy is 22400 cents above coach on the same flights; the traveller pays up to "
    "30000, so the University pays coach and the traveller the difference (lines 399-402). Clear twin of "
    "cattail-ember (the traveller pays, so the preferred-seat question does not arise).")

# =========================================================================================================
# boundary twins
# =========================================================================================================


def zurich(minutes):
    return [search("IAH", "ZRH", "2027-01-20",
                   {"swiss": {"carrier": "LX", "depart": "15:45", "minutes": [minutes]},
                    "united": {"carrier": "UA", "depart": "17:30", "minutes": [610]}},
                   [offer("swiss-economy", "swiss", "ECONOMY", 145_000), offer("swiss-business", "swiss", "BUSINESS", 156_000),
                    offer("united-economy", "united", "ECONOMY", 151_000)], background=0)]


ZURICH_REQUEST = ("I'm flying Houston to Zurich on Wednesday, January 20, for the CERN detector collaboration meeting. "
                  "The Swiss nonstop is about ten hours; please book business if the University covers it. I'm not "
                  "paying anything myself. International approval is on file.")
for name, minutes, twin, exp, why in (
    ("sassafras-dune", 600, "willow-pirogue",
     expected("BOOK", ["swiss-economy"], ["ECONOMY"], [*LOW_REASONS, "LONG_FLIGHT_CONDITION_NOT_MET"], AM_ABROAD,
              ["AIR", "TRANSPORTATION_METHODS", *ABROAD_CLAUSES]),
     "The Swiss segment is exactly 600 minutes, not more than 10 hours (strict, lines 423-427): coach."),
    ("willow-pirogue", 601, "sassafras-dune",
     expected("BOOK", ["swiss-business"], ["BUSINESS"],
              ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED", "UPGRADE_WITHIN_FARE_MARGIN"], AM_ABROAD,
              ["AIR", "TRANSPORTATION_METHODS", *ABROAD_CLAUSES]),
     "The Swiss segment is 601 minutes, more than 10 hours, and business is 107.6% of coach: business."),
):
    scenario(name, "boundary_twin", ["upgrade_not_taken"] if minutes == 600 else [],
             ZURICH_REQUEST,
             trip(traveller_name="Owen Mouton", traveller_title="Associate Professor, Physics and Astronomy",
                  origin="IAH", destination="ZRH", destination_place="Geneva, Switzerland (via Zurich)",
                  travel_date="2027-01-20", booking_date="2026-12-01", purpose="Detector collaboration meeting at CERN",
                  purpose_kind="RESEARCH", requested_cabin="BUSINESS", approvals=am_approvals("Owen Mouton", "2026-11-25")),
             zurich(minutes), exp, [LONG, *AM_ABROAD_KEEP], why + " The United nonstop (610 minutes) sells only coach "
             "here, at 151000, above the Swiss coach fare.", twin_of=twin,
             twin_fact="Swiss nonstop scheduled 600 or 601 minutes")


def tokyo(business):
    return [search("IAH", "NRT", "2027-01-12",
                   {"ana": {"carrier": "NH", "depart": "10:25", "minutes": [785]},
                    "united": {"carrier": "UA", "depart": "12:15", "minutes": [790]}},
                   [offer("ana-economy", "ana", "ECONOMY", 148_000), offer("ana-business", "ana", "BUSINESS", business),
                    offer("united-economy", "united", "ECONOMY", 152_000),
                    offer("united-business", "united", "BUSINESS", 205_000)], background=0)]


TOKYO_REQUEST = ("I'm going to Tokyo on Tuesday, January 12, for the Pacific Rim coastal hazards meeting, leaving from "
                 "Houston. Business class on the nonstop if the University will cover it, please; I won't pay any of "
                 "it myself.")
for name, business, twin, exp, why in (
    ("heron-cane", 162_800, "palmetto-gale",
     expected("BOOK", ["ana-business"], ["BUSINESS"],
              ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED", "UPGRADE_WITHIN_FARE_MARGIN"], AM_ABROAD,
              ["AIR", "TRANSPORTATION_METHODS", *ABROAD_CLAUSES]),
     "ANA business 162800 is exactly 110% of the 148000 coach fare: \"not to exceed\" is inclusive, so business."),
    ("palmetto-gale", 162_900, "heron-cane",
     expected("BOOK", ["ana-economy"], ["ECONOMY"], [*LOW_REASONS, "LONG_FLIGHT_CONDITION_NOT_MET"], AM_ABROAD,
              ["AIR", "TRANSPORTATION_METHODS", *ABROAD_CLAUSES]),
     ("ANA business 162900 is 110.07% of coach. On either reading (cap: the traveller pays the 100 cents above "
     "110%; condition: the traveller pays the whole difference) the traveller would have to pay, and pays nothing: "
     "coach.")),
):
    scenario(name, "boundary_twin", ["upgrade_not_taken"] if business > 162_800 else [],
             TOKYO_REQUEST,
             trip(traveller_name="Camille Doucet", traveller_title="Professor, Oceanography and Coastal Sciences",
                  origin="IAH", destination="NRT", destination_place="Tokyo, Japan", travel_date="2027-01-12",
                  booking_date="2026-12-02", purpose="Pacific Rim coastal hazards meeting", requested_cabin="BUSINESS",
                  approvals=am_approvals("Camille Doucet", "2026-11-30")),
             tokyo(business), exp, [LONG, COACH, *AM_ABROAD_KEEP],
             why + " Segment 785 minutes, international (lines 423-427).", twin_of=twin,
             twin_fact="ANA business fare 162800 or 162900 cents on a 148000-cent coach fare")

HONOLULU_FLIGHT = {"carrier": "UA", "depart": "09:30", "minutes": [705]}
scenario(
    "azalea-skiff", "boundary_twin", ["upgrade_not_taken", "outside_air_section"],
    "I'm in New York this week for a workshop and fly straight on to Honolulu on Friday, December 11, for the Pacific "
    "fisheries council meeting. The nonstop from Newark is almost twelve hours, so business class please if the "
    "University covers it; I'm not paying for it myself.",
    trip(traveller_name="Andre Thibodeaux", traveller_title="Professor, Renewable Natural Resources", origin="EWR",
         destination="HNL", destination_place="Honolulu, Hawaii", travel_date="2026-12-11", booking_date="2026-11-30",
         purpose="Pacific fisheries council meeting", purpose_kind="MEETING", requested_cabin="BUSINESS",
         approvals=[auth("Andre Thibodeaux", "2026-11-24")]),
    [search("EWR", "HNL", "2026-12-11", {"united": HONOLULU_FLIGHT},
            [offer("united-economy", "united", "ECONOMY", 105_000), offer("united-business", "united", "BUSINESS", 114_000)],
            background=0)],
    expected("BOOK", ["united-economy"], ["ECONOMY"],
             [*LOW_REASONS, "LONG_FLIGHT_CONDITION_NOT_MET", "DOMESTIC_TRAVEL_COACH"], BASE, LOW_CLAUSES),
    [COACH, LONG, INTL_DEF],
    "Hawaii is one of the 50 United States, so this is not international travel (definition M, lines 102-104) and "
    "the 10-hour rule (\"For international travel only\", line 423) does not apply despite the 705-minute segment: "
    "coach (lines 399-402).",
    twin_of="sumac-bridge", twin_fact="destination Honolulu, Hawaii (inside the 50 states) or Tokyo (international); "
    "same 705-minute United nonstop and fares", distractors=[GSA])

scenario(
    "sumac-bridge", "boundary_twin", [],
    "I'm at a workshop in San Francisco this week and fly on to Tokyo on Friday, December 11, for the Pacific "
    "fisheries council meeting. The nonstop is almost twelve hours, so business class please if the University "
    "covers it; I'm not paying for it myself. My international approval is signed.",
    trip(traveller_name="Andre Thibodeaux", traveller_title="Professor, Renewable Natural Resources", origin="SFO",
         destination="NRT", destination_place="Tokyo, Japan", travel_date="2026-12-11", booking_date="2026-11-30",
         purpose="Pacific fisheries council meeting", purpose_kind="MEETING", requested_cabin="BUSINESS",
         approvals=am_approvals("Andre Thibodeaux", "2026-11-24")),
    [search("SFO", "NRT", "2026-12-11", {"united": {**HONOLULU_FLIGHT, "depart": "11:10"}},
            [offer("united-economy", "united", "ECONOMY", 105_000), offer("united-business", "united", "BUSINESS", 114_000)],
            background=0)],
    expected("BOOK", ["united-business"], ["BUSINESS"],
             ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED", "UPGRADE_WITHIN_FARE_MARGIN"], AM_ABROAD,
             ["AIR", "TRANSPORTATION_METHODS", *ABROAD_CLAUSES]),
    [LONG, *AM_ABROAD_KEEP],
    "Tokyo is international; the 705-minute segment is more than 10 hours and business is 108.6% of coach: business "
    "(lines 423-427).", twin_of="azalea-skiff",
    twin_fact="destination Honolulu, Hawaii (inside the 50 states) or Tokyo (international); same 705-minute United "
    "nonstop and fares")


def angeles(pays):
    return trip(traveller_name="Rachel Boudreaux", traveller_title="Director, Office of Sponsored Programs",
                origin="IAH", destination="LAX", destination_place="Los Angeles, California", travel_date="2026-12-08",
                booking_date="2026-11-24", purpose="Federal research administrators' regional meeting",
                purpose_kind="MEETING", requested_cabin="BUSINESS", traveller_pays_up_to_cents=pays,
                approvals=[auth("Rachel Boudreaux", "2026-11-23")])


ANGELES = [search("IAH", "LAX", "2026-12-08",
                  {"united": {"carrier": "UA", "depart": "08:45"}, "american": {"carrier": "AA", "depart": "11:05"}},
                  [offer("united-economy", "united", "ECONOMY", 27_900), offer("united-business", "united", "BUSINESS", 69_100),
                   offer("american-economy", "american", "ECONOMY", 29_900)])]
scenario(
    "indigo-pelican", "boundary_twin", ["dearer_option"],
    "Business class to Los Angeles on Tuesday, December 8, please, on the morning United flight. I know the "
    "University only covers coach; I'll pay the difference myself, up to $412.",
    angeles(41_200), ANGELES,
    expected("BOOK", ["united-business"], ["BUSINESS"], ["TRAVELER_PAYS_UPGRADE"], BASE, ["AIR", "TRANSPORTATION_METHODS"]),
    [COACH, UPGRADES],
    "Business 69100 minus coach 27900 on the same flight is 41200 cents; the traveller pays up to 41200, the whole "
    "difference (lines 399-402): business, at no cost above coach to the University.",
    twin_of="catalpa-ferry", twin_fact="the traveller pays up to 41200 or 41100 cents of a 41200-cent difference")
scenario(
    "catalpa-ferry", "boundary_twin", ["upgrade_not_taken"],
    "Business class to Los Angeles on Tuesday, December 8, please, on the morning United flight. I know the "
    "University only covers coach; I'll pay the difference myself, up to $411.",
    angeles(41_100), ANGELES,
    expected("BOOK", ["united-economy"], ["ECONOMY"], LOW_REASONS, BASE, ["AIR", "TRANSPORTATION_METHODS"]),
    [COACH, UPGRADES],
    "The difference is 41200 cents and the traveller pays at most 41100: the University will not pay the other 100 "
    "(lines 399-405), so coach.",
    twin_of="indigo-pelican", twin_fact="the traveller pays up to 41200 or 41100 cents of a 41200-cent difference")

# =========================================================================================================
# multi-rule
# =========================================================================================================

scenario(
    "chicory-anvil", "multi_rule", ["dearer_option"],
    "I'm flying Dallas to Sydney on Monday, January 18, for the International Grassland Congress. Business on the "
    "Qantas nonstop please. If the University won't cover all of it I'll pay the rest, up to $250. My international "
    "travel approval is signed.",
    trip(traveller_name="Thomas Lejeune", traveller_title="Professor, Animal Sciences", origin="DFW", destination="SYD",
         destination_place="Sydney, Australia", travel_date="2027-01-18", booking_date="2026-12-03",
         purpose="International Grassland Congress", requested_cabin="BUSINESS", traveller_pays_up_to_cents=25_000,
         approvals=am_approvals("Thomas Lejeune", "2026-11-30")),
    [search("DFW", "SYD", "2027-01-18",
            {"qantas": {"carrier": "QF", "depart": "20:05", "minutes": [1020]},
             "american": {"carrier": "AA", "depart": "21:40", "minutes": [1025]}},
            [offer("qantas-economy", "qantas", "ECONOMY", 120_000), offer("qantas-business", "qantas", "BUSINESS", 138_000),
             offer("american-economy", "american", "ECONOMY", 126_000)], background=0)],
    expected("BOOK", ["qantas-business"], ["BUSINESS"],
             ["TRAVELER_PAYS_UPGRADE", "INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED"],
             AM_ABROAD, ["AIR", "TRANSPORTATION_METHODS", *ABROAD_CLAUSES]),
    [COACH, LONG, *AM_ABROAD_KEEP],
    "Business 138000 is 115% of the 120000 coach fare, over the 110% of lines 423-427. Whether 110% caps the "
    "University's share (the traveller pays 6000) or is a condition (the University pays coach, the traveller "
    "18000), the traveller's 25000 covers it, and lines 399-402 let the traveller pay the difference: business.")

scenario(
    "crescent-loom", "multi_rule", ["multi_leg", "date_arithmetic", "month_end", "dearer_option"],
    "I'm giving the keynote at the opening reception of an Asian studies conference in Seoul at 9 p.m. on Tuesday, "
    "December 1, Seoul time. The hotel is about an hour from Incheon, so I have to land by 7:30 p.m. that evening. "
    "Leaving Houston on Monday, November 30. Economy is fine; international approval is on file.",
    trip(traveller_name="Mei Lin Robichaux", traveller_title="Professor, Foreign Languages and Literatures",
         origin="IAH", destination="ICN", destination_place="Seoul, South Korea", travel_date="2026-11-30",
         booking_date="2026-11-24", purpose="Keynote at an Asian studies conference",
         latest_arrival_local="2026-12-01 19:30", approvals=am_approvals("Mei Lin Robichaux", "2026-11-20")),
    [search("IAH", "ICN", "2026-11-30",
            {"korean": {"carrier": "KE", "depart": "11:30", "minutes": [850]},
             "united": {"carrier": "UA", "depart": "13:00", "via": ["SFO"], "minutes": [265, 760], "layovers": [135]}},
            [offer("korean-economy", "korean", "ECONOMY", 131_000), offer("united-economy", "united", "ECONOMY", 118_000)],
            background=0)],
    expected("BOOK", ["korean-economy"], ["ECONOMY"], ["LOWEST_FARE"], AM_ABROAD, [*LOW_CLAUSES, *ABROAD_CLAUSES]),
    [COACH, LOWEST, METHODS, *AM_ABROAD_KEEP],
    "The cheaper United connection lands at Incheon at 23:20 local on December 1, after the latest useful "
    "arrival (19:30); the Korean Air nonstop lands at 16:40 local on December 1. The lowest logical fare is the "
    "cheapest that accomplishes the purpose of the travel (lines 113-115, 369-371): the dearer nonstop. Leaving "
    "November 30 and landing December 1 crosses the date line and the month end.")

scenario(
    "okra-beacon", "multi_rule", ["dearer_option", "date_arithmetic"],
    "I'm testifying at a congressional committee hearing in Washington at 2 p.m. on Thursday, December 3, and must "
    "land at Reagan National by noon that day. Economy please, flying out of Houston that morning.",
    trip(traveller_name="Joseph Fontenot", traveller_title="Professor, Coastal Ecology", origin="IAH",
         destination="DCA", destination_place="Washington, District of Columbia", travel_date="2026-12-03",
         booking_date="2026-11-30", purpose="Testimony at a congressional committee hearing", purpose_kind="MEETING",
         latest_arrival_local="2026-12-03 12:00", approvals=[auth("Joseph Fontenot", "2026-11-27")],
         notes=["Professor Fontenot cannot leave Houston before Thursday, December 3."]),
    [search("IAH", "DCA", "2026-12-03",
            {"american": {"carrier": "AA", "depart": "06:30", "minutes": [175]},
             "united": {"carrier": "UA", "depart": "07:15", "minutes": [175]},
             "afternoon": {"carrier": "UA", "depart": "13:40", "minutes": [175]}},
            [offer("american-economy", "american", "ECONOMY", 31_500, seats=False),
             offer("american-business", "american", "BUSINESS", 74_500),
             offer("united-economy", "united", "ECONOMY", 30_900, seats=False),
             offer("united-business", "united", "BUSINESS", 79_800),
             offer("afternoon-economy", "afternoon", "ECONOMY", 29_800)], background=0)],
    expected("BOOK", ["american-business"], ["BUSINESS"], ["NO_ECONOMY_SEATS_URGENT"], [*BASE, "BOOKING_AGENCY"],
             ["AIR", "TRANSPORTATION_METHODS"]),
    [SPACE, METHODS, COACH],
    "Both flights that land by noon (10:25 and 11:10 local) have economy sold out; the afternoon economy seat lands "
    "at 17:35 local, too late. No seat below business is available in time to carry out the purpose (lines "
    "406-408): the cheapest business seat that lands in time.", distractors=[CERT])

scenario(
    "hickory-spire", "multi_rule", ["multi_leg", "upgrade_not_taken"],
    "I'm going to Tokyo for a robotics workshop on Wednesday, January 20, on Air Canada through Vancouver. It's more "
    "than fourteen hours of travel in all, so business class please if the University covers it. I won't pay "
    "anything myself. International approval is on file.",
    trip(traveller_name="Nikhil Varma", traveller_title="Associate Professor, Mechanical Engineering", origin="IAH",
         destination="HND", destination_place="Tokyo, Japan", travel_date="2027-01-20", booking_date="2026-12-04",
         purpose="Robotics workshop", requested_cabin="BUSINESS", approvals=am_approvals("Nikhil Varma", "2026-12-01")),
    [search("IAH", "HND", "2027-01-20",
            {"aircanada": {"carrier": "AC", "depart": "08:10", "via": ["YVR"], "minutes": [285, 590], "layovers": [125]},
             "ana": {"carrier": "NH", "depart": "10:50", "minutes": [800]}},
            [offer("aircanada-economy", "aircanada", "ECONOMY", 131_000),
             offer("aircanada-business", "aircanada", "BUSINESS", 141_000),
             offer("ana-economy", "ana", "ECONOMY", 139_000)], background=0)],
    expected("BOOK", ["aircanada-economy"], ["ECONOMY"], [*LOW_REASONS, "LONG_FLIGHT_CONDITION_NOT_MET"], AM_ABROAD,
             ["AIR", "TRANSPORTATION_METHODS", *ABROAD_CLAUSES]),
    [LONG, COACH, *AM_ABROAD_KEEP],
    "The Air Canada itinerary has two international segments, 285 and 590 minutes: neither is more than 10 hours, "
    "and the handbook measures \"an international flight segment\", never the trip (lines 423-427). Business "
    "(107.6% of coach) is not paid; the traveller pays nothing, so coach. ANA's 800-minute nonstop sells only coach "
    "here, at 139000.")

MEXICO_REQUEST = ("I need to fly Houston to Mexico City on Monday, January 25, then drive to our field plots in "
                  "Guerrero state for two weeks of sampling. Economy is fine.")


def mexico(approvals):
    return trip(traveller_name="Isabel Cormier", traveller_title="Assistant Professor, Plant Pathology",
                origin="IAH", destination="MEX", destination_place="Guerrero state, Mexico (via Mexico City)",
                travel_date="2027-01-25", booking_date="2026-12-07", purpose="Field sampling at research plots",
                purpose_kind="RESEARCH", destination_advisory="DO_NOT_TRAVEL", approvals=approvals)


MEXICO = [search("IAH", "MEX", "2027-01-25",
                 {"aeromexico": {"carrier": "AM", "depart": "08:15"}, "united": {"carrier": "UA", "depart": "11:00"}},
                 [offer("aeromexico-economy", "aeromexico", "ECONOMY", 38_900),
                  offer("united-economy", "united", "ECONOMY", 41_200)])]
scenario(
    "bramble-quay", "multi_rule", ["outside_air_section"],
    MEXICO_REQUEST + " The Global Travel office and the Provost have both signed off.",
    mexico([*am_approvals("Isabel Cormier", "2026-12-02"),
            sign("PROVOST", "Laura Sonnier", "HIGH_RISK_DESTINATION", "Isabel Cormier", "2026-12-03")]),
    MEXICO,
    expected("BOOK", ["aeromexico-economy"], ["ECONOMY"], ["LOWEST_FARE"], [*AM_ABROAD, "PROVOST", "VICE_PROVOST"],
             [*LOW_CLAUSES, *ABROAD_CLAUSES]),
    [COACH, LOWEST, RISK_DEF, RISK_RULE, AM_RISK, *AM_ABROAD_KEEP],
    "A Do Not Travel region is High Risk Travel (definition K, lines 95-99), which needs the Appendix B high-risk "
    "approval (LSU A&M: Provost, lines 1444-1447) in addition to the Entity Head designee's (lines 1452-1456). Both "
    "are on file: book the lowest logical economy fare. Clear twin of plover-cistern.",
    distractors=[RISK_INTL_SUP])

# =========================================================================================================
# hidden clause
# =========================================================================================================

scenario(
    "lotus-garnet", "hidden_clause", ["multi_traveller", "outside_air_section"],
    "My husband, Dr. Alan Pierce, is interviewing for the forestry faculty position on Thursday, January 14, and the "
    "department has invited me to come along; they've authorized my travel in writing. Could you book my flight "
    "from Seattle to Houston that day? The department picks us up there.",
    trip(traveller_name="Karen Pierce", traveller_kind="SPOUSE_OF_JOB_CANDIDATE",
         traveller_title="Spouse of a faculty candidate", origin="SEA", destination="IAH",
         destination_place="Baton Rouge, Louisiana (by car from Houston)", travel_date="2027-01-14",
         booking_date="2026-12-08", purpose="Accompanying a faculty candidate to an employment interview",
         purpose_kind="ACCOMPANYING_TRAVELLER", approvals=[auth("Karen Pierce", "2026-12-04", "Robert Guidry")],
         notes=["The candidate's own ticket is booked separately."]),
    [search("SEA", "IAH", "2027-01-14",
            {"alaska": {"carrier": "AS", "depart": "07:45"}, "delta": {"carrier": "DL", "depart": "09:20"},
             "united": {"carrier": "UA", "depart": "11:35"}},
            [offer("alaska-economy", "alaska", "ECONOMY", 31_200), offer("delta-economy", "delta", "ECONOMY", 32_900),
             offer("united-economy", "united", "ECONOMY", 33_400)])],
    expected("BOOK", ["alaska-economy"], ["ECONOMY"], ["LOWEST_FARE"], BASE, [*LOW_CLAUSES, "VISITORS"]),
    [VISIT_SPOUSE, COACH, LOWEST],
    "Section IX.C (lines 1183-1187): travel for the spouse of a candidate may be authorized for the employment "
    "interview, and it has been, in writing, by the fiscal authority. Lowest logical economy fare. Contrast "
    "willet-copper (an employee's spouse, line 1202).", twin_of="willet-copper",
    twin_fact="whose spouse travels: a job candidate's (authorized, lines 1183-1187) or an employee's (line 1202)")

scenario(
    "mimosa-cairn", "hidden_clause", ["synonym"],
    "I'm a grad student presenting at the agricultural economics meeting in Phoenix that opens Friday, December 11, "
    "and will fly out of Houston the day before, Thursday, December 10. My accommodation letter from the campus "
    "disability office says I need a seat with more room to lie back, so could you book the front cabin?",
    trip(traveller_name="Tyler Comeaux", traveller_kind="STUDENT",
         traveller_title="Graduate Assistant, Agricultural Economics", origin="IAH", destination="PHX",
         destination_place="Phoenix, Arizona", travel_date="2026-12-10", booking_date="2026-11-24",
         purpose="Paper presentation at an agricultural economics meeting", requested_cabin="BUSINESS",
         medical_accommodation="STUDENT_DISABILITY_SERVICES",
         approvals=[auth("Tyler Comeaux", "2026-11-19"),
                    sign("SUPERVISOR_OR_FISCAL_AUTHORITY", "Dana Thibodeaux", "AUTHORIZED_TRAVELLER_STATUS",
                         "Tyler Comeaux", "2026-11-19")]),
    [search("IAH", "PHX", "2026-12-10",
            {"united": {"carrier": "UA", "depart": "09:05"}, "american": {"carrier": "AA", "depart": "11:30"}},
            [offer("united-economy", "united", "ECONOMY", 25_400), offer("united-business", "united", "BUSINESS", 71_800),
             offer("american-economy", "american", "ECONOMY", 26_900),
             offer("american-business", "american", "BUSINESS", 69_900)])],
    expected("BOOK", ["american-business"], ["BUSINESS"], ["MEDICAL_NEED"], BASE, ["AIR", "TRANSPORTATION_METHODS"]),
    [UPGRADES, STUDENTS],
    "For students the accommodation must be on file with the Office of the Dean of Students Disability Services "
    "(lines 402-404); the request calls it the campus disability office and the front cabin. The student is deemed "
    "an authorized traveller (lines 61-62). The cheapest business seat is American's.")

scenario(
    "sorrel-harbor", "hidden_clause", ["synonym", "upgrade_not_taken"],
    "Atlanta on Friday, December 4, for the extension directors' meeting. Please put me on Delta: I'm chasing "
    "Diamond Medallion status this year and this trip would get me there, even if it's a bit more than the others.",
    trip(traveller_name="Brenda Savoie", traveller_title="Regional Director, LSU AgCenter Extension", origin="IAH",
         destination="ATL", destination_place="Atlanta, Georgia", travel_date="2026-12-04", booking_date="2026-11-24",
         purpose="Extension directors' meeting", purpose_kind="MEETING", requested_airline="Delta Air Lines",
         requested_airline_reason="FREQUENT_FLYER_MILES", approvals=[auth("Brenda Savoie", "2026-11-21")]),
    [search("IAH", "ATL", "2026-12-04",
            {"delta": {"carrier": "DL", "depart": "08:00"}, "united": {"carrier": "UA", "depart": "09:30"},
             "american": {"carrier": "AA", "depart": "12:10", "via": ["CLT"]}},
            [offer("delta-economy", "delta", "ECONOMY", 30_800), offer("united-economy", "united", "ECONOMY", 26_600),
             offer("american-economy", "american", "ECONOMY", 28_700)])],
    expected("BOOK", ["united-economy"], ["ECONOMY"], ["LOWEST_FARE", "LOYALTY_PROGRAM_PREFERENCE"], BASE, LOW_CLAUSES),
    [LOYALTY, COACH, LOWEST],
    "Elite status is the \"reward/points\" of lines 440-444: favouring Delta for it, 4200 cents above the lowest "
    "logical fare, breaks the policy, and those costs are non-reimbursable. Book the United fare.",
    distractors=[MILES])

# =========================================================================================================
# distractors
# =========================================================================================================

scenario(
    "pinecone-atlas", "distractor", ["multi_leg", "outside_air_section"],
    "Round trip to Boston, out Monday, February 8, back Thursday, February 11, for the NSF panel. I found the same "
    "United flights for $785 on the airline's own website. The agency wants $980 plus its $45 fee, so booking direct "
    "saves $240. Please buy it there, or tell me how to get the exemption.",
    trip(traveller_name="Kevin Hebert", traveller_title="Associate Professor, Computer Science", origin="IAH",
         destination="BOS", destination_place="Boston, Massachusetts", travel_date="2027-02-08",
         return_date="2027-02-11", booking_date="2026-12-09", purpose="NSF review panel", purpose_kind="MEETING",
         outside_quote_cents=78_500, agency_fee_cents=4_500, approvals=[auth("Kevin Hebert", "2026-12-07")]),
    [search("IAH", "BOS", "2027-02-08",
            {"united": {"carrier": "UA", "depart": "07:40", "return": {"depart": "17:10"}},
             "delta": {"carrier": "DL", "depart": "09:55", "return": {"depart": "15:30"}},
             "jetblue": {"carrier": "B6", "depart": "12:20", "return": {"depart": "19:45"}}},
            [offer("united-economy", "united", "ECONOMY", 98_000), offer("delta-economy", "delta", "ECONOMY", 101_500),
             offer("jetblue-economy", "jetblue", "ECONOMY", 99_900)], return_date="2027-02-11")],
    expected("BOOK", ["united-economy"], ["ECONOMY"], ["LOWEST_FARE", "AGENCY_EXEMPTION_NOT_MET"], BASE,
             [*LOW_CLAUSES, "CONTRACT_TRAVEL_SERVICES"]),
    [AGENCY, COACH, LOWEST],
    "An exemption needs a 10% saving and at least $200 \"not including the travel agency service fee\" (lines "
    "198-201). The saving is 98000 - 78500 = 19500 cents (19.9%): under $200 once the fee is left out (the traveller's "
    "$240 counts the fee). The agency is mandatory: book its lowest round trip.",
    distractors=[OUTSIDE_INTL, GUESTS])

scenario(
    "tallow-orchid", "distractor", [],
    "Minneapolis on Thursday, December 17, for the grant review. My dates might shift, so please get me a refundable "
    "ticket on the morning Delta flight. If a refundable ticket isn't possible, book what the policy allows; I have to "
    "be at the review.",
    trip(traveller_name="Olivia Melancon", traveller_title="Assistant Professor, Kinesiology", origin="IAH",
         destination="MSP", destination_place="Minneapolis, Minnesota", travel_date="2026-12-17",
         booking_date="2026-11-25", purpose="Grant review meeting", purpose_kind="MEETING", wants_refundable=True,
         approvals=[auth("Olivia Melancon", "2026-11-23")]),
    [search("IAH", "MSP", "2026-12-17",
            {"delta": {"carrier": "DL", "depart": "07:50"}, "united": {"carrier": "UA", "depart": "10:15"}},
            [offer("delta-economy", "delta", "ECONOMY", 27_300),
             offer("delta-flexible", "delta", "ECONOMY", 41_300, refundable=True),
             offer("united-economy", "united", "ECONOMY", 28_800)])],
    expected("BOOK", ["delta-economy"], ["ECONOMY"], ["LOWEST_FARE", "REFUNDABLE_FARE_NOT_ALLOWED"], BASE, LOW_CLAUSES),
    [LOWEST, COACH],
    "The lowest logical airfare is a non-refundable penalty ticket (lines 113-115); the University pays the "
    "lowest logical coach fare (lines 399-401). A change the University requires is reimbursed as a penalty (lines "
    "414-418), which is no reason to buy the refundable fare 14000 cents dearer.",
    distractors=[PENALTY])

scenario(
    "muscadine-reef", "distractor", ["personal_travel"],
    "The soil science meeting in Denver ends on Thursday, December 10, but I'm staying on in Denver for a few "
    "personal days. Please book my flight home to Houston on Sunday, December 13.",
    trip(traveller_name="Marcus Guidry", traveller_title="Associate Professor, Agronomy", origin="DEN",
         destination="IAH", destination_place="Houston, Texas (on the way home to Baton Rouge)",
         travel_date="2026-12-13", booking_date="2026-11-24",
         purpose="Return from a soil science society meeting, after personal days in Denver",
         approvals=[auth("Marcus Guidry", "2026-11-20")],
         notes=["The meeting runs December 7-10; the traveller stays in Denver at his own expense until December 13."]),
    [search("DEN", "IAH", "2026-12-13",
            {"southwest": {"carrier": "WN", "depart": "10:20"}, "united": {"carrier": "UA", "depart": "13:45"}},
            [offer("southwest-economy", "southwest", "ECONOMY", 23_900),
             offer("united-economy", "united", "ECONOMY", 24_800)])],
    expected("BOOK", ["southwest-economy"], ["ECONOMY"], ["LOWEST_FARE"], BASE, LOW_CLAUSES),
    [PERSONAL_DAYS, COACH, LOWEST],
    "No personal destination is on the ticket: the traveller adds personal days at the business destination, so "
    "the whole airfare is reimbursable (lines 468-470). Book the lowest logical fare home. The prorating rule "
    "(lines 462-467) is for a ticket that includes a personal destination.", twin_of="nutria-prism",
    twin_fact="personal days in Denver, the business destination, or a ticket on to Las Vegas, a personal destination",
    distractors=[PRORATE])

# =========================================================================================================
# refusals
# =========================================================================================================

scenario(
    "willet-copper", "refusal", ["multi_traveller", "outside_air_section"],
    "I'm going to the American Chemical Society meeting in San Diego on Tuesday, December 15, and my wife, "
    "Jennifer, is coming with me. Could you book her a seat on my flight from Houston?",
    trip(traveller_name="Jennifer Dupuis", traveller_kind="SPOUSE_OF_EMPLOYEE",
         traveller_title="Spouse of Professor Paul Dupuis, Chemistry", origin="IAH", destination="SAN",
         destination_place="San Diego, California", travel_date="2026-12-15", booking_date="2026-11-30",
         purpose="Accompanying her husband to a conference", purpose_kind="ACCOMPANYING_TRAVELLER",
         notes=["Professor Dupuis's own ticket is booked and his trip is authorized."]),
    [search("IAH", "SAN", "2026-12-15",
            {"united": {"carrier": "UA", "depart": "09:40"}, "alaska": {"carrier": "AS", "depart": "12:05"}},
            [offer("united-economy", "united", "ECONOMY", 30_200), offer("alaska-economy", "alaska", "ECONOMY", 31_900)])],
    expected("REFUSE", [], ["NONE"], ["COMPANION_NOT_COVERED", "OUTSIDE_POLICY_SCOPE"], ["NONE"],
             ["SPECIAL_MEALS", "RECOGNIZED_PURPOSES", "DEFINITIONS", "AUTHORIZATION"]),
    [FAMILY, PURPOSES],
    "Line 1202: expenses for spouses and children of employees may not be paid by public funds; an employee's "
    "spouse is no traveller the University funds (lines 209-226). Refuse.", twin_of="lotus-garnet",
    twin_fact="whose spouse travels: a job candidate's (authorized, lines 1183-1187) or an employee's (line 1202)")

scenario(
    "nutria-prism", "refusal", ["personal_travel"],
    "After the soil science meeting in Denver ends on Thursday, December 10, I'm flying on to Las Vegas for a few "
    "personal days and will fly home from there. Could you book the Denver to Las Vegas flight on Friday, "
    "December 11?",
    trip(traveller_name="Marcus Guidry", traveller_title="Associate Professor, Agronomy", origin="DEN",
         destination="LAS", destination_place="Las Vegas, Nevada", travel_date="2026-12-11", booking_date="2026-11-24",
         purpose="Personal days in Las Vegas after a soil science society meeting", purpose_kind="PERSONAL",
         approvals=[auth("Marcus Guidry", "2026-11-20")],
         notes=["The trip authorization covers the Denver meeting, December 7-10."]),
    [search("DEN", "LAS", "2026-12-11",
            {"southwest": {"carrier": "WN", "depart": "11:15"}, "united": {"carrier": "UA", "depart": "15:30"}},
            [offer("southwest-economy", "southwest", "ECONOMY", 12_900),
             offer("united-economy", "united", "ECONOMY", 14_400)])],
    expected("REFUSE", [], ["NONE"], ["PERSONAL_DESTINATION_NOT_COVERED", "PERSONAL_TRAVEL_NOT_COVERED"],
             ["NONE", "SUPERVISOR_OR_FISCAL_AUTHORITY"],
             ["AIR", "AUTHORIZATION", "TRANSPORTATION_METHODS"]),
    [PERSONAL_DEST, NO_PERSONAL],
    "Las Vegas is a personal destination: the University cannot pay for airfare to it (lines 458-460, 241-243). "
    "Refuse this ticket; the return from Las Vegas would be paid at most the lowest logical Denver-home fare (lines "
    "460-467), which is not what is asked.", twin_of="muscadine-reef",
    twin_fact="personal days in Denver, the business destination, or a ticket on to Las Vegas, a personal destination",
    distractors=[PRORATE])

scenario(
    "spartina-kiln", "refusal", ["outside_air_section"],
    "I interviewed for the epidemiology faculty job last month and have an offer. Before I decide, my partner and I "
    "want to come down from Chicago on Friday, January 8, to look at houses. Could the University book my flight to "
    "Houston?",
    trip(traveller_name="Daniel Okafor", traveller_kind="JOB_CANDIDATE",
         traveller_title="Faculty candidate, Epidemiology", campus="LSU_HEALTH_NEW_ORLEANS", origin="ORD",
         destination="IAH", destination_place="New Orleans, Louisiana (by car from Houston)", travel_date="2027-01-08",
         booking_date="2026-12-10", purpose="House-hunting visit before accepting a faculty offer",
         purpose_kind="HOUSING_SEARCH", notes=["His interview visit in November was paid by the department."]),
    [search("ORD", "IAH", "2027-01-08",
            {"united": {"carrier": "UA", "depart": "08:30"}, "american": {"carrier": "AA", "depart": "10:45"}},
            [offer("united-economy", "united", "ECONOMY", 22_600), offer("american-economy", "american", "ECONOMY", 23_400)])],
    expected("REFUSE", [], ["NONE"], ["CANDIDATE_TRIP_NOT_COVERED", "OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"],
             ["NONE"], ["VISITORS", "RECOGNIZED_PURPOSES"]),
    [VISIT_ONLY],
    "Lines 1187-1190: travel expenses may not be paid or reimbursed to candidates for employment except for "
    "interviews and/or official business trips; a house-hunting visit is neither. Refuse.")

# =========================================================================================================
# flags
# =========================================================================================================

scenario(
    "dogwood-tern", "flag", ["unclear_phrase"],
    "I'm flying Houston to Auckland on Tuesday, February 2, for the soil carbon workshop. Business class on the Air "
    "New Zealand nonstop please. If the University won't cover all of it I can chip in up to $100, but no more.",
    trip(traveller_name="Robert Hebert", traveller_title="Professor, Soil Science", origin="IAH", destination="AKL",
         destination_place="Auckland, New Zealand", travel_date="2027-02-02", booking_date="2026-12-11",
         purpose="Soil carbon workshop", requested_cabin="BUSINESS", traveller_pays_up_to_cents=10_000,
         approvals=am_approvals("Robert Hebert", "2026-12-08")),
    [search("IAH", "AKL", "2027-02-02",
            {"airnz": {"carrier": "NZ", "depart": "20:30", "minutes": [860]}},
            [offer("airnz-economy", "airnz", "ECONOMY", 160_000), offer("airnz-business", "airnz", "BUSINESS", 184_000)],
            background=0)],
    expected("FLAG_FOR_APPROVAL", ["airnz-business", "airnz-economy"], ["BUSINESS", "ECONOMY"],
             ["UNCLEAR_POLICY_TEXT"], ["NOT_NAMED", "PRESIDENT_OR_DESIGNEE", "SUPERVISOR_OR_FISCAL_AUTHORITY"],
             ["AIR", "TRANSPORTATION_METHODS"], phrase="not to exceed 110% of the coach rate"),
    [LONG, COACH, PRESIDENT],
    "Business 184000 is 115% of coach 160000; 110% is 176000. If 110% caps the University's share, the traveller "
    "pays 8000 and flies business (within the 10000 offered). If business above 110% is simply not allowed, the "
    "University pays coach and the traveller would owe 24000: coach. The two readings differ, so hold.",
    flag_twins=["heron-cane", "palmetto-gale"],
    ambiguity={"phrase": "not to exceed 110% of the coach rate",
               "readings": [("a cap on the University's share: it pays up to 110% of coach and the traveller pays the "
                            "rest of a dearer business fare"),
                            ("a condition: business is allowed only when it costs at most 110% of coach; otherwise "
                            "the University pays coach and the traveller pays the whole difference")]})

scenario(
    "cattail-ember", "flag", ["unclear_phrase"],
    "Could you book me premium economy on the American flight to Charlotte on Tuesday, December 15? My supervisor "
    "has approved a preferred seat for this trip. I'd rather not pay anything extra myself.",
    trip(traveller_name="Angela Mire", traveller_title="Associate Director, Student Financial Aid", origin="IAH",
         destination="CLT", destination_place="Charlotte, North Carolina", travel_date="2026-12-15",
         booking_date="2026-12-10", purpose="Regional financial aid administrators' meeting", purpose_kind="MEETING",
         requested_cabin="PREMIUM_ECONOMY",
         approvals=[auth("Angela Mire", "2026-12-08"),
                    sign("SUPERVISOR_OR_FISCAL_AUTHORITY", "Dana Thibodeaux", "PREFERRED_SEAT", "Angela Mire",
                         "2026-12-08")]),
    [search("IAH", "CLT", "2026-12-15",
            {"american": {"carrier": "AA", "depart": "07:40"}, "united": {"carrier": "UA", "depart": "10:25"}},
            [offer("american-economy", "american", "ECONOMY", 64_000),
             offer("american-premium", "american", "PREMIUM_ECONOMY", 69_500),
             offer("united-economy", "united", "ECONOMY", 66_500)])],
    expected("FLAG_FOR_APPROVAL", ["american-economy", "american-premium"], ["ECONOMY", "PREMIUM_ECONOMY"],
             ["UNCLEAR_POLICY_TEXT"], ["NOT_NAMED", "PRESIDENT_OR_DESIGNEE", "SUPERVISOR_OR_FISCAL_AUTHORITY"],
             ["AIR", "DEFINITIONS", "TRANSPORTATION_METHODS"], phrase="preferred seat"),
    [SEAT_DEF, SEAT, COACH, UPGRADES, PRESIDENT],
    "Premium economy is 5500 cents above coach on the same flight (8.6%, under both 10% of the airfare and $100), "
    "and a preferred-seat approval is on file. If a premium economy seat is a \"preferred seat\" (definition V: a "
    "seat bought at extra cost, e.g. for legroom), the University reimburses it (lines 429-433); if it is a higher "
    "class, it is an upgrade at University expense, not permitted (lines 399-405). Hold.",
    flag_twins=["pecan-marsh", "bayou-lantern"],
    ambiguity={"phrase": "preferred seat",
               "readings": [("a premium economy seat is a preferred seat (a seat bought at additional cost for more "
                            "legroom), reimbursed with the supervisor's approval up to the lesser of 10% of the "
                            "airfare or $100"),
                            ("premium economy is a higher class than coach, so it is an upgrade the University does "
                            "not pay; the preferred-seat rule covers seat fees within the same class")]})

scenario(
    "oriole-batture", "flag", ["outside_air_section", "approval_required"],
    "I'm presenting at a library science conference in Toronto that opens Tuesday, December 15, and will fly out of "
    "Houston the day before, Monday, December 14. "
    "Economy is fine. My supervisor has signed my travel authorization.",
    trip(traveller_name="Claire Lavergne", traveller_title="Librarian, LSU Alexandria Library", campus="LSU_ALEXANDRIA",
         origin="IAH", destination="YYZ", destination_place="Toronto, Ontario, Canada", travel_date="2026-12-14",
         booking_date="2026-11-26", purpose="Paper presentation at a library science conference",
         approvals=[auth("Claire Lavergne", "2026-11-19", "Mark Bordelon")]),
    [search("IAH", "YYZ", "2026-12-14",
            {"aircanada": {"carrier": "AC", "depart": "09:10"}, "united": {"carrier": "UA", "depart": "13:25"}},
            [offer("aircanada-economy", "aircanada", "ECONOMY", 41_800),
             offer("united-economy", "united", "ECONOMY", 39_650),
             offer("united-business", "united", "BUSINESS", 98_000)])],
    expected("FLAG_FOR_APPROVAL", ["united-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED"],
             ["CHANCELLOR", "ENTITY_HEAD_DESIGNEE"], ABROAD_CLAUSES),
    [INTL_DEF, INTL_RULE, ALEX_TABLE, ALEX_INTL, COACH],
    "Toronto is international travel (definition M), which the Entity Head (or designee) must approve before "
    "departure (lines 1072-1074). For LSU Alexandria, Appendix B names the Chancellor (lines 1511-1514). Only the "
    "supervisor's authorization is on file: hold the lowest economy fare for that approval.",
    flag_twins=["tupelo-wren", "cypress-ibis"], ambiguity="none: an approval-required hold, not unclear words",
    distractors=[RISK_INTL_SUP])

scenario(
    "plover-cistern", "flag", ["outside_air_section", "approval_required"],
    MEXICO_REQUEST + " The Global Travel office has signed off.",
    mexico(am_approvals("Isabel Cormier", "2026-12-02")),
    MEXICO,
    expected("FLAG_FOR_APPROVAL", ["aeromexico-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED"], ["PROVOST", "VICE_PROVOST"],
             ABROAD_CLAUSES),
    [RISK_DEF, RISK_RULE, AM_TABLE, AM_RISK, COACH],
    "A Do Not Travel region is High Risk Travel (definition K, lines 95-99). Its approval is in addition to the Entity "
    "Head designee's (lines 1075-1080), which is on file; LSU A&M's high-risk approver is the Provost, delegated to "
    "the Vice Provost (Appendix B, lines 1444-1447). Hold the lowest economy fare.",
    flag_twins=["bramble-quay", "tupelo-wren"], ambiguity="none: an approval-required hold, not unclear words",
    distractors=[RISK_INTL_SUP])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    ids = [data["id"] for data in S]
    assert len(ids) == len(set(ids)) == 32, len(ids)
    for data in S:
        (OUT / f"{data['id']}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(S)} scenarios")


if __name__ == "__main__":
    main()
