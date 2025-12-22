# ============================================================
# ACCollapseEngine — ArcCore-Prime V1.1
# Guardian-Bound Structural Collapse Layer
# ============================================================
#
# Purpose:
#   Converts full memory nodes into compact structural seeds
#   while respecting Guardian boundary rules and ArcCore's
#   cycle, depth, and role constraints.
#
# ============================================================

import copy
from enum import IntEnum


# ============================================================
# LOOP 2.2 — COMPRESSION CONTRACT (NORMATIVE)
# ============================================================
#
# Compression levels define how much information is retained
# over time. Levels are ordered by decreasing fidelity.
#
# Downgrades MUST be explicit.
# No node may be downgraded past SIGIL_ONLY silently.
#
# Reconstruction behavior MUST respect the compression level.
# Persistence guarantees are defined in docs/memory_model.md
#
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

    NOTE:
    This engine performs structural collapse only.
    Compression level transitions are explicit but
    downgrade policy is enforced elsewhere.
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

        role = node.get("role", "unknown")
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

        This method does NOT silently downgrade compression levels.
        Any downgrade must be explicitly recorded.
        """

        # 1. Structural clone
        collapsed = copy.deepcopy(node)

        # Ensure compression metadata exists
        collapsed.setdefault("compression_level", CompressionLevel.RAW)
        collapsed.setdefault("compressed_from", None)

        # 2. Guardian validation
        ok, reason = self._validate_node(collapsed, depth)
        if not ok:
            return {
                "role": collapsed.get("role", "unknown"),
                "cycle": collapsed.get("cycle", 0),
                "error": f"[Guardian] Collapse blocked: {reason}",
                "seed": "[Blocked]",
                "compression_level": CompressionLevel.SIGIL_ONLY,
                "compressed_from": collapsed.get("compression_level"),
                "children": []
            }

        # 3. Priority-sensitive collapse
        seed = collapsed.get("seed")
        raw = collapsed.get("content", "")
        priority = collapsed.get("priority", 0)

        # If seed already exists, discard raw content safely
        if seed:
            collapsed["content"] = None
            if collapsed["compression_level"] == CompressionLevel.RAW:
                collapsed["compressed_from"] = CompressionLevel.RAW
                collapsed["compression_level"] = CompressionLevel.SEED

        else:
            # Generate seed if missing
            if priority >= 3:
                snippet = raw[:80]
            else:
                snippet = raw[:50]

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
