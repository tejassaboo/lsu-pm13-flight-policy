# Re-validation notes, 2026-11-24 evening

Source: `efficient_corporate_travel_agent/pilot/ladder/runs/revalidation_2026-11-24/analysis.json`
(`lsu-pm13-flight-policy@v2`), with each run's `messages.json` beside it. Model: deepseek-v4-flash-0731, full
harness, max_steps 6.

27 runs were graded and 5 passed. 22 failed. Another 5 runs (`bayou-lantern`, `catalpa-ferry`, `cypress-ibis`,
`oriole-batture`, `spartina-kiln`) ended in an upstream 429 rate limit before they submitted, so they have no
verdict. They are not failures.

## The approver amendment (template SYNC_NOTES 4')

On a BOOK, the sign-offs are already on file: the trip authorization (lines 232-237), plus the Entity Head
designee's and any high-risk approval for travel outside the United States. Such a BOOK now accepts `NONE` beside
those roles (`rules.relied`, `BASE` in `tests/build_scenarios.py`). Holds still accept only the awaited roles.
Refusals keep 4(b). This changes the accept sets of all 25 BOOK scenarios.

17 of the 22 failures had only `approver` wrong (`NONE`), and the amendment explains them alone. They now pass:
azalea-skiff, bramble-quay, crescent-loom, egret-sorghum, heron-cane, hickory-spire, indigo-pelican,
lotus-garnet, magnolia-levee, mimosa-cairn, muscadine-reef, palmetto-gale, pecan-marsh, pinecone-atlas,
sassafras-dune, sorrel-harbor and sumac-bridge.

`MAX_PASS_ALWAYS_LOWEST` goes from 0 to 14. Always-book-the-cheapest-seat with `NONE` now passes the 14 cases
whose answer is the cheapest seat listed.

## Every failure the approver rule does not explain, classified

All five also answered `NONE` on the approver. Under 4' that is right on the three BOOKs (okra-beacon,
tupelo-wren and tallow-orchid's key) and wrong on the two holds.

| scenario | category | submitted vs key | class | evidence | fix |
|---|---|---|---|---|---|
| cattail-ember | flag | BOOK american-economy, UPGRADE_NOT_ELIGIBLE, NONE; key FLAG (american-economy, american-premium), UNCLEAR_POLICY_TEXT | model slip | It weighed the preferred-seat approval and settled on one reading: "a preferred seat is a seat with extra legroom ... That doesn't allow premium economy cabin". It never saw that definition V (lines 157-159: "Seats for purchase ... at an additional cost ... more legroom") makes a premium economy seat a defensible preferred seat. That seat would be reimbursable under lines 429-433 within the lesser of 10% and $100 (5500 cents is 8.6%). Same pattern as Thornton ember-trellis and velvet-prairie. | none |
| dogwood-tern | flag | BOOK airnz-business, TRAVELER_PAYS_UPGRADE, NONE; key FLAG (both offers), UNCLEAR_POLICY_TEXT | model slip | "not to exceed 110% of the coach rate ... is a cap on reimbursement. The traveler covers the rest" ($80 of $100 offered). It took the cap reading of lines 423-424 and never considered the condition reading, under which business above 110% is not allowed and the traveller would owe the whole $240. Same pattern as Thornton ember-trellis. | none |
| okra-beacon | multi_rule | BOOK **ZX69-XC6S** (american-economy, sold out), cabin BUSINESS, NO_ECONOMY_SEATS_URGENT; key SB3Y-KJUA (american-business) | model slip | The reasoning is right: no seat below business lands by noon (lines 406-408), and it wants "AA business at $745". But it wrote "book AA 1175 business (offer ZX69-XC6S, business)", which is the id of the sold-out AA economy offer on the same flight. SB3Y-KJUA is listed right after it with `cabin: BUSINESS`. The cabin it submitted (BUSINESS) contradicts the offer it submitted. | none (approver now accepts NONE as well) |
| tallow-orchid | distractor | REFUSE, REFUNDABLE_FARE_NOT_ALLOWED; key BOOK delta-economy (non-refundable lowest fare), LOWEST_FARE or REFUNDABLE_FARE_NOT_ALLOWED | model slip | It found the right rule (line 114: lowest logical fares "are non-refundable, penalty tickets"). It also said itself that "the organization would want to get them there ... book the cheapest fare". Then it refused because "the traveler specifically wants refundable". The trip is authorized and the request asks for a ticket. REFUSE means "buys no ticket at all for this request", and nothing in the request says to buy nothing if the fare cannot be refundable. The key's REFUNDABLE_FARE_NOT_ALLOWED was already accepted. | none |
| tupelo-wren | easy | BOOK HTPX-9YWA (Air Canada 09:10, lands 13:05, $418), LOWEST_FARE; key WWD6-SW77 (United 13:25, lands 17:20, $396.50) | **scenario defect (ambiguous facts)** | The request said "presenting at a library science conference in Toronto on Monday, December 14", and the trip flies that same Monday with no `latest_arrival_local`. The model reasoned: "Arriving at 17:20 on the day of the conference where you need to present seems like undo inconvenience", which is definition P (lines 113-114: "cheapest available ... without causing undo inconvenience") together with lines 369-371 ("accomplish the purpose of the travel"). Read that way, the 17:20 arrival is not the lowest logical fare, so the key's offer is unfair on these facts. | Request reworded: the conference "opens Tuesday, December 15", and the traveller "will fly out of Houston the day before, Monday, December 14". Same flights, fares, approvals and answer; the id is kept. Its flag twin `oriole-batture` had the identical sentence and the same key offer, and got the same rewording to keep the pair aligned (its run was lost to the 429, so this is preventive). |

No grader defects. No failure needed the lotus-garnet/spartina-kiln Louisiana-airport idea.

A latent risk the run did not hit: `mimosa-cairn` ("presenting at the agricultural economics meeting in
Phoenix on Thursday, December 10", flying that day) keys the 11:30 departure over a 09:05 one, with no arrival
deadline. The model got the offer right this time and failed only on the approver, so it is unchanged.

## Files changed

- `src/plugin/rules.py`, `verifier/rules.py` (byte-identical): `relied` adds `NONE` to a BOOK's on-file roles.
- `tests/build_scenarios.py`: `BASE` includes `NONE`; the tupelo-wren and oriole-batture request text.
- `tests/plugin_spec.py`: `MAX_PASS_ALWAYS_LOWEST = 14`.
- `README.md`: approver column regenerated from the scenario JSON; approver and degenerate-agent paragraph.
- Scenario JSON. Accept sets changed (`NONE` added) in azalea-skiff, bayou-lantern, bramble-quay, catalpa-ferry,
  chicory-anvil, crescent-loom, cypress-ibis, egret-sorghum, heron-cane, hickory-spire, indigo-pelican,
  lotus-garnet, magnolia-levee, mimosa-cairn, muscadine-reef, okra-beacon, palmetto-gale, pecan-marsh,
  pinecone-atlas, sassafras-dune, sorrel-harbor, sumac-bridge, tallow-orchid, tupelo-wren and willow-pirogue.
  The request was reworded in tupelo-wren and oriole-batture.

World facts are unchanged. `world_diff.py --plugins` against HEAD shows no pinned-search differences; only the
trip (request) of the two reworded cases differs, plus the 25 answer keys that gained `NONE`.
