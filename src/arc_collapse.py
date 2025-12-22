# ============================================================
# ACCollapseEngine — ArcCore-Prime V1.1
# Guardian-Bound Structural Collapse Layer
# Loop 1.4: Interning + Governance Clarification
# ============================================================
#
# Purpose:
#   Converts full memory nodes into compact structural seeds
#   while respecting Guardian boundary rules and ArcCore's
#   cycle, depth, and role constraints.
#
# ============================================================

import copy
import sys


class ACCollapseEngine:
    """
    Safe collapse engine bound to Guardian policy rules.
    Performs:
      - AC-70: Auric Seed Compression
      - AC-31: Recursive Controlled Collapse
      - AC-67: Priority-Preserving Seed Retention
    """

    def __init__(self, guardian=None):
        # Optional binding; ArcMemorySystem injects Guardian authority.
        # CollapseEngine itself never decides policy.
        self.guardian = guardian

    # ------------------------------------------------------------
    #  INTERNAL: validate structure before collapse
    # ------------------------------------------------------------

    def _validate_node(self, node: dict, depth: int):
        """
        Returns (True, None) if safe.
        Returns (False, reason) if unsafe.

        Governance note:
        - ACCollapseEngine does not interpret policy.
        - Guardian remains the sole authority.
        """

        if self.guardian is None:
            return True, None

        # Loop 1.4 — intern high-frequency structural strings
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

        # 1. Structural clone
        collapsed = copy.deepcopy(node)

        # 2. Guardian validation
        ok, reason = self._validate_node(collapsed, depth)
        if not ok:
            return {
                "role": sys.intern(collapsed.get("role", "unknown")),
                "cycle": collapsed.get("cycle", 0),
                "error": sys.intern(f"[Guardian] Collapse blocked: {reason}"),
                "seed": sys.intern("[Blocked]"),
                "children": []
            }

        # 3. Priority-sensitive collapse
        seed = collapsed.get("seed")
        raw = collapsed.get("content", "")
        priority = collapsed.get("priority", 0)

        # If seed already exists, discard raw content safely
        if seed:
            collapsed["content"] = None

        else:
            # Generate seed if missing
            if priority >= 3:
                snippet = raw[:80]
            else:
                snippet = raw[:50]

            collapsed["seed"] = f"[AutoSeed AC-{collapsed.get('cycle', 0)}]: {snippet}..."
            collapsed["content"] = None

        # 4. Recursively collapse children
        child_list = collapsed.get("children", [])
        new_children = []

        for child in child_list:
            new_child = self.collapse_state(child, depth + 1)
            new_children.append(new_child)

        collapsed["children"] = new_children

        return collapsed
