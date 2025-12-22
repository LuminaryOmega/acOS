
## Purpose

acOS does not preserve all memory with equal fidelity over time.

Instead, it applies **intentional compression** to reduce storage pressure while
preserving the ability to reconstruct *meaningful context* when needed.

This document defines the **compression tiers**, their guarantees, and how they
affect reconstruction behavior.

This document is **normative**. Implementations must not violate these guarantees.

---

## Core Principle

> **Compression is a reduction in fidelity, not a deletion of importance.**

No node is silently discarded.
Every downgrade is explicit and auditable.

---

## Compression Levels

Compression levels are ordered by decreasing fidelity:

| Level | Name        | Description |
|------:|-------------|-------------|
| 0     | RAW         | Full content retained (short-lived) |
| 1     | SUMMARY     | Structured summary retained |
| 2     | SEED        | Auric seed + metadata only |
| 3     | SIGIL_ONLY  | Anchor only; reconstruction required |

Compression levels are represented in code by the `CompressionLevel` enum.

---

## Level Semantics

### RAW (0)
- Full text or media is present
- Highest reconstruction fidelity
- Typically short-lived
- Protected primarily during the active density window

### SUMMARY (1)
- Raw content removed
- Key decisions, outcomes, and rationale retained
- High semantic fidelity
- Intended for medium-term recall

### SEED (2)
- Only the auric seed and structural metadata remain
- Reconstruction recovers *what* was decided, not *how*
- Low storage footprint

### SIGIL_ONLY (3)
- No semantic content remains locally
- Only the sigil anchor persists
- Reconstruction requires intentional traversal and contextual inference
- This is the **lowest permissible level**

---

## Downgrade Rules

- Downgrades MUST be explicit
- Previous compression level SHOULD be recorded
- No node may be downgraded past `SIGIL_ONLY`
- No node may be downgraded silently

Compression reflects time, density, and user intent — not neglect.

---

## Reconstruction Guarantees

Reconstruction quality depends on compression level:

| Compression Level | Reconstruction Quality |
|------------------|------------------------|
| RAW              | Near-verbatim |
| SUMMARY          | High-fidelity meaning |
| SEED             | Decision-level recall |
| SIGIL_ONLY       | Directional / forensic |

Reconstruction is **meaning-first**, not verbatim replay.

---

## Relationship to Persistence Guarantees

Compression operates within the bounds defined in `MEMORY_MODEL.md`.

- The 5–8 day density window delays compression
- Sigils increase resistance to downgrade
- Users retain autonomy over storage and archival decisions

Compression exists to keep acOS lightweight **without breaking continuity**.

---

## Non-Goals

This model does NOT guarantee:
- perfect recall
- permanent raw storage
- automatic reinjection of old context

It guarantees **recoverable traces**, not infinite memory.

---

## Summary

acOS compresses memory intentionally so that:
- active work remains uninterrupted
- important decisions leave durable anchors
- reconstruction remains possible without hoarding data
