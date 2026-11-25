# Validation notes: lsu-pm13-flight-policy (paid wave 1 validation w1v3, 2026-11-25)

Run: `efficient_corporate_travel_agent/pilot/ladder/runs/validation_w1v3_2026-11-25/lsu-pm13-flight-policy@w1v3/`,
arm `full`, DeepSeek V4 Flash, temperature 0, max_steps 6, max_tokens 8192, one run per scenario, at plugin head
69227b4 (after the approver rule 4' and the declined-request sentence). Line numbers are lines of
`src/plugin/data/policy.txt`.

## Results

28/32 valid (87.5%), **easy 6/6**. By category: boundary 6/8, distractor 3/3, easy 6/6, flag 2/4, hidden 3/3,
multi 5/5, refusal 3/3. All four failures are model slips, so no key changed; re-scoring the stored submissions at
this commit gives the same **28/32**.

## Every failure, classified

| scenario | category | submitted vs key | class | evidence |
|---|---|---|---|---|
| catalpa-ferry | boundary_twin | right offer (United coach 82U5-DK9C), reason UPGRADE_COST_NOT_NOMINAL; key UPGRADE_NOT_ELIGIBLE only | model slip | The single-code key the 2026-11-24 review asked to look at. The model found the ground: "The University would need to cover $1 of the upgrade. But the University doesn't cover upgrades" (line 402). It then named the code for the size of the cost: "the upgrade cost ($412) is not nominal and exceeds the traveller's willingness to pay". LSU's handbook has no nominal-cost test (no "nominal" anywhere); the code is a decoy borrowed from Thornton's upgrade-cost rule. Read against the facts it points the wrong way, since the shortfall is $1. The ground for declining is line 402 (upgrades at University expense are not permitted), which UPGRADE_NOT_ELIGIBLE names. Not loosened; LOWEST_FARE stays off (declined-request rule). |
| cattail-ember | flag | BOOK American coach, UPGRADE_NOT_ELIGIBLE; key FLAG (coach or premium), UNCLEAR_POLICY_TEXT | model slip | The same as 2026-11-24. It saw the preferred-seat approval and settled it: "this pertains to preferred seating within economy, which is a separate fee ... doesn't justify premium economy cabin." It never read definition V (lines 157-159: "Seats for purchase on an aircraft at an additional cost ... more legroom"), which makes a premium economy seat a defensible preferred seat. That seat would be reimbursable under lines 429-433: $55 is 8.6% of the fare, under both limits. |
| dogwood-tern | flag | BOOK Air NZ business, TRAVELER_PAYS_UPGRADE; key FLAG (both offers), UNCLEAR_POLICY_TEXT | model slip (borderline: booked in both paid runs) | The same as 2026-11-24: "the university will pay up to 110% of coach ... The traveler chips in $80." It took the cap reading of lines 423-424 and never weighed the condition reading, under which business above 110% is not allowed. On that reading the traveller owes the whole $240 (lines 400-401), over the $100 offered. The text reads both ways, so the key stays. The cap reading is the one the model takes every time. If the next run books again, the lead should decide whether to make it a BOOK under a new id. |
| palmetto-gale | boundary_twin | BOOK ANA business CVLK-LDRT, LONG_FLIGHT_APPROVED; key ANA coach, LONG_FLIGHT_CONDITION_NOT_MET / UPGRADE_NOT_ELIGIBLE | model slip (a limit rationalised away) | It did the arithmetic right: "1629/1480 = 1.10068. So 110.07% ... it exceeds 110% by $1 ... strictly, the condition is not met", then "Given the tiny overage, I think the intended answer is ... business." Line 424 says "not to exceed 110%". On the cap reading the traveller would owe $1, and the request says "I won't pay any of it myself". On the condition reading business is not allowed. So coach is right on both readings (Q3: ANA coach is the lowest fare, and the flight is over 10 hours). The twin heron-cane ($1,628, exactly 110%) passed. |

## Fixes

None. No rule, scenario or README change; this commit adds these notes only.

Cross-plugin checks from wave 2:

- **Long-flight business:** every LSU key that grants business on lines 423-427 already accepts both
  `INTERNATIONAL_LONG_FLIGHT` and `LONG_FLIGHT_APPROVED` (`rules.py` `business`, both branches).
- **Route codes:** LSU has no booked connection that declines a nonstop, and no key uses `ALTERNATE_ROUTE_*` or
  `COST_SAVINGS`. The one keyed connection, hickory-spire, declines business, not a route.

## Q2

Nothing changed, so the always-cheapest agent still passes **7/32 (22%)** (`MAX_PASS_ALWAYS_LOWEST = 7`,
measured by `test_verifier.py`).

## Re-run

None needed: no record or request changed. Optional variance checks: dogwood-tern (whether the cap reading persists)
and catalpa-ferry (whether the specific code still misses).

## Checks

At this commit: `uv run pytest -q` (252 passed), `uv run ruff check .`, `uv lock --check`, `check_shared.py`,
`tools/stock_verify.py` (0 failures), stock `nanoagent plugin inspect .` (exit 0).
