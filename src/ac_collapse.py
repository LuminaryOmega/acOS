# ============================================================
# ACCollapseEngine — ArcCore-Prime V1.5 (Unified)
# Guardian-Bound Structural Collapse Layer
# ============================================================
#
# History:
#   - Loop 1.1: Basic Recursive Collapse
#   - Loop 1.4: String Interning (Optimization)
#   - Loop 2.2: Compression Level Enums (State Safety)
#   - V1.5:     Unified Architecture
#
# Purpose:
#   Converts full memory nodes into compact structural seeds
#   while respecting Guardian boundary rules and ArcCore's
#   cycle, depth, and role constraints.
#
# ============================================================

import copy
import sys
from enum import IntEnum


# ============================================================
# LOOP 2.2 — COMPRESSION CONTRACT (NORMATIVE)
# ============================================================
# Compression levels define how much information is retained.
# Downgrades MUST be explicit.
# ============================================================

class CompressionLevel(IntEnum):
    RAW = 0          # Full content retained (short-lived)
    SUMMARY = 1      # Structured summary retained
    SEED = 2         # Auric seed + metadata only
    SIGIL_ONLY = 3   # Anchor only; reconstruction required


class ACCollapseEngine:
    """
    Safe collapse engine bound to Guardian policy rules.

    Performs:
      - AC-70: Auric Seed Compression
      - AC-31: Recursive Controlled Collapse
      - AC-67: Priority-Preserving Seed Retention
      - Loop 1.4: System-level String Interning
    """

    def __init__(self, guardian=None):
        # Optional binding; ArcMemorySystem will inject Guardian instance
        self.guardian = guardian

    # ------------------------------------------------------------
    #  INTERNAL: validate structure before collapse
    # ------------------------------------------------------------

    def _validate_node(self, node: dict, depth: int):
        """
        Returns (True, None) if safe.
        Returns (False, reason) if unsafe.
        """

        if self.guardian is None:
            return True, None

        # Loop 1.4 Optimization: Intern high-frequency strings
        role = sys.intern(node.get("role", "unknown"))
        cycle = node.get("cycle", 0)
        children = node.get("children", [])

        ok, reason = self.guardian.gate(
            role=role,
            cycle=cycle,
            child_count=len(children),
            depth=depth,
        )

        return ok, reason

    # ------------------------------------------------------------
    #  MAIN COLLAPSE
    # ------------------------------------------------------------

    def collapse_state(self, node: dict, depth: int = 0) -> dict:
        """
        Recursively collapses a node into a seed-safe structure.
        All Guardian policies are enforced at each step.
        """

        # 1. Structural clone (Preserve original memory safe)
        collapsed = copy.deepcopy(node)

        # Ensure compression metadata exists
        collapsed.setdefault("compression_level", CompressionLevel.RAW)
        collapsed.setdefault("compressed_from", None)

        # 2. Guardian validation (Optimized)
        ok, reason = self._validate_node(collapsed, depth)
        if not ok:
            # Intern error states for memory efficiency on failures
            return {
                "role": sys.intern(collapsed.get("role", "unknown")),
                "cycle": collapsed.get("cycle", 0),
                "error": sys.intern(f"[Guardian] Collapse blocked: {reason}"),
                "seed": sys.intern("[Blocked]"),
                "compression_level": CompressionLevel.SIGIL_ONLY,
                "compressed_from": collapsed.get("compression_level"),
                "children": []
            }

        # 3. Priority-sensitive collapse (The "Prismatic" Step)
        seed = collapsed.get("seed")
        raw = collapsed.get("content", "")
        priority = collapsed.get("priority", 0)

        # Strategy: If seed exists, safely discard raw content
        if seed:
            collapsed["content"] = None
            # Explicit State Transition
            if collapsed["compression_level"] == CompressionLevel.RAW:
                collapsed["compressed_from"] = CompressionLevel.RAW
                collapsed["compression_level"] = CompressionLevel.SEED

        else:
            # Strategy: Generate seed if missing
            if priority >= 3:
                # High priority: Keep longer snippet
                snippet = raw[:80]
            else:
                # Low priority: Aggressive truncate
                snippet = raw[:50]

            # Loop 1.4: Intern the prefix logic if possible, though variable content cannot be interned.
            collapsed["seed"] = f"[AutoSeed AC-{collapsed.get('cycle', 0)}]: {snippet}..."
            collapsed["content"] = None
            collapsed["compressed_from"] = collapsed.get("compression_level")
            collapsed["compression_level"] = CompressionLevel.SEED

        # 4. Recursively collapse children
        child_list = collapsed.get("children", [])
        new_children = []

        for child in child_list:
            new_child = self.collapse_state(child, depth + 1)
            new_children.append(new_child)

        collapsed["children"] = new_children

        return collapsed
