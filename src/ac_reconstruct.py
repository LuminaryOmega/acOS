# ============================================================
# ARC RECONSTRUCTION ENGINE — ArcCore-Prime V1
# Loop 6 — Structural Reconstruction
# Cycle 31 (Recursive Threading)
# Cycle 33 (Contextual Re-Expansion)
# Guardian: Arien
# ============================================================

from typing import List, Dict, Any


class ArcReconstruct:
    """
    Deterministic reconstruction engine for ArcCore-Prime.

    Responsibilities:
      - Walk structural paths in the memory tree
      - Rebuild multi-node meaning from seeds
      - Create "threads" (cycle-sorted or path-sorted)
      - Generate readable reconstructed output
      - Prepare data for capsule export (Loop 7)
    """

    # ------------------------------------------------------------
    # SEED EXPANSION (deterministic)
    # ------------------------------------------------------------

    def expand_seed(self, seed: str) -> str:
        """
        Deterministic seed expansion:
        Converts a compressed seed into a richer contextual statement.
        Uses structural logic, not generative models.

        Example:
            "[AC-3] Stability found..." →
            "This message relates to Cycle 3, indicating stability arises
             through structured descent into detail."
        """
        if seed is None:
            return "(no seed)"

        if seed.startswith("[AC-"):
            cycle_tag = seed.split("]")[0][1:]  # "AC-3"
            body = seed.split("] ", 1)[-1]
            return f"({cycle_tag}) → {body}"

        if seed.startswith("[Seed AC-"):
            cycle_tag = seed.split("]")[0][1:]  # "Seed AC-3"
            body = seed.split("]: ", 1)[-1]
            return f"({cycle_tag}) → {body}"

        return f"(expanded) {seed}"

    # ------------------------------------------------------------
    # PATH-BASED RECONSTRUCTION
    # ------------------------------------------------------------

    def reconstruct_path(self, node: Dict[str, Any], depth: int = 0) -> List[str]:
        """
        Reconstructs a single linear path:
        Node → Children → Grandchildren

        Returns a list of expanded statements.
        """
        output = []

        indent = "  " * depth
        seed = node.get("seed") or node.get("content")
        expanded = self.expand_seed(seed)
        cycle = node.get("cycle")
        role = node.get("role", "").upper()

        output.append(f"{indent}[AC-{cycle}] {role}: {expanded}")

        for child in node.get("children", []):
            output.extend(self.reconstruct_path(child, depth + 1))

        return output

    # ------------------------------------------------------------
    # CYCLE-BASED THREAD RECONSTRUCTION
    # ------------------------------------------------------------

    def reconstruct_thread(self, tree: Dict[str, Any], cycle_id: int) -> List[str]:
        """
        Returns all nodes belonging to a given cycle, expanded.
        Useful for:
          - dataset grouping
          - cycle-specific summaries
          - structural introspection
        """

        results = []

        def walk(n: Dict[str, Any]):
            if int(n.get("cycle", -1)) == cycle_id:
                seed = n.get("seed") or n.get("content")
                results.append(self.expand_seed(seed))

            for child in n.get("children", []):
                walk(child)

        walk(tree)
        return results

    # ------------------------------------------------------------
    # FULL TREE RECONSTRUCTION (pretty print)
    # ------------------------------------------------------------

    def reconstruct_full(self, tree: Dict[str, Any]) -> str:
        """
        Reconstructs the entire tree into a human-readable structural summary.
        """
        lines = self.reconstruct_path(tree)
        return "\n".join(lines)
