# Evidence and trip states

## Evidence states

Use these states for each material claim or component:

| State | Meaning | Minimum evidence |
| --- | --- | --- |
| `UNKNOWN` | No usable data. | None. |
| `ASSUMED` | Working hypothesis, not validated. | Assumption and owner. |
| `DECIDED` | Traveler preference or constraint. | Explicit traveler decision and date when material. |
| `RESEARCHED` | Supported external information, not priced or bought. | Applicable source and consultation date. |
| `QUOTED` | Price and terms observed at a point in time. | Seller, operator, scope, date/time, currency, taxes/extras status. |
| `VERIFIED` | Current fact checked with a competent source. | Official or authoritative source, applicability, consultation date. |
| `RESERVED` | Provider accepted a booking for the correct traveler/date/service. | Confirmation or booking reference and status. |
| `PAID` | Payment accepted and reconciled. | Provider receipt or payment evidence. |
| `STALE` | Evidence exceeded its useful review window. | Previous evidence plus reason it needs refresh. |
| `CONFLICTING` | Relevant sources or records disagree. | Both claims and unresolved applicability. |
| `CANCELLED` | Previous reservation is no longer valid. | Cancellation evidence and refund status. |

Do not collapse facets. Example: `event occurrence = VERIFIED`, `traveler intent = DECIDED`, `ticket price = QUOTED`, `traveler ticket = RESERVED`.

## Confirmation rules

A fact is confirmed only when the evidence matches its full scope. Check traveler, date, local time, timezone, route, fare, room, ticket, and seller as applicable.

An explicit statement from the traveler or an established first-party traveler profile is sufficient for `DECIDED`, unless that source marks the statement tentative or a later decision supersedes it. `DECIDED` does not prove an external rule, price, or booking.

A reservation requires provider acceptance. A saved cart, screenshot, aggregator result, pending payment, or user intention is not a reservation.

A quote requires enough information to reproduce the comparison. If baggage, taxes, mandatory fees, payment surcharge, room occupancy, or cancellation terms are unknown, mark those facets `UNKNOWN` even if a base price exists.

## Staleness

Set review windows from volatility and consequence rather than one universal age:

- border, visa, authorization, and health requirements: research, pre-purchase, 30 days, and 7 days;
- flight and hotel prices: short-lived; recheck at checkout;
- transport schedules: when sales open, 30 days, 7 days, and 24 hours;
- events and attractions: pre-purchase, 30 days, and 7 days;
- strikes and alerts: 7 days and 24 hours;
- weather: 7 days and 24 hours;
- exchange rate: each quote and each payment.

Escalate refresh frequency when the trip overlaps a launch window, election, strike notice, severe weather season, major event, or regulatory transition.

## Trip maturity states

### `IDEA`

Use when the concept exists but travelers, dates, hard constraints, route, or basic feasibility remain materially incomplete.

### `INVESTIGATED`

Require:

- travelers, dates, route, hard constraints, and essential events are identified;
- basic border, health, logistics, budget, and safety feasibility has been investigated;
- major gaps and dependencies are visible;
- no implication that estimates are current quotes.

### `QUOTED`

Require every essential component to have at least one comparable, sufficiently current quote with seller/operator, scope, currency, major extras, and key terms. Essential components normally include international and internal transport, lodging, critical events, insurance when required by the plan, and a consolidated budget.

### `READY TO BUY`

Require:

- no unresolved CRITICAL finding;
- every HIGH finding resolved or explicitly accepted by the travelers;
- identity and entry requirements verified;
- dependencies and availability checked together;
- final comparable totals include required baggage, taxes, fees, and dated conversions;
- cancellation/change policies reviewed;
- purchase order and fallback plan documented;
- explicit human approval exists for the proposed plan.

This state does not authorize execution.

### `BOOKED`

Require all essential components to be reserved with valid confirmations, actual spend reconciled, uncovered nights or segments eliminated, and the operational plan through return documented. Report partial coverage separately, for example `essential reservations: 6/9`.

## State calculation

Return the highest fully satisfied state. One advanced component cannot lift the whole trip. Report two separate fields:

```text
Maturity: INVESTIGATED
Active workflow: QUOTING IN PROGRESS
Essential reservations: 0/9
```

Never downgrade a sound traveler decision merely because it is not booked; classify the decision and booking facets separately.
