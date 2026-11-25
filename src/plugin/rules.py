"""The answer key's rules for LSU System Permanent Memorandum 13 (PM-13), University Travel (last revised July 2,
2026; Appendix I effective October 1, 2026), as exact integer code. Byte-identical in src/plugin/rules.py and
verifier/rules.py; it imports only modules a verifier may use.

Every rule cites the frozen handbook text (src/plugin/data/policy.txt) by line. Where the text leaves an
answer open, the rule returns FLAG_FOR_APPROVAL with the unclear words, and a scenario may depend on each
unclear phrase at most once (tests/test_scenarios.py). Combinations no scenario needs raise ValueError, so a
new scenario cannot fall silently into untested logic.

The duration hook. The handbook has one duration threshold: "For international travel only, when an
international flight segment is more than 10 hours in duration, the University will allow the business
class rate, not to exceed 110% of the coach rate. The traveler's itinerary provided by the travel agency must
document the flight segment as more than 10 hours" (lines 423-427). It is measured per segment, as the
agency's itinerary documents it (each segment's scheduled minutes), strictly over 600 minutes. Segments are
never added together and layovers never count, so a connection is over the limit exactly when one of its
segments is; there is no unclear case in the measurement itself. Whether the long segment is an
international one, and whether the trip is international travel at all (definition M, lines 102-104), is
decided in solve(), not in the hook.
"""

from contract import (
    Accommodation,
    Advisory,
    AirlineReason,
    ApprovalSubject,
    Approver,
    Cabin,
    Campus,
    Clause,
    Decision,
    Purpose,
    ReasonCode,
    TravellerKind,
)

from .world import airport, days_between

HANDBOOK = "LSU System Permanent Memorandum 13 (PM-13), University Travel, Appendix I (effective October 1, 2026)"

# Each closed-list section and the heading it names in the frozen text (tests check every heading is there).
CLAUSE_HEADINGS = {
    Clause.APPLICATION: "A. Application of Regulations",
    Clause.DEFINITIONS: "II. DEFINITIONS",
    Clause.CONTRACT_TRAVEL_SERVICES: "A. Contract Travel Services",
    Clause.RECOGNIZED_PURPOSES: "B. Recognized Purposes",
    Clause.AUTHORIZATION: "C. Authorization",
    Clause.PERSONAL_CREDITS: "I. Personal Credits",
    Clause.REIMBURSEMENT_REQUESTS: "IV. REQUESTS FOR REIMBURSEMENT",
    Clause.OFFICIAL_DOMICILE: "A. Official Domicile/Temporary Assignment",
    Clause.TRANSPORTATION_METHODS: "V. METHODS OF TRANSPORTATION",
    Clause.AIR: "A. Air",
    Clause.TRAIN: "B. Train",
    Clause.MOTOR_VEHICLE: "C. Motor Vehicle",
    Clause.LODGING_AND_MEALS: "VI. REIMBURSEMENT FOR LODGING AND MEALS & INCIDENTAL EXPENSES (M&IE)",
    Clause.EXTENDED_STAY: "C. Extended Stay",
    Clause.OTHER_EXPENSES: "VII. REIMBURSEMENT FOR OTHER EXPENSES (WHILE IN TRAVEL STATUS ONLY)",
    Clause.AIRLINE_LUGGAGE: "D. Luggage Charges from Airlines",
    Clause.INTERNATIONAL_TRAVEL: "VIII. INTERNATIONAL TRAVEL",
    Clause.VISITORS: "IX. VISITORS TO CAMPUS",
    Clause.SPECIAL_MEALS: "X. SPECIAL MEALS",
    Clause.APPENDIX_A: "APPENDIX A",
    Clause.APPENDIX_B: "APPENDIX B",
}

# The handbook's duration threshold (the per-handbook duration hook; tests/test_duration.py tests both sides).
# operator ">" is strict ("more than").
DURATION_RULES = (
    {"name": "international-segment", "minutes": 600, "operator": ">", "lines": [423, 427],
     "quote": "when an international flight segment is more than 10 hours in duration"},
)
LIMIT = DURATION_RULES[0]["minutes"]

# Handbook-specific conventions shown by booking_requirements, beyond the template's.
CONVENTIONS = (
    ("search_flights lists the offers of the booking agency the university contracts with; each offer's segments, "
     "with their scheduled minutes, are that agency's itinerary."),
)

# Line 424: "the business class rate, not to exceed 110% of the coach rate" (inclusive).
COACH_PERCENT = 110
# Lines 199-200: an exemption from the agency needs "saved 10% and ... cost savings amounting to at least $200,
# not including the travel agency service fee". "saved 10%" has no operator word: exactly 10% is not modelled.
EXEMPTION_PERCENT, EXEMPTION_CENTS = 10, 20_000
# Line 433: a preferred seat "will be reimbursed at the lesser of 10% of the airfare or up to $100".
SEAT_PERCENT, SEAT_CENTS = 10, 10_000

# Appendix B: who approves travel outside the 50 United States and U.S. Territories (the Entity Head designee)
# and travel to High Risk Regions, per campus. Only the campuses a scenario uses are listed.
OUTSIDE_US_APPROVERS = {
    Campus.LSU_A_AND_M: (Approver.GLOBAL_TRAVEL_DIRECTOR,),  # lines 1452-1456
    Campus.LSU_ALEXANDRIA: (Approver.CHANCELLOR,),  # lines 1511-1514
}
HIGH_RISK_APPROVERS = {
    Campus.LSU_A_AND_M: (Approver.PROVOST, Approver.VICE_PROVOST),  # lines 1444-1447 (designated, delegated)
    Campus.LSU_ALEXANDRIA: (Approver.CHANCELLOR, Approver.EXECUTIVE_VICE_CHANCELLOR_ADMINISTRATION),  # 1506-1508
}


def over(rule, offer):
    """True or False: whether one of ``offer``'s segments (out or back) is over the handbook's ``rule``
    duration, measured per segment by its scheduled minutes (lines 423-427); segments never add up."""
    limit = DURATION_RULES[0]["minutes"] if rule == DURATION_RULES[0]["name"] else None
    if limit is None:
        raise ValueError(f"unknown duration rule {rule!r}")
    return any(segment.scheduled_minutes > limit for segment in [*offer.segments, *offer.return_segments])


def domestic_airport(code):
    """Inside the 50 United States (and the territories definition M lists, none of which this world has)."""
    return airport(code).country == "US"


def international_trip(trip):
    """Definition M (lines 102-104): travel to destinations outside the 50 United States, District of
    Columbia, Puerto Rico, U.S. Virgin Islands, American Samoa, Guam and Saipan."""
    if not domestic_airport(trip.origin.code):
        raise ValueError("a trip that starts outside the United States is not modelled")
    return not domestic_airport(trip.destination.code)


def by_value(items):
    return sorted(set(items), key=lambda item: item.value)


def with_parents(clauses):
    """Section V.A (Air) sits under V (Methods of Transportation); either names the section."""
    clauses = list(clauses)
    if Clause.AIR in clauses:
        clauses.append(Clause.TRANSPORTATION_METHODS)
    return clauses


def answer(decision, offers, reasons, approvers, clauses, why, phrase=""):
    return {
        "decision": decision,
        "offer_ids": sorted(offer.offer_id for offer in offers),
        "cabins": by_value(offer.cabin for offer in offers) or [Cabin.NONE],
        "reason_codes": by_value(reasons),
        "approvers": by_value(approvers),
        "clauses": by_value(with_parents(clauses)),
        "unclear_phrase": phrase,
        "explanation": why,
    }


def refuse(reasons, clauses, why):
    return answer(Decision.REFUSE, [], reasons, [Approver.NONE], clauses, why)


def cheapest(offers):
    if not offers:
        return []
    low = min(offer.fare_cents for offer in offers)
    return [offer for offer in offers if offer.fare_cents == low]


def flights_of(offer):
    return tuple((segment.flight_number, segment.depart_utc) for segment in [*offer.segments, *offer.return_segments])


def signed(trip, subject, roles):
    """Whether an approval of ``subject`` by one of ``roles``, covering this traveller, was signed on or
    before the booking date."""
    for record in trip.approvals:
        if record.subject == subject and record.role in roles and record.traveller == trip.traveller_name:
            if days_between(record.signed_on, trip.booking_date) < 0:
                raise ValueError("an approval on file is dated after the booking date")
            return True
    return False


def in_time(trip, offer):
    """Whether the offer lands by the latest useful arrival (local at the destination airport): the method of
    transportation must "accomplish the purpose of the travel" (lines 369-371)."""
    if not trip.latest_arrival_local:
        return True
    return offer.segments[-1].arrive_local <= trip.latest_arrival_local


def medical(trip):
    """Line 402-404: "a medical accommodation on file with the Office of Civil Rights & Title IX for employees,
    Office of the Dean of Students Disability Services for students"."""
    kind, office = trip.traveller_kind, trip.medical_accommodation
    if office in (Accommodation.NONE, Accommodation.DOCTOR_NOTE_ONLY):
        return False
    if kind == TravellerKind.EMPLOYEE and office == Accommodation.CIVIL_RIGHTS_TITLE_OFFICE:
        return True
    if kind == TravellerKind.STUDENT and office == Accommodation.STUDENT_DISABILITY_SERVICES:
        return True
    raise ValueError("an accommodation on file with the other group's office is not modelled")


def solve(trip, offers, hidden):
    """The answer key for one trip and the offers of its searches: the decision, and every accepted offer
    id, cabin, reason, approver and section. ``hidden`` (answer_key_inputs) is unused by this handbook."""
    if hidden:
        raise ValueError("this handbook's scenarios carry no answer_key_inputs")
    refused = who_and_why(trip)
    if refused is not None:
        return refused
    if not signed(trip, ApprovalSubject.TRIP_AUTHORIZATION, {Approver.SUPERVISOR_OR_FISCAL_AUTHORITY}):
        raise ValueError("a trip without its travel authorization (lines 232-237) is not modelled")
    if trip.traveller_kind == TravellerKind.STUDENT and not signed(
            trip, ApprovalSubject.AUTHORIZED_TRAVELLER_STATUS, {Approver.SUPERVISOR_OR_FISCAL_AUTHORITY}):
        raise ValueError("a student not deemed an authorized traveler (lines 61-62) is not modelled")
    international = international_trip(trip)
    booking = choose(trip, offers, international)
    if trip.traveller_kind in (TravellerKind.JOB_CANDIDATE, TravellerKind.SPOUSE_OF_JOB_CANDIDATE):
        # Lines 1183-1188: a candidate's (and the candidate's spouse's) interview travel, authorized in writing.
        booking["clauses"] = by_value([*booking["clauses"], Clause.VISITORS])
        booking["explanation"] += " Lines 1183-1188: interview travel for a candidate, and for the spouse, authorized."
    base = [Approver.NONE, Approver.SUPERVISOR_OR_FISCAL_AUTHORITY]  # lines 232-237: the trip's authorization
    if not international:
        if trip.destination_advisory != Advisory.NONE:
            raise ValueError("a travel advisory on a domestic trip is not modelled")
        if booking["decision"] == Decision.BOOK:
            booking["approvers"] = by_value([*booking["approvers"], *base])
        return booking
    return outside_us(trip, booking, base)


def who_and_why(trip):
    """Refusals for a traveller or a purpose the University does not pay a ticket for; None otherwise."""
    kind, purpose = trip.traveller_kind, trip.purpose_kind
    if kind in (TravellerKind.SPOUSE_OF_EMPLOYEE, TravellerKind.CHILD_OF_EMPLOYEE):
        return refuse([ReasonCode.COMPANION_NOT_COVERED, ReasonCode.OUTSIDE_POLICY_SCOPE],
                      [Clause.SPECIAL_MEALS, Clause.RECOGNIZED_PURPOSES, Clause.DEFINITIONS],
                      "Line 1202: expenses for spouses and children of employees may not be paid by public funds; "
                      "lines 209-226 list the travel the University funds, and an employee's family is not in it.")
    if purpose == Purpose.HOUSING_SEARCH:
        if kind not in (TravellerKind.JOB_CANDIDATE, TravellerKind.SPOUSE_OF_JOB_CANDIDATE):
            raise ValueError("a housing trip by anyone but a candidate is not modelled")
        return refuse([ReasonCode.CANDIDATE_TRIP_NOT_COVERED, ReasonCode.OUTSIDE_POLICY_SCOPE,
                       ReasonCode.PERSONAL_TRAVEL_NOT_COVERED], [Clause.VISITORS],
                      "Lines 1188-1190: travel expenses may not be paid or reimbursed to candidates for employment "
                      "except for interviews and/or official business trips; a housing visit is neither.")
    if purpose == Purpose.PERSONAL:
        return refuse([ReasonCode.PERSONAL_DESTINATION_NOT_COVERED, ReasonCode.PERSONAL_TRAVEL_NOT_COVERED],
                      [Clause.AIR, Clause.AUTHORIZATION],
                      "Lines 458-460 (and 241-243): the University cannot pay for airfare to a personal destination.")
    if purpose == Purpose.ACCOMPANYING_TRAVELLER and kind != TravellerKind.SPOUSE_OF_JOB_CANDIDATE:
        raise ValueError("an accompanying traveller other than a candidate's spouse is not modelled")
    if kind not in (TravellerKind.EMPLOYEE, TravellerKind.STUDENT, TravellerKind.JOB_CANDIDATE,
                    TravellerKind.SPOUSE_OF_JOB_CANDIDATE):
        raise ValueError(f"a {kind.value} traveller is not modelled")
    return None


def outside_us(trip, booking, base):
    """Lines 1072-1080 and definition M (lines 102-104): travel outside the 50 United States needs the Entity
    Head (or designee) approval, the person Appendix B names for the campus, before departure; travel to a High
    Risk Region (definition K, lines 95-99) also needs the Appendix B high-risk approver."""
    designees = OUTSIDE_US_APPROVERS.get(trip.campus)
    risk_roles = HIGH_RISK_APPROVERS.get(trip.campus)
    if designees is None or risk_roles is None:
        raise ValueError(f"travel outside the United States for {trip.campus.value} is not modelled")
    if trip.outside_quote_cents:
        raise ValueError("an outside fare for international travel (Section VIII.H) is not modelled")
    if trip.destination_advisory not in (Advisory.NONE, Advisory.DO_NOT_TRAVEL):
        raise ValueError("whether a lower advisory level makes a High Risk Region is not modelled")
    high_risk = trip.destination_advisory == Advisory.DO_NOT_TRAVEL
    clauses = [Clause.INTERNATIONAL_TRAVEL, Clause.DEFINITIONS, Clause.APPENDIX_B]
    missing = []
    if not signed(trip, ApprovalSubject.TRAVEL_OUTSIDE_UNITED_STATES, set(designees)):
        missing = [Approver.ENTITY_HEAD_DESIGNEE, *designees]
        why = (f"Lines 102-104 and 1072-1074: {trip.destination_place} is international travel, which the Entity "
               f"Head designee for {trip.campus.value} (Appendix B) must approve before departure.")
    elif high_risk and not signed(trip, ApprovalSubject.HIGH_RISK_DESTINATION, set(risk_roles)):
        missing = list(risk_roles)
        why = (f"Lines 95-99 and 1075-1080: travel to a High Risk Region needs the Appendix B high-risk approval for "
               f"{trip.campus.value}, in addition to the international travel approval on file.")
    if missing:
        if booking["decision"] != Decision.BOOK:
            raise ValueError("a missing approval on top of unclear words is not modelled")
        held = {
            **booking, "decision": Decision.FLAG_FOR_APPROVAL, "reason_codes": [ReasonCode.APPROVAL_REQUIRED],
            "approvers": by_value(missing), "clauses": by_value(clauses), "explanation": why,
        }
        return held
    if booking["decision"] == Decision.BOOK:
        relied = [*booking["approvers"], *base, Approver.ENTITY_HEAD_DESIGNEE, *designees,
                  *(risk_roles if high_risk else ())]
        booking["approvers"] = by_value(relied)
        booking["clauses"] = by_value([*booking["clauses"], *clauses])
    return booking


def choose(trip, offers, international):
    """The cabin and offer under Section V.A (lines 391-444) and definition P (lowest logical airfare, lines
    113-117), before any approval for travel outside the United States is checked."""
    usable = [offer for offer in offers if offer.seats_available and in_time(trip, offer)]
    if not usable:
        raise ValueError("no offer that can be bought lands in time")
    coach = cheapest([offer for offer in usable if offer.cabin == Cabin.ECONOMY])
    extras, clauses = [], [Clause.AIR, Clause.DEFINITIONS]
    if trip.outside_quote_cents:
        extras.append(exemption(trip, coach))
        clauses.append(Clause.CONTRACT_TRAVEL_SERVICES)
    if trip.requested_cabin == Cabin.ECONOMY:
        return economy(trip, usable, coach, extras, clauses)
    if trip.outside_quote_cents or trip.wants_refundable or trip.requested_airline:
        raise ValueError("an outside fare, refund or airline wish on a request above economy is not modelled")
    if trip.requested_cabin == Cabin.BUSINESS:
        return business(trip, usable, coach, international)
    if trip.requested_cabin == Cabin.PREMIUM_ECONOMY:
        return premium(trip, usable, coach, international)
    raise ValueError(f"a {trip.requested_cabin.value} request is not modelled")


def exemption(trip, coach):
    """Lines 198-201: booking outside the agency needs an exemption granted beforehand, and the request must
    show the traveller "saved 10% and experienced cost savings amounting to at least $200, not including the
    travel agency service fee". Only quotes that fail a test are modelled: the agency's ticket is bought."""
    if not coach:
        raise ValueError("an outside quote with no economy offer is not modelled")
    fare = coach[0].fare_cents
    saving = fare - trip.outside_quote_cents  # the agency's service fee is not counted (line 200)
    if saving * 100 == EXEMPTION_PERCENT * fare:
        raise ValueError("a saving of exactly 10% is not modelled ('saved 10%' has no operator word)")
    if saving >= EXEMPTION_CENTS and saving * 100 > EXEMPTION_PERCENT * fare:
        raise ValueError("an outside quote that passes both exemption tests is not modelled")
    return ReasonCode.AGENCY_EXEMPTION_NOT_MET


def economy(trip, usable, coach, extras, clauses):
    """Lines 399-401 and definition P: the University pays the lowest logical coach/economy fare; lowest
    logical fares are non-refundable (line 114); loyalty routing that costs more breaks lines 440-444."""
    if not coach:
        others = cheapest(usable)
        if any(offer.cabin == Cabin.PREMIUM_ECONOMY for offer in usable):
            raise ValueError("no economy seat but a premium economy one is not modelled")
        return answer(Decision.BOOK, others, [ReasonCode.NO_ECONOMY_SEATS_URGENT],
                      [Approver.NONE, Approver.BOOKING_AGENCY], [Clause.AIR],
                      "Lines 406-408: no seat below first or business class lands in time to carry out the purpose "
                      "of the travel, so the cheapest business seat that does is bought, with the agency's "
                      "certification.")
    fare = coach[0].fare_cents
    if any(offer.fare_cents < fare for offer in usable):
        raise ValueError("an economy request whose cheapest offer is another cabin is not modelled")
    if any(offer.refundable for offer in coach):
        raise ValueError("a refundable lowest fare is not modelled")
    reasons, notes = [ReasonCode.LOWEST_FARE, *extras], []
    if trip.wants_refundable:
        reasons.append(ReasonCode.REFUNDABLE_FARE_NOT_ALLOWED)
        notes.append("lowest logical fares are non-refundable penalty tickets (line 114)")
    if trip.requested_airline:
        if trip.requested_airline_reason != AirlineReason.FREQUENT_FLYER_MILES:
            raise ValueError("an airline wish for another reason is not modelled")
        if all(offer.carrier != trip.requested_airline for offer in coach):
            reasons.append(ReasonCode.LOYALTY_PROGRAM_PREFERENCE)
            notes.append("the preferred airline costs more, and favouring it for points breaks lines 440-444")
    if extras:
        notes.append(f"the outside quote saves {fare - trip.outside_quote_cents} cents on {fare}, which fails the "
                     "exemption tests of lines 198-201 (service fee not counted)")
    why = "Lines 399-401 and 113-117: the lowest logical economy fare that lands in time"
    return answer(Decision.BOOK, coach, reasons, [Approver.NONE], clauses, why + (": " + "; ".join(notes) if notes else "."))


def same_flights(want, coach):
    if not coach or flights_of(coach[0]) != flights_of(want[0]):
        raise ValueError("the coach rate must be on the same flights as the dearer cabin")
    return coach[0].fare_cents


def business(trip, usable, coach, international):
    """Lines 399-406 and 423-427: business only at the traveller's expense above coach, unless a medical
    accommodation is on file, business is the lowest priced airfare, or (international travel only) a segment is
    more than 10 hours, where the University allows the business rate up to 110% of the coach rate."""
    want = cheapest([offer for offer in usable if offer.cabin == Cabin.BUSINESS])
    if not want:
        raise ValueError("a business request with no business offer in time is not modelled")
    if not coach:
        raise ValueError("a business request with no economy seat in time is not modelled")
    fare = want[0].fare_cents
    if fare <= coach[0].fare_cents:
        return answer(Decision.BOOK, want, [ReasonCode.LOWEST_FARE], [Approver.NONE], [Clause.AIR],
                      "Lines 402-406: the higher-class ticket is the lowest priced airfare available.")
    if medical(trip):
        return answer(Decision.BOOK, want, [ReasonCode.MEDICAL_NEED], [Approver.NONE], [Clause.AIR],
                      "Lines 402-404: a medical accommodation is on file with the office named for this traveller.")
    low = same_flights(want, coach)
    pays = trip.traveller_pays_up_to_cents
    segments = [*want[0].segments, *want[0].return_segments]
    long = over(DURATION_RULES[0]["name"], want[0])
    numbers = f"business {fare} cents against coach {low} ({fare * 100 / low:.2f}%)"
    if international and long:
        if any(segment.scheduled_minutes <= LIMIT for segment in segments):
            raise ValueError("a business ticket with both long and short segments is not modelled")
        if any(domestic_airport(segment.origin) and domestic_airport(segment.destination) for segment in segments):
            raise ValueError("a long domestic segment on an international trip is not modelled")
        if fare * 100 <= COACH_PERCENT * low:
            return answer(Decision.BOOK, want, [ReasonCode.INTERNATIONAL_LONG_FLIGHT, ReasonCode.LONG_FLIGHT_APPROVED,
                                                ReasonCode.UPGRADE_WITHIN_FARE_MARGIN], [Approver.NONE], [Clause.AIR],
                          f"Lines 423-427: an international segment over 600 minutes and {numbers}, within 110%.")
        if pays >= fare - low:
            return answer(Decision.BOOK, want, [ReasonCode.TRAVELER_PAYS_UPGRADE, ReasonCode.INTERNATIONAL_LONG_FLIGHT],
                          [Approver.NONE], [Clause.AIR],
                          f"Lines 399-402 and 423-427: {numbers}; the traveller pays all of the difference over "
                          "coach, so business is bought on either reading of the 110% words.")
        if pays * 100 < fare * 100 - COACH_PERCENT * low:
            return answer(Decision.BOOK, coach, [ReasonCode.UPGRADE_NOT_ELIGIBLE, ReasonCode.LOWEST_FARE,
                                                 ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET], [Approver.NONE],
                          [Clause.AIR],
                          f"Lines 423-427: {numbers}, over 110%, and the traveller will not pay even the part above "
                          "110%: coach on either reading.")
        return answer(Decision.FLAG_FOR_APPROVAL, [*want, *coach], [ReasonCode.UNCLEAR_POLICY_TEXT],
                      [Approver.NOT_NAMED, Approver.PRESIDENT_OR_DESIGNEE, Approver.SUPERVISOR_OR_FISCAL_AUTHORITY],
                      [Clause.AIR],
                      f"Lines 423-427: {numbers}. The traveller pays {pays} cents: enough for the part above 110% "
                      "(a cap: business) but not the difference over coach (a condition: coach).",
                      phrase="not to exceed 110% of the coach rate")
    if pays >= fare - low:
        return answer(Decision.BOOK, want, [ReasonCode.TRAVELER_PAYS_UPGRADE], [Approver.NONE], [Clause.AIR],
                      f"Lines 399-402: {numbers}; the traveller pays the difference ({fare - low} cents, up to {pays}).")
    reasons, clauses = [ReasonCode.UPGRADE_NOT_ELIGIBLE, ReasonCode.LOWEST_FARE], [Clause.AIR]
    why = f"Lines 399-402: {numbers}; the traveller pays only {pays} cents of the {fare - low}-cent difference"
    if international:
        reasons.append(ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET)
        why += "; no segment is more than 600 minutes (lines 423-427)"
    elif long:
        reasons += [ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET, ReasonCode.DOMESTIC_TRAVEL_COACH]
        clauses.append(Clause.DEFINITIONS)
        why += f"; {trip.destination_place} is not international travel (lines 102-104), so lines 423-427 do not apply"
    return answer(Decision.BOOK, coach, reasons, [Approver.NONE], clauses, why + ".")


def premium(trip, usable, coach, international):
    """A premium economy request. The University pays at most the lowest logical coach fare (lines 399-402);
    whether a premium economy seat is a "preferred seat" (definition V, lines 157-159; lines 428-433, with a
    supervisor's approval, at the lesser of 10% of the airfare or $100) is not said."""
    want = cheapest([offer for offer in usable if offer.cabin == Cabin.PREMIUM_ECONOMY])
    if not want or international or over(DURATION_RULES[0]["name"], want[0]):
        raise ValueError("only a domestic premium economy request with an offer in time is modelled")
    if medical(trip):
        raise ValueError("a premium economy request with a medical accommodation is not modelled")
    low = same_flights(want, coach)
    fare, pays = want[0].fare_cents, trip.traveller_pays_up_to_cents
    extra = fare - low
    numbers = f"premium economy {fare} cents against coach {low} ({extra} cents more)"
    if pays >= extra:
        return answer(Decision.BOOK, want, [ReasonCode.TRAVELER_PAYS_UPGRADE], [Approver.NONE], [Clause.AIR],
                      f"Lines 399-402: {numbers}; the traveller pays the difference.")
    seat = signed(trip, ApprovalSubject.PREFERRED_SEAT, {Approver.SUPERVISOR_OR_FISCAL_AUTHORITY})
    if not seat:
        return answer(Decision.BOOK, coach, [ReasonCode.UPGRADE_NOT_ELIGIBLE, ReasonCode.LOWEST_FARE], [Approver.NONE],
                      [Clause.AIR, Clause.DEFINITIONS],
                      f"Lines 399-402 and 428-433: {numbers}; the traveller does not pay it and no preferred-seat "
                      "approval is on file, so coach on either reading.")
    if pays or extra * 100 > SEAT_PERCENT * low or extra > SEAT_CENTS:
        raise ValueError("a premium economy seat dearer than the preferred-seat cap is not modelled")
    return answer(Decision.FLAG_FOR_APPROVAL, [*want, *coach], [ReasonCode.UNCLEAR_POLICY_TEXT],
                  [Approver.NOT_NAMED, Approver.PRESIDENT_OR_DESIGNEE, Approver.SUPERVISOR_OR_FISCAL_AUTHORITY],
                  [Clause.AIR, Clause.DEFINITIONS],
                  f"Lines 157-159, 399-405 and 428-433: {numbers}, within the lesser of 10% and $100, with a "
                  "preferred-seat approval on file. As a preferred seat it is reimbursed; as a higher class it is an "
                  "upgrade the University does not pay.", phrase="preferred seat")
