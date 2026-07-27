# Risk and deliverable contracts

## Severity

| Severity | Use when | Gate effect |
| --- | --- | --- |
| `CRITICAL` | Could prevent entry, boarding, the trip, or an essential event; create immediate health/safety exposure; or cause severe financial loss. | Blocks `READY TO BUY`. |
| `HIGH` | Could cause major cost, lost nights, missed connections, lost coverage, or material disruption. | Must be resolved or explicitly accepted. |
| `MEDIUM` | Reduces quality, comfort, efficiency, or budget accuracy with a reasonable workaround. | Track with owner and trigger. |
| `LOW` | Optimization or documentation improvement with little immediate consequence. | Does not block. |

For a numerical matrix use probability 1-5 and impact 1-5:

- 20-25 CRITICAL;
- 12-19 HIGH;
- 6-11 MEDIUM;
- 1-5 LOW.

Escalate manually for legal, health, safety, boarding, or essential-event consequences.

## Finding contract

```text
ID:
Severity:
Category:
Finding:
Evidence state:
Evidence and consultation date:
Consequence:
Required action:
Owner:
Depends on:
Deadline or trigger:
Blocks readiness: yes/no
Status:
```

Every CRITICAL and HIGH finding requires an owner, dependency, and deadline or review trigger.

## Risk register

Track:

- risk and affected travelers/components;
- probability, impact, inherent severity;
- warning signal or trigger;
- prevention;
- contingency response;
- owner and mitigation cost;
- residual severity;
- traveler acceptance and date when applicable.

## Decision log

Track decision ID, date, decision, alternatives, reason, evidence, decision makers, assumptions, accepted risks, affected components, reopening trigger, and status (`PROPOSED`, `APPROVED`, `SUPERSEDED`, `REVOKED`).

## Purchase order logic

Order decisions and proposed purchases from these factors:

1. eligibility and legal feasibility;
2. hard date or essential-event dependency;
3. scarcity and sales window;
4. dependency on another component;
5. reversibility and cancellation protection;
6. price volatility and financial exposure;
7. fallback availability.

Do not present one universal sequence as mandatory. Explain why each trip's sequence follows its dependency graph. Never execute the sequence under this skill.

## Standard advisor report

Use this order, omitting empty sections:

1. **Executive result**: maturity, active workflow, reservation coverage, verdict.
2. **Decided / verified / quoted / reserved**: separate columns or groups.
3. **Priority findings**: CRITICAL first, then dependency order.
4. **Stale assumptions and conflicts**.
5. **Research completed and still required**.
6. **Delegated tasks**: worker, scope, status, and next action.
7. **Budget**: original currencies, dated conversion, per person/group, paid/quoted/remaining, contingency.
8. **Risk matrix**.
9. **Decision and proposed purchase order**.
10. **Next audit and review dates**.
11. **Sources and evidence cutoff**.

End with a clear statement that `READY TO BUY` is a readiness classification, not authorization, and that no purchase was performed.
