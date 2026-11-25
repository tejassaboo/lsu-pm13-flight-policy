# LSU PM-13 Flight Policy

**No affiliation with Louisiana State University.** The handbook is LSU System Permanent Memorandum 13 (PM-13),
*University Travel* (policy digest last revised July 2, 2026; Appendix I effective October 1, 2026; Appendices A
and B dated July 1, 2026 - June 30, 2027), a public university-system document, bundled verbatim for research.
Do not publish this plugin until it has passed validation (MASTER_PLAN section 4).

A `nanoagent.plugin/v0001` plugin. An agent handles one flight booking request under the real regulations: it
reads the trip record, searches a simulated flight world and submits **BOOK**, **REFUSE** or
**FLAG_FOR_APPROVAL** with the offer, cabin, reason, approver and section. A deterministic Python verifier, with
no LLM, rebuilds the offers and the regulations' answer itself and checks every field. Built from the
original-handbook template (`handbook_plugins/_template`); `tests/build_scenarios.py` writes the scenario files
(an authoring aid; the JSON files are the truth).

## The handbook and the harness flag

The frozen text (`src/plugin/data/policy.txt`, 17,762 words, 1,891 lines, sha256 `8f5a1a40...ae2d765`, equal to
`pilot_work/originals/lsu-pm13/frozen/SHA256SUMS`) is never paraphrased, and the task text restates no rule.
Under stock NanoAgent the agent does not see it: the plugin then runs as the `off` baseline. The
`harness.policy` switch of the NanoAgent fork (github.com/tejassaboo/nanoagent, branch `policy-switch`) adds it
to the system prompt: `harness.policy: full` adds all of it, and the selection methods add parts of it. These
plugins are meant to run with `query: instructions+input`, so a selector sees the traveller's request.

**Size.** At 1.33 tokens a word the regulations alone are about 23,600 tokens. Under `full` the first call
carries about 28,200 input tokens (regulations, task instructions about 220, tool and submit schemas about
4,300 at 4 characters a token, the request), and the last call up to about 31,000 as tool results accumulate.
A run makes 3 calls (`get_trip`, `search_flights`, `submit`): about 86,000 to 88,000 input tokens per run
(output tokens not counted). Every single call fits under the hosted cap of 65,536 tokens, but a run's
cumulative input crosses it during the third call in all 32 cases, so `full` cannot finish hosted: run it
locally with a raised cap.

## Task

- **Input:** `TaskInput`: `scenario` (one of 32 case ids) and `request`, the traveller's own words.
- **Steps:** `get_trip`, then `search_flights` on the trip's origin, destination and travel date (with the
  return date for the two round-trip cases), then `submit`.
- **Output:** `BookingOutput`: `decision`, `offer_id` (empty when refusing), `cabin` (`NONE` when refusing),
  `reason_code`, `approver` and `clause`, each from a closed list. The reason list is the template's shared list
  plus `AGENCY_EXEMPTION_NOT_MET`, `PERSONAL_DESTINATION_NOT_COVERED`, `CANDIDATE_TRIP_NOT_COVERED` and
  `DOMESTIC_TRAVEL_COACH`. Fares are in cents of US dollars (`currency: USD`).
- **Success:** every field is one the answer key accepts. Score = fields right / 6.
- **Hidden facts:** none (`answer_key_inputs` unused). Whether a trip is international is for the agent to work
  out from definition M and the airports.

| Scenario | Category | Expected decision (offer slot; cabin) | Reason | Approver | Clause (frozen lines) |
|---|---|---|---|---|---|
| `bayou-lantern` | easy | BOOK (united-premium; PREMIUM_ECONOMY) | TRAVELER_PAYS_UPGRADE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or TRANSPORTATION_METHODS (399-402) |
| `cypress-ibis` | easy | BOOK (early-economy; ECONOMY) | LOWEST_FARE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or DEFINITIONS or TRANSPORTATION_METHODS (113-115, 399-402) |
| `egret-sorghum` | easy | BOOK (united-business; BUSINESS) | MEDICAL_NEED | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or TRANSPORTATION_METHODS (402-406) |
| `magnolia-levee` | easy | BOOK (korean-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED or UPGRADE_WITHIN_FARE_MARGIN | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 423-427, 1072-1074, 1402, 1452-1456) |
| `pecan-marsh` | easy | BOOK (united-economy; ECONOMY) | LOWEST_FARE or UPGRADE_NOT_ELIGIBLE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or DEFINITIONS or TRANSPORTATION_METHODS (157-159, 399-402, 402-406, 429-433) |
| `tupelo-wren` | easy | BOOK (united-economy; ECONOMY) | LOWEST_FARE | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 113-115, 399-402, 1072-1074, 1402, 1452-1456) |
| `azalea-skiff` | boundary_twin | BOOK (united-economy; ECONOMY) | DOMESTIC_TRAVEL_COACH or LONG_FLIGHT_CONDITION_NOT_MET or LOWEST_FARE or UPGRADE_NOT_ELIGIBLE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or DEFINITIONS or TRANSPORTATION_METHODS (102-104, 399-402, 423-427) |
| `catalpa-ferry` | boundary_twin | BOOK (united-economy; ECONOMY) | LOWEST_FARE or UPGRADE_NOT_ELIGIBLE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or TRANSPORTATION_METHODS (399-402, 402-406) |
| `heron-cane` | boundary_twin | BOOK (ana-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED or UPGRADE_WITHIN_FARE_MARGIN | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 399-402, 423-427, 1072-1074, 1402, 1452-1456) |
| `indigo-pelican` | boundary_twin | BOOK (united-business; BUSINESS) | TRAVELER_PAYS_UPGRADE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or TRANSPORTATION_METHODS (399-402, 402-406) |
| `palmetto-gale` | boundary_twin | BOOK (ana-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or LOWEST_FARE or UPGRADE_NOT_ELIGIBLE | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 399-402, 423-427, 1072-1074, 1402, 1452-1456) |
| `sassafras-dune` | boundary_twin | BOOK (swiss-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or LOWEST_FARE or UPGRADE_NOT_ELIGIBLE | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 423-427, 1072-1074, 1402, 1452-1456) |
| `sumac-bridge` | boundary_twin | BOOK (united-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED or UPGRADE_WITHIN_FARE_MARGIN | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 423-427, 1072-1074, 1402, 1452-1456) |
| `willow-pirogue` | boundary_twin | BOOK (swiss-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED or UPGRADE_WITHIN_FARE_MARGIN | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 423-427, 1072-1074, 1402, 1452-1456) |
| `bramble-quay` | multi_rule | BOOK (aeromexico-economy; ECONOMY) | LOWEST_FARE | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or PROVOST or SUPERVISOR_OR_FISCAL_AUTHORITY or VICE_PROVOST | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (95-99, 102-104, 113-115, 399-402, 1072-1074, 1075-1080, 1402, 1444-1447, 1452-1456) |
| `chicory-anvil` | multi_rule | BOOK (qantas-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or TRAVELER_PAYS_UPGRADE | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 399-402, 423-427, 1072-1074, 1402, 1452-1456) |
| `crescent-loom` | multi_rule | BOOK (korean-economy; ECONOMY) | LOWEST_FARE | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 113-115, 369-371, 399-402, 1072-1074, 1402, 1452-1456) |
| `hickory-spire` | multi_rule | BOOK (aircanada-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or LOWEST_FARE or UPGRADE_NOT_ELIGIBLE | ENTITY_HEAD_DESIGNEE or GLOBAL_TRAVEL_DIRECTOR or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL or TRANSPORTATION_METHODS (102-104, 399-402, 423-427, 1072-1074, 1402, 1452-1456) |
| `okra-beacon` | multi_rule | BOOK (american-business; BUSINESS) | NO_ECONOMY_SEATS_URGENT | BOOKING_AGENCY or NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or TRANSPORTATION_METHODS (369-371, 399-402, 406-408) |
| `lotus-garnet` | hidden_clause | BOOK (alaska-economy; ECONOMY) | LOWEST_FARE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or DEFINITIONS or TRANSPORTATION_METHODS or VISITORS (113-115, 399-402, 1183-1187) |
| `mimosa-cairn` | hidden_clause | BOOK (american-business; BUSINESS) | MEDICAL_NEED | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or TRANSPORTATION_METHODS (61-62, 402-406) |
| `sorrel-harbor` | hidden_clause | BOOK (united-economy; ECONOMY) | LOWEST_FARE or LOYALTY_PROGRAM_PREFERENCE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or DEFINITIONS or TRANSPORTATION_METHODS (113-115, 399-402, 440-444) |
| `muscadine-reef` | distractor | BOOK (southwest-economy; ECONOMY) | LOWEST_FARE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or DEFINITIONS or TRANSPORTATION_METHODS (113-115, 399-402, 468-470) |
| `pinecone-atlas` | distractor | BOOK (united-economy; ECONOMY) | AGENCY_EXEMPTION_NOT_MET or LOWEST_FARE | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or CONTRACT_TRAVEL_SERVICES or DEFINITIONS or TRANSPORTATION_METHODS (113-115, 198-201, 399-402) |
| `tallow-orchid` | distractor | BOOK (delta-economy; ECONOMY) | LOWEST_FARE or REFUNDABLE_FARE_NOT_ALLOWED | NONE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or DEFINITIONS or TRANSPORTATION_METHODS (113-115, 399-402) |
| `nutria-prism` | refusal | REFUSE (none; NONE) | PERSONAL_DESTINATION_NOT_COVERED or PERSONAL_TRAVEL_NOT_COVERED | NONE | AIR or AUTHORIZATION or TRANSPORTATION_METHODS (241-243, 458-460) |
| `spartina-kiln` | refusal | REFUSE (none; NONE) | CANDIDATE_TRIP_NOT_COVERED or OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED | NONE | VISITORS (1187-1190) |
| `willet-copper` | refusal | REFUSE (none; NONE) | COMPANION_NOT_COVERED or OUTSIDE_POLICY_SCOPE | NONE | DEFINITIONS or RECOGNIZED_PURPOSES or SPECIAL_MEALS (209-212, 1202) |
| `cattail-ember` | flag | FLAG_FOR_APPROVAL (american-economy, american-premium; ECONOMY or PREMIUM_ECONOMY) | UNCLEAR_POLICY_TEXT | NOT_NAMED or PRESIDENT_OR_DESIGNEE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or DEFINITIONS or TRANSPORTATION_METHODS (43-44, 157-159, 399-402, 402-406, 429-433) |
| `dogwood-tern` | flag | FLAG_FOR_APPROVAL (airnz-business, airnz-economy; BUSINESS or ECONOMY) | UNCLEAR_POLICY_TEXT | NOT_NAMED or PRESIDENT_OR_DESIGNEE or SUPERVISOR_OR_FISCAL_AUTHORITY | AIR or TRANSPORTATION_METHODS (43-44, 399-402, 423-427) |
| `oriole-batture` | flag | FLAG_FOR_APPROVAL (united-economy; ECONOMY) | APPROVAL_REQUIRED | CHANCELLOR or ENTITY_HEAD_DESIGNEE | APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL (102-104, 399-402, 1072-1074, 1471, 1511-1514) |
| `plover-cistern` | flag | FLAG_FOR_APPROVAL (aeromexico-economy; ECONOMY) | APPROVAL_REQUIRED | PROVOST or VICE_PROVOST | APPENDIX_B or DEFINITIONS or INTERNATIONAL_TRAVEL (95-99, 399-402, 1075-1080, 1402, 1444-1447) |

Mix (EDGE_CASES.md 5.2, 32 row): 6 easy, 8 boundary twins, 5 multi-rule, 3 hidden clause, 3 distractor, 3
refusal, 4 flags (12.5%; the 15% cap is 4). Decisions: 25 BOOK (9 business, 1 premium economy, 15 economy),
3 REFUSE, 4 FLAG_FOR_APPROVAL. Twin pairs: 600 against 601 segment minutes (`sassafras-dune`,
`willow-pirogue`), business at 110.00% against 110.07% of coach (`heron-cane`, `palmetto-gale`), Honolulu against
Tokyo on the same 705-minute nonstop (`azalea-skiff`, `sumac-bridge`), and the traveller covering the whole
business-coach difference or a dollar less (`indigo-pelican`, `catalpa-ferry`); plus two contrast pairs, a
candidate's spouse against an employee's (`lotus-garnet`, `willet-copper`) and personal days at the business
destination against a personal destination (`muscadine-reef`, `nutria-prism`). Unclear words are each one flag
with clear twins on both sides: "not to exceed 110% of the coach rate" when the traveller will pay the part
above 110% but not the whole difference (`dogwood-tern`; twins `heron-cane`, `palmetto-gale`), and whether a
premium economy seat is a "preferred seat" (definition V and lines 429-433) or an upgrade (`cattail-ember`;
twins `pecan-marsh`, `bayou-lantern`). `oriole-batture` (LSU Alexandria: the Chancellor, Appendix B) and
`plover-cistern` (a Do Not Travel region: the Provost or Vice Provost) are approval-required holds, never the
same as "no compliant offer". On a BOOK the approver accepts `NONE` and the supervisor or fiscal authority whose
trip authorization the booking relies on (lines 232-237), plus, for travel outside the United States, the
Entity Head designee and the campus's Appendix B title (and the high-risk approvers where one was needed). The
cabin is graded as the chosen offer's own cabin. Degenerate agents: always-flag passes 2 (the two unclear-word
holds, given the held offer), always-book-the-cheapest-seat passes 14 (the cases whose answer is the cheapest
seat listed).

Duration (`rules.over`): per segment, as the agency's itinerary documents it ("an international flight segment
is more than 10 hours in duration", lines 423-427), strictly over 600 scheduled minutes, out and back; segments
are never added and layovers never count. Whether the trip is international (definition M, lines 102-104) and
the segment an international one is decided in `rules.solve`, which raises on combinations no scenario needs (a
long domestic segment on an international trip, a ticket mixing long and short segments). Background offers:
three per search domestically, none on international searches or where an arrival deadline makes timing
matter.

The world has no Louisiana airport, so travellers leave from Houston (IAH) or from where their trip takes them,
and inbound visitors fly into Houston; the trip record's `destination_place` names the real place of business.

## Tools

| Tool | Does | Code |
|---|---|---|
| `booking_requirements` | The trip record's fields, the world's conventions (local times, dates, fares, sold-out seats) and its airports | `src/plugin/guide.py` |
| `get_trip` | A case's request and trip record: traveller, route, dates, purpose, campus, requested cabin, what the traveller will pay, approvals on file, notes | `src/plugin/tools.py` |
| `search_flights` | Every offer on a route and local date (one way, or round trip with `return_date`): pinned scenario offers plus seeded background offers | `src/plugin/world.py` |
| `solve_booking` | The answer key (`rules.solve`), the agent task's `reference`, never shown to the agent | `src/plugin/rules.py` |

| Task | Does | Runner |
|---|---|---|
| `book-lsu-flight` | Handles one booking request | `agent`, with `get_trip` and `search_flights`; reference `solve_booking` |
| `booking-requirements` | Shows `booking_requirements` | `tool` |
| `search-flights` | Shows `search_flights` | `tool` |

## Layout

- `contract.py`: the template's shared contract plus this handbook's scenario ids, approvers, sections, reason codes and trip record.
- `src/plugin/`: `world.py` (the simulated world: real airports and airline hubs, distance-based times
  and fares, hash-seeded background offers and opaque offer ids), `scenarios.py`, `guide.py`,
  `answer.py`, `tools.py`, `rules.py` (this handbook's rules, citing frozen lines), `__main__.py`.
- `src/plugin/data/`: `policy.txt` (frozen), `handbook.json`, `scenarios/*.json`.
- `verifier/`: byte-identical copies of `world.py`, `scenarios.py`, `guide.py`, `answer.py` and
  `rules.py`, plus `booking.py` (`verify_task`) and `tools.py` (`verify_input`, `verify_output`).
- `tests/`: the template's acceptance suite; `tests/plugin_spec.py` holds this handbook's settings; `tests/build_scenarios.py` writes the scenario files (an authoring aid, not a test).

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv lock --check
python3 ../_template/check_shared.py .
# from a NanoAgent checkout (read-only use):
nanoagent plugin inspect <this folder>
nanoagent plugin pack <this folder> /tmp/lsu-pm13-flight-policy.tar.gz
# from this folder, with that checkout's Python:
/path/to/nanoagent/nanoagent/.venv/bin/python ../_template/tools/stock_verify.py
```

Offline: `hosts: []`, an empty `.env`, `write: []`, no clock (each case fixes its `booking_date`, on or after November 24, 2026).
