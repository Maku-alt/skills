# Lightweight worker handoff

Use isolated workers to protect coordinator context, not to create ceremony. Prefer native subagent completion notifications and structured final responses. Do not require file sentinels, run manifests, phase logs, or SDD packages unless the repository already requires them.

## Dispatch rule

Delegate when a task is current, specialist, parallelizable, or token-heavy. Keep small synthesis and traveler decisions with the coordinator.

For a full audit with at least two independent volatile domains, delegate current-source research when subagents are available. This is a context-isolation rule: the coordinator should not absorb all border, transport, event, health, and market research itself.

Launch independent workers in parallel when their inputs do not depend on one another. Use fresh or minimally forked context. Do not pass the full parent conversation by default.

## Worker package

Provide only:

```yaml
task_id: stable-short-id
specialty: borders|aviation|ground-transport|lodging|health-insurance|finance|events|itinerary-safety|accessibility|agency-dmc
objective: one concrete outcome
context: only relevant travelers, route, dates, constraints, and known evidence
questions: bounded questions to answer
inputs: exact files or links allowed
source_policy: official/current requirements and consultation date
constraints:
  - no purchases, cancellations, or booking changes
  - no unrelated file edits
  - do not infer missing personal data
  - keep uncertainty visible
deliverable: travel-specialist-result-v1
```

Include a token-conscious instruction: inspect only named inputs first; search beyond them only when required to answer the bounded questions.

## Worker response contract

Require one compact final deliverable:

```yaml
schema: travel-specialist-result-v1
task_id: stable-short-id
status: completed|partial|blocked
as_of: ISO-8601 date or timestamp
scope: what was actually checked
findings:
  - claim: concise result
    evidence_state: RESEARCHED|VERIFIED|QUOTED|CONFLICTING
    source: official URL or exact local evidence path
    consulted_at: ISO-8601 date or timestamp
    applies_to: traveler, segment, booking, fare, or country
    confidence: high|medium|low
missing_inputs: []
risks:
  - severity: CRITICAL|HIGH|MEDIUM|LOW
    risk: concise statement
    mitigation: next action
recommended_actions:
  - action: concrete next step
    owner: traveler|coordinator|named-specialist
    deadline_or_trigger: date or condition
next_review: date or trigger
notes: only material caveats
```

Workers must not return logs, search diaries, hidden reasoning, full copied webpages, or unrelated recommendations.

## Coordinator acceptance

Accept a result only when:

- `task_id`, status, scope, and `as_of` are present;
- each volatile claim has applicable evidence and consultation date;
- unknown personal facts remain missing inputs;
- risks and actions stay within specialty;
- no purchase or unauthorized mutation occurred.

If the result is incomplete, send one focused follow-up or mark the handoff failed. Do not inspect worker chat or exploratory logs to reconstruct missing conclusions.

## Resume behavior

After dispatch, continue useful work that does not depend on the worker. Wait through the native agent mailbox or completion mechanism. On completion, integrate only the contracted final response and recalculate gaps, severity, dependencies, and trip state.

Use file artifacts only when a detailed report is too large for the response or the user requested persistent evidence. In that case the worker returns the artifact path and a compact summary; the coordinator opens only what is necessary for the decision.
