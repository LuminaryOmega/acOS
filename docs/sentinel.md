Sentinel Model — Authority, Gating, and Judgment

ArcCore-Prime · Loop 3.1

Purpose

The Sentinel governs authority and permission within ArcCore.

Its role is not to execute actions, but to judge whether an action is allowed, under what authority, and for what reason.

This document defines:

the classes of power an action may exercise

the judgment contract every gated action must satisfy

the laws that bind authority, judgment, and execution

This model exists to prevent:

accidental destructive actions

silent privilege escalation

unexplainable system behavior

Core Principle

Memory that can mutate must be governed.

ArcCore is capable of persistence, compression, and reconstruction.
Therefore, every action that touches memory must declare its nature and submit to judgment.

OperationType (OT)
Definition

OperationType defines the class of power an action exercises over ArcCore.

It is not:

a role

a permission

a user identity

a cycle

It is the nature of the action itself.

Every action must map to exactly one OperationType.

If an action cannot be classified, it is invalid.

Canonical Operation Types

This set is closed and minimal.

READ
WRITE
MARK
GOVERN


No aliases.
No extensions without modifying this document.

OperationType Semantics
READ

Observational access that does not mutate state.

Includes:

reconstruction

summaries

thread inspection

sigil sweeps (read-only)

Guarantees:

no memory mutation

no compression changes

no sigil creation or removal

READ actions may fail, but they cannot cause harm.

WRITE

Creation or extension of memory.

Includes:

ingesting interactions

appending nodes

adding children

writing seeds

Guarantees:

existing memory is preserved

no deletion or restructuring occurs

WRITE adds data but does not reinterpret meaning.

MARK

Semantic mutation of existing memory.

Includes:

applying or removing sigils

changing compression levels

altering priority or density

MARK operations change how memory will be recalled.

They are meaning-altering but not structurally destructive.

GOVERN

Structural or irreversible authority.

Includes:

pruning

collapsing

archiving

overrides

forced reconstruction escalation

GOVERN actions are destructive, irreversible, or system-shaping.

This is the highest-risk operation class.

OperationType Law

Every action must explicitly declare its OperationType before execution.

No inference.
No implicit classification.

GateResult (GR)
Definition

GateResult is the Sentinel’s judgment.

It explains:

whether an action is allowed

why the decision was made

what authority comparison was used

GateResult does not:

execute code

mutate memory

escalate privileges

Canonical GateResult Structure

Every Sentinel judgment must return:

allowed: bool
reason: str
operation: OperationType
required_authority: int
actor_authority: int


No additional fields are required to explain a decision.

Field Semantics
allowed

True → action may proceed

False → action must not proceed

There is no partial or soft allowance.

reason

A human-readable explanation.

Examples:

authority 3 < required 7

READ permitted — non-mutating

MARK denied — sigil escalation requires higher authority

This string is part of the trust surface.

operation

The declared OperationType being judged.

Used for:

auditing

debugging

explanation

required_authority

The minimum authority level required for this operation.

This value is explicit and contextual.

actor_authority

The authority level of the actor attempting the action.

No inference or escalation occurs at this stage.

GateResult Law

A GateResult must be explainable in isolation.

If a decision cannot be understood without external context, it is invalid.

Laws of Interaction
Law 1 — Judgment precedes action

Sentinel judgment must occur before execution.

No post-hoc denial.

Law 2 — Sentinel does not mutate

The Sentinel never performs the action it judges.

Judgment and execution are strictly separated.

Law 3 — No silent paths

Any mutating action that bypasses Sentinel judgment is a defect.

Law 4 — Authority is explicit

Authority comparisons are numeric and monotonic.

No role magic.
No implied privilege.

Non-Goals (Explicit)

This model does not:

define authority values

bind authority to cycles

log audits

enforce policies

replace existing Guardian logic

Those concerns are addressed in later loops.

Closing Statement

The Sentinel exists to ensure ArcCore can explain itself, protect itself, and remain trustworthy as complexity increases.

Authority without explanation is power.
Authority with explanation is governance.
