— Audit & Traceability

ArcCore-Prime Governance Model

Purpose

Audit & Traceability defines how ArcCore explains itself over time.

It ensures that:

no significant action is silent

authority decisions are reviewable

failures are diagnosable

trust does not depend on memory or belief

This model exists to answer one core question:

“Why did the system do (or refuse to do) this?”

Core Principle

Authority without traceability becomes power without accountability.

ArcCore must not only make correct decisions —
it must be able to reconstruct the reasoning behind them.

What Is Audited (Scope)

Only governed actions are auditable.

Specifically:

all MARK operations

all GOVERN operations

any denied action (of any type)

optional: high-authority WRITE actions

READ actions are not audited by default, to preserve privacy and reduce noise.

Audit Record (Conceptual)

An Audit Record is a snapshot of a Sentinel judgment at a point in time.

Each record represents one decision, not one execution.

Canonical Audit Record Fields
timestamp
operation
allowed
reason
actor_authority
required_authority
target_node_id (optional)
cycle_context (optional)


Nothing here is secret.
Nothing here is inferred.

Field Semantics
timestamp

When the judgment occurred

Monotonic and comparable

operation

The OperationType being judged

Directly mirrors Sentinel input

allowed

True or False

Matches GateResult exactly

reason

Human-readable explanation

Must match GateResult reason verbatim

actor_authority / required_authority

Numeric values used in comparison

Required for post-hoc reasoning

target_node_id (optional)

Present if the action targets a specific node

Absent for global or system actions

cycle_context (optional)

Active cycle at time of judgment

Useful for reconstructing intent

Audit Levels (Noise Control)

Audit verbosity must be configurable.

Suggested levels:

OFF        → no audit records
GOVERN     → only GOVERN operations
MARK+      → MARK and GOVERN
ALL_DENY   → any denied action
FULL       → all governed actions


This allows:

minimal overhead by default

deep introspection when needed

Audit Storage (Non-Prescriptive)

Audit records may be:

kept in memory

written to file

streamed externally

rotated or pruned

This model does not mandate storage strategy.

ArcCore respects:

user autonomy

privacy requirements

deployment constraints

Traceability Guarantees
Guarantee 1 — No Silent Failure

Any denied governed action must be auditable.

Guarantee 2 — Decision Replay

Given an audit record, a human must be able to reconstruct the decision logic without code execution.

Guarantee 3 — Audit Is Non-Mutating

Audit mechanisms must never affect system behavior.

Audit observes.
It does not interfere.

Relationship to Sentinel & Authority

Sentinel produces GateResult

Authority Model defines required authority

Audit records capture the outcome

Audit does not:

judge

enforce

escalate

It records.

Privacy & Respect

Audit records:

contain no raw content

contain no user secrets

reference nodes symbolically

prioritize explanation over surveillance

ArcCore audits decisions, not people.

Non-Goals (Explicit)

Audit & Traceability does not:

log READ actions by default

store raw memory

centralize telemetry

enforce compliance externally

Those choices remain user-controlled.

Closing Statement

Audit & Traceability ensures ArcCore can answer for itself.

When memory is questioned,
when authority is challenged,
when trust is tested —
