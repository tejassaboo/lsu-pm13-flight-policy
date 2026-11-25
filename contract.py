"""Each tool's and task's typed input and output (see nanoagent.plugin.v0001.contract): declarations only.

The first part is the original-handbook template's shared contract and is the same in every plugin made from
it. The HANDBOOK-SPECIFIC part in the middle is filled per handbook: the scenario ids, the closed lists of
approvers and sections, and the trip record; the shared inputs and outputs after it refer to those names.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output

# ---------------------------------------------------------------------------------------------------------
# SHARED (template): keep identical across plugins, except the agent task's id in Task.BOOK_FLIGHT.
# ---------------------------------------------------------------------------------------------------------


class Tool(Enum):
    BOOKING_REQUIREMENTS = "booking_requirements"
    GET_TRIP = "get_trip"
    SEARCH_FLIGHTS = "search_flights"
    SOLVE_BOOKING = "solve_booking"


class Task(Enum):
    BOOKING_REQUIREMENTS = "booking-requirements"
    SEARCH_FLIGHTS = "search-flights"
    BOOK_FLIGHT = "book-lsu-flight"


class Decision(Enum):
    BOOK = "BOOK"
    REFUSE = "REFUSE"
    FLAG_FOR_APPROVAL = "FLAG_FOR_APPROVAL"


class Cabin(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"
    NONE = "NONE"


class ReasonCode(Enum):
    """Why the decision was made. The list is shared by every handbook plugin, so it also holds reasons
    that a given handbook never uses."""

    LOWEST_FARE = "LOWEST_FARE"
    UPGRADE_NOT_ELIGIBLE = "UPGRADE_NOT_ELIGIBLE"
    CLIENT_REIMBURSABLE = "CLIENT_REIMBURSABLE"
    UPGRADE_WITHIN_FARE_MARGIN = "UPGRADE_WITHIN_FARE_MARGIN"
    MEDICAL_NEED = "MEDICAL_NEED"
    COST_SAVINGS = "COST_SAVINGS"
    NO_ECONOMY_SEATS_URGENT = "NO_ECONOMY_SEATS_URGENT"
    TRAVELER_PAYS_UPGRADE = "TRAVELER_PAYS_UPGRADE"
    LONG_FLIGHT_APPROVED = "LONG_FLIGHT_APPROVED"
    LONG_FLIGHT_CONDITION_NOT_MET = "LONG_FLIGHT_CONDITION_NOT_MET"
    PREMIUM_ECONOMY_ALLOWED = "PREMIUM_ECONOMY_ALLOWED"
    UPGRADE_COST_NOT_NOMINAL = "UPGRADE_COST_NOT_NOMINAL"
    ALTERNATE_ROUTE_WITHIN_MARGIN = "ALTERNATE_ROUTE_WITHIN_MARGIN"
    ALTERNATE_ROUTE_TOO_EXPENSIVE = "ALTERNATE_ROUTE_TOO_EXPENSIVE"
    LOYALTY_PROGRAM_PREFERENCE = "LOYALTY_PROGRAM_PREFERENCE"
    COMPANION_NOT_COVERED = "COMPANION_NOT_COVERED"
    PERSONAL_TRAVEL_NOT_COVERED = "PERSONAL_TRAVEL_NOT_COVERED"
    OUTSIDE_POLICY_SCOPE = "OUTSIDE_POLICY_SCOPE"
    NO_COMPLIANT_OFFER = "NO_COMPLIANT_OFFER"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    UNCLEAR_POLICY_TEXT = "UNCLEAR_POLICY_TEXT"
    ADVANCE_PURCHASE_TOO_LATE = "ADVANCE_PURCHASE_TOO_LATE"
    DISTANCE_BELOW_MINIMUM = "DISTANCE_BELOW_MINIMUM"
    DRIVING_EXPECTED = "DRIVING_EXPECTED"
    RAIL_PREFERRED = "RAIL_PREFERRED"
    REFUNDABLE_FARE_NOT_ALLOWED = "REFUNDABLE_FARE_NOT_ALLOWED"
    PREFERRED_CARRIER_REQUIRED = "PREFERRED_CARRIER_REQUIRED"
    CONNECTION_TOO_LONG = "CONNECTION_TOO_LONG"
    OVERNIGHT_STOP_REQUIRED = "OVERNIGHT_STOP_REQUIRED"
    NATIONAL_CARRIER_REQUIRED = "NATIONAL_CARRIER_REQUIRED"
    SENIOR_ROLE_ENTITLEMENT = "SENIOR_ROLE_ENTITLEMENT"
    INTERNATIONAL_LONG_FLIGHT = "INTERNATIONAL_LONG_FLIGHT"
    TRAVELLER_LIMIT_PER_FLIGHT = "TRAVELLER_LIMIT_PER_FLIGHT"
    # HANDBOOK-SPECIFIC reason codes go below this line; keep every shared one above.
    AGENCY_EXEMPTION_NOT_MET = "AGENCY_EXEMPTION_NOT_MET"
    PERSONAL_DESTINATION_NOT_COVERED = "PERSONAL_DESTINATION_NOT_COVERED"
    CANDIDATE_TRIP_NOT_COVERED = "CANDIDATE_TRIP_NOT_COVERED"
    DOMESTIC_TRAVEL_COACH = "DOMESTIC_TRAVEL_COACH"
    # Decoys: codes for rules of other handbooks that this one lacks, so the list hints at none of its own rules.
    NEXT_OF_KIN_TRAVEL = "NEXT_OF_KIN_TRAVEL"
    CREATIVE_TICKETING = "CREATIVE_TICKETING"
    SAME_CLASS_AS_CUSTOMER = "SAME_CLASS_AS_CUSTOMER"
    DOUBLE_BOOKING_PROHIBITED = "DOUBLE_BOOKING_PROHIBITED"
    PRIVATE_AIRCRAFT_NOT_APPROVED = "PRIVATE_AIRCRAFT_NOT_APPROVED"
    OPEN_SKIES_AGREEMENT = "OPEN_SKIES_AGREEMENT"
    FLY_AMERICA_US_CARRIER_REQUIRED = "FLY_AMERICA_US_CARRIER_REQUIRED"
    DENIED_BOARDING_NOT_ALLOWED = "DENIED_BOARDING_NOT_ALLOWED"


class TripType(Enum):
    ONE_WAY = "ONE_WAY"
    ROUND_TRIP = "ROUND_TRIP"


class Topic(Enum):
    ALL = "ALL"
    FIELDS = "FIELDS"
    AIRPORTS = "AIRPORTS"


CODE = "An IATA airport code, e.g. JFK"


@dataclass
class Airport(Output):
    code: Annotated[str, CODE]
    name: Annotated[str, "The airport's name"]
    city: Annotated[str, "The city it serves"]
    country: Annotated[str, "Its country, as an ISO code"]


@dataclass
class Segment(Output):
    flight_number: Annotated[str, "The airline's flight number, e.g. BA 117"]
    origin: Annotated[str, CODE]
    destination: Annotated[str, CODE]
    depart_local: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, local time at that airport"]
    arrive_local: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, local time at that airport"]
    depart_utc: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, UTC"]
    arrive_utc: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, UTC"]
    scheduled_minutes: Annotated[int, "Its scheduled time from departure to arrival, in minutes"]


@dataclass
class Offer(Output):
    offer_id: Annotated[str, "The offer's id, to submit when booking or holding it"]
    carrier: Annotated[str, "The airline"]
    trip_type: Annotated[TripType, "ONE_WAY, or ROUND_TRIP when the fare covers the flights out and back"]
    cabin: Annotated[Cabin, "The cabin sold on every flight of the offer"]
    fare_cents: Annotated[int, "The whole fare for one passenger, in cents of the search's currency"]
    seats_available: Annotated[bool, "False when this cabin is sold out on these flights: it is listed but cannot be bought"]
    refundable: Annotated[bool, "Whether the fare can be refunded or changed without a fee"]
    stops: Annotated[int, "Connections on the way out; zero for a nonstop"]
    segments: Annotated[list[Segment], "The flights out, in order"]
    layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights out"]
    stopover_nights: Annotated[list[bool], "Per connection out: true when it is a ticketed stopover with a hotel night booked"]
    flying_minutes: Annotated[int, "The flights' scheduled minutes out added together, ground time left out"]
    elapsed_minutes: Annotated[int, "Minutes from the first departure out to the last arrival, ground time included"]
    return_segments: Annotated[list[Segment], "For a round trip, the flights back, in order; empty otherwise"]
    return_layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights back"]
    return_stopover_nights: Annotated[list[bool], "Per connection back: true for a ticketed stopover with a hotel night"]
    return_flying_minutes: Annotated[int, "The flights' scheduled minutes back added together; zero one way"]
    return_elapsed_minutes: Annotated[int, "Minutes from the first departure back to the last arrival; zero one way"]


# ---------------------------------------------------------------------------------------------------------
# HANDBOOK-SPECIFIC: LSU System Permanent Memorandum 13 (PM-13), University Travel, Appendix I.
# ---------------------------------------------------------------------------------------------------------


class Scenario(Enum):
    AZALEA_SKIFF = "azalea-skiff"
    BAYOU_LANTERN = "bayou-lantern"
    BRAMBLE_QUAY = "bramble-quay"
    CATALPA_FERRY = "catalpa-ferry"
    CATTAIL_EMBER = "cattail-ember"
    CHICORY_ANVIL = "chicory-anvil"
    CRESCENT_LOOM = "crescent-loom"
    CYPRESS_IBIS = "cypress-ibis"
    DOGWOOD_TERN = "dogwood-tern"
    EGRET_SORGHUM = "egret-sorghum"
    HERON_CANE = "heron-cane"
    HICKORY_SPIRE = "hickory-spire"
    INDIGO_PELICAN = "indigo-pelican"
    LOTUS_GARNET = "lotus-garnet"
    MAGNOLIA_LEVEE = "magnolia-levee"
    MIMOSA_CAIRN = "mimosa-cairn"
    MUSCADINE_REEF = "muscadine-reef"
    NUTRIA_PRISM = "nutria-prism"
    OKRA_BEACON = "okra-beacon"
    ORIOLE_BATTURE = "oriole-batture"
    PALMETTO_GALE = "palmetto-gale"
    PECAN_MARSH = "pecan-marsh"
    PINECONE_ATLAS = "pinecone-atlas"
    PLOVER_CISTERN = "plover-cistern"
    SASSAFRAS_DUNE = "sassafras-dune"
    SORREL_HARBOR = "sorrel-harbor"
    SPARTINA_KILN = "spartina-kiln"
    SUMAC_BRIDGE = "sumac-bridge"
    TALLOW_ORCHID = "tallow-orchid"
    TUPELO_WREN = "tupelo-wren"
    WILLET_COPPER = "willet-copper"
    WILLOW_PIROGUE = "willow-pirogue"


class Approver(Enum):
    """Roles that may sign off. NONE: the decision relies on no one's sign-off, given or awaited (one for
    something else may be on file). NOT_NAMED: one is needed, but the handbook names no role."""

    NONE = "NONE"
    NOT_NAMED = "NOT_NAMED"
    SUPERVISOR_OR_FISCAL_AUTHORITY = "SUPERVISOR_OR_FISCAL_AUTHORITY"
    DEPARTMENT_HEAD = "DEPARTMENT_HEAD"
    DEAN = "DEAN"
    CAMPUS_HEAD = "CAMPUS_HEAD"
    PRESIDENT_OR_DESIGNEE = "PRESIDENT_OR_DESIGNEE"
    ENTITY_HEAD_DESIGNEE = "ENTITY_HEAD_DESIGNEE"
    GLOBAL_TRAVEL_DIRECTOR = "GLOBAL_TRAVEL_DIRECTOR"
    PROVOST = "PROVOST"
    VICE_PROVOST = "VICE_PROVOST"
    CHANCELLOR = "CHANCELLOR"
    EXECUTIVE_VICE_CHANCELLOR_ADMINISTRATION = "EXECUTIVE_VICE_CHANCELLOR_ADMINISTRATION"
    ACCOUNTING_SERVICES_CONTROLLER = "ACCOUNTING_SERVICES_CONTROLLER"
    RESEARCH_COMPLIANCE_DIRECTOR = "RESEARCH_COMPLIANCE_DIRECTOR"
    HIGH_RISK_PANEL = "HIGH_RISK_PANEL"
    RISK_MANAGEMENT_OFFICE = "RISK_MANAGEMENT_OFFICE"
    BOOKING_AGENCY = "BOOKING_AGENCY"


class Clause(Enum):
    """The handbook's sections, by heading."""

    APPLICATION = "APPLICATION"
    DEFINITIONS = "DEFINITIONS"
    CONTRACT_TRAVEL_SERVICES = "CONTRACT_TRAVEL_SERVICES"
    RECOGNIZED_PURPOSES = "RECOGNIZED_PURPOSES"
    AUTHORIZATION = "AUTHORIZATION"
    PERSONAL_CREDITS = "PERSONAL_CREDITS"
    REIMBURSEMENT_REQUESTS = "REIMBURSEMENT_REQUESTS"
    OFFICIAL_DOMICILE = "OFFICIAL_DOMICILE"
    TRANSPORTATION_METHODS = "TRANSPORTATION_METHODS"
    AIR = "AIR"
    TRAIN = "TRAIN"
    MOTOR_VEHICLE = "MOTOR_VEHICLE"
    LODGING_AND_MEALS = "LODGING_AND_MEALS"
    EXTENDED_STAY = "EXTENDED_STAY"
    OTHER_EXPENSES = "OTHER_EXPENSES"
    AIRLINE_LUGGAGE = "AIRLINE_LUGGAGE"
    INTERNATIONAL_TRAVEL = "INTERNATIONAL_TRAVEL"
    VISITORS = "VISITORS"
    SPECIAL_MEALS = "SPECIAL_MEALS"
    APPENDIX_A = "APPENDIX_A"
    APPENDIX_B = "APPENDIX_B"


class TravellerKind(Enum):
    EMPLOYEE = "EMPLOYEE"
    STUDENT = "STUDENT"
    GUEST_SPEAKER = "GUEST_SPEAKER"
    JOB_CANDIDATE = "JOB_CANDIDATE"
    SPOUSE_OF_JOB_CANDIDATE = "SPOUSE_OF_JOB_CANDIDATE"
    SPOUSE_OF_EMPLOYEE = "SPOUSE_OF_EMPLOYEE"
    CHILD_OF_EMPLOYEE = "CHILD_OF_EMPLOYEE"


class Campus(Enum):
    """The LSU campus or entity the traveller belongs to, or that invites them."""

    LSU_A_AND_M = "LSU_A_AND_M"
    LSU_AG_CENTER = "LSU_AG_CENTER"
    LSU_ALEXANDRIA = "LSU_ALEXANDRIA"
    LSU_EUNICE = "LSU_EUNICE"
    LSU_SHREVEPORT = "LSU_SHREVEPORT"
    PENNINGTON_BIOMEDICAL = "PENNINGTON_BIOMEDICAL"
    LSU_HEALTH_NEW_ORLEANS = "LSU_HEALTH_NEW_ORLEANS"
    LSU_HEALTH_SHREVEPORT = "LSU_HEALTH_SHREVEPORT"
    LSU_HEALTH_CARE_SERVICES = "LSU_HEALTH_CARE_SERVICES"


class Purpose(Enum):
    CONFERENCE = "CONFERENCE"
    RESEARCH = "RESEARCH"
    MEETING = "MEETING"
    JOB_INTERVIEW = "JOB_INTERVIEW"
    ACCOMPANYING_TRAVELLER = "ACCOMPANYING_TRAVELLER"
    PERSONAL = "PERSONAL"
    HOUSING_SEARCH = "HOUSING_SEARCH"


class Accommodation(Enum):
    """Where a documented medical accommodation for the traveller is on file."""

    NONE = "NONE"
    CIVIL_RIGHTS_TITLE_OFFICE = "CIVIL_RIGHTS_TITLE_OFFICE"
    STUDENT_DISABILITY_SERVICES = "STUDENT_DISABILITY_SERVICES"
    DOCTOR_NOTE_ONLY = "DOCTOR_NOTE_ONLY"


class Advisory(Enum):
    """The State Department's travel warning level for the place the traveller goes to."""

    NONE = "NONE"
    EXERCISE_INCREASED_CAUTION = "EXERCISE_INCREASED_CAUTION"
    RECONSIDER_TRAVEL = "RECONSIDER_TRAVEL"
    DO_NOT_TRAVEL = "DO_NOT_TRAVEL"


class AirlineReason(Enum):
    NONE = "NONE"
    FREQUENT_FLYER_MILES = "FREQUENT_FLYER_MILES"
    CONFERENCE_DISCOUNT = "CONFERENCE_DISCOUNT"


class ApprovalSubject(Enum):
    TRIP_AUTHORIZATION = "TRIP_AUTHORIZATION"
    AUTHORIZED_TRAVELLER_STATUS = "AUTHORIZED_TRAVELLER_STATUS"
    TRAVEL_OUTSIDE_UNITED_STATES = "TRAVEL_OUTSIDE_UNITED_STATES"
    HIGH_RISK_DESTINATION = "HIGH_RISK_DESTINATION"
    PREFERRED_SEAT = "PREFERRED_SEAT"
    AGENCY_EXEMPTION = "AGENCY_EXEMPTION"
    LONGER_ASSIGNMENT = "LONGER_ASSIGNMENT"


@dataclass
class Approval(Output):
    role: Annotated[Approver, "The role of the person who signed"]
    name: Annotated[str, "Their name"]
    subject: Annotated[ApprovalSubject, "What they signed"]
    traveller: Annotated[str, "The name of the traveller it covers"]
    signed_on: Annotated[str, "The day it was signed, YYYY-MM-DD"]


@dataclass
class Trip(Output):
    traveller_name: Annotated[str, "Who flies"]
    traveller_kind: Annotated[TravellerKind, "What the person flying is to the university"]
    traveller_title: Annotated[str, "Their job title or programme, or how they are related to the person they travel with"]
    campus: Annotated[Campus, "The campus or entity the trip is for"]
    origin: Annotated[Airport, "Where the flight leaves from"]
    destination: Annotated[Airport, "Where it goes"]
    destination_place: Annotated[str, "The city, and its state or country, where the trip's business is"]
    travel_date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport"]
    return_date: Annotated[str, "For a round-trip ticket, the day to fly back, YYYY-MM-DD, local at the destination; empty for a one-way ticket"]
    booking_date: Annotated[str, "Today in this world, the day the ticket is bought, YYYY-MM-DD"]
    purpose: Annotated[str, "Why the trip is made, in plain words"]
    purpose_kind: Annotated[Purpose, "The kind of trip"]
    latest_arrival_local: Annotated[
        str, "The latest time the traveller can land and still do what the trip is for, YYYY-MM-DD HH:MM, local at the destination airport; empty when any arrival works"
    ]
    requested_cabin: Annotated[Cabin, "The cabin the traveller asks for"]
    traveller_pays_up_to_cents: Annotated[
        int, "The most the traveller has agreed to pay out of pocket toward a dearer ticket, in cents; zero when nothing"
    ]
    wants_refundable: Annotated[bool, "Whether the traveller asks for a fare that can be refunded or changed without a fee"]
    requested_airline: Annotated[str, "An airline the traveller asks for, as search_flights names it; empty when none"]
    requested_airline_reason: Annotated[AirlineReason, "Why they ask for that airline; NONE when they ask for none"]
    medical_accommodation: Annotated[Accommodation, "Where a documented medical accommodation for the traveller is on file; NONE when none"]
    destination_advisory: Annotated[Advisory, "The State Department's travel warning level where the traveller goes; NONE for travel inside the United States or where only normal precautions are advised"]
    outside_quote_cents: Annotated[
        int, "A fare for the same flights that the traveller found from a seller other than the university's booking agency, in cents; zero when none"
    ]
    agency_fee_cents: Annotated[int, "The booking agency's service fee for issuing this ticket, in cents"]
    approvals: Annotated[list[Approval], "Approvals already signed for this trip"]
    notes: Annotated[list[str], "Other notes on file for this trip"]


# ---------------------------------------------------------------------------------------------------------
# SHARED (template), continued: the tools' and tasks' inputs and outputs.
# ---------------------------------------------------------------------------------------------------------


@dataclass
class TaskInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    request: Annotated[str, "The traveller's request, in their own words"]


@dataclass
class TripInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id, as the task input gives it"]


@dataclass
class TripOutput(Output):
    scenario: Annotated[Scenario, "The case id"]
    request: Annotated[str, "The traveller's request, in their own words"]
    trip: Annotated[Trip, "The trip record behind the request"]


@dataclass
class SearchInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    origin: Annotated[str, "The airport to leave from: An IATA airport code, e.g. JFK"]
    destination: Annotated[str, "The airport to fly to: An IATA airport code, e.g. JFK"]
    date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport, on or after the booking date"]
    return_date: Annotated[str, "For round-trip fares, the day to fly back, YYYY-MM-DD, local at the destination; empty for one way"]


@dataclass
class SearchOutput(Output):
    note: Annotated[str, "Where the offers come from, and a word when this case lists none for the search"]
    currency: Annotated[str, "The currency of every fare, as an ISO code"]
    offers: Annotated[list[Offer], "Every offer leaving on that local date, in departure order"]


@dataclass
class BookingOutput(Output):
    decision: Annotated[
        Decision,
        "BOOK: buy offer_id now. REFUSE: buy nothing, because the organisation buys no ticket at all for this request. "
        "FLAG_FOR_APPROVAL: hold offer_id and buy nothing yet, because someone must approve it first or "
        "the handbook's words leave the answer open",
    ]
    offer_id: Annotated[str, "The offer bought or held, exactly as search_flights listed it; empty when refusing"]
    cabin: Annotated[Cabin, "That offer's cabin; NONE when refusing"]
    reason_code: Annotated[ReasonCode, "Why, from the closed list"]
    approver: Annotated[
        Approver,
        "The role whose sign-off this decision relies on, whether already on file or still awaited; NONE when "
        "this decision relies on no one's sign-off, even if a sign-off for something else is on file; NOT_NAMED "
        "when a sign-off is needed but the handbook names no role",
    ]
    clause: Annotated[Clause, "The handbook section the decision rests on"]


@dataclass
class SolveOutput(Output):
    trip: Annotated[Trip, "The trip record"]
    offers: Annotated[list[Offer], "Every offer on the trip's route and date"]
    decision: Annotated[Decision, "The correct decision"]
    offer_ids: Annotated[list[str], "Every offer id that is a correct choice; empty when refusing"]
    cabins: Annotated[list[Cabin], "Every correct cabin"]
    reason_codes: Annotated[list[ReasonCode], "Every accepted reason"]
    approvers: Annotated[list[Approver], "Every accepted approver"]
    clauses: Annotated[list[Clause], "Every accepted section"]
    unclear_phrase: Annotated[str, "For a hold over unclear words, those words; empty otherwise"]
    explanation: Annotated[str, "How the answer key reached the answer"]


@dataclass
class FieldHelp(Output):
    name: Annotated[str, "The trip record field's name"]
    kind: Annotated[str, "Its type"]
    description: Annotated[str, "What it means"]


@dataclass
class RequirementsInput(Output):
    topic: Annotated[Topic, "ALL for everything, FIELDS for the trip record's fields, AIRPORTS for the airport list"]


@dataclass
class RequirementsOutput(Output):
    fields: Annotated[list[FieldHelp], "The trip record's fields; empty for AIRPORTS"]
    conventions: Annotated[list[str], "How times, dates, fares and seats work in this world; empty for AIRPORTS"]
    airports: Annotated[list[Airport], "The airports the simulated world knows; empty for FIELDS"]


TOOLS = {
    Tool.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Tool.GET_TRIP: (TripInput, TripOutput),
    Tool.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Tool.SOLVE_BOOKING: (TaskInput, SolveOutput),
}
TASKS = {
    Task.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Task.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Task.BOOK_FLIGHT: (TaskInput, BookingOutput),
}
