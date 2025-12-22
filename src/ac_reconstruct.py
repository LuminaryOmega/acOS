# ============================================================
# ACReconstruct — ArcCore Memory Reconstruction Engine
# ============================================================
#
# Purpose:
#   Reconstructs human-readable meaning from collapsed
#   ArcCore memory trees. Reconstruction is deterministic,
#   meaning-first, and compression-aware.
#
# ============================================================

from typing import Dict, Any, List
from ac_collapse import CompressionLevel


class ArcReconstruct:
    """
    Deterministic reconstruction engine.

    Reconstructs memory from:
      - raw content
      - summaries
      - auric seeds
      - sigil anchors

    Reconstruction behavior is governed by compression level.
    """

    def __init__(self):
        pass

    # ------------------------------------------------------------
    # Seed Expansion
    # ------------------------------------------------------------

    def expand_seed(self, seed: str) -> str:
        """
        Expands an auric seed into a readable semantic statement.
        This is deterministic and does not hallucinate.
        """
        if not seed:
            return "[No seed available]"
        return seed.replace("[AutoSeed", "[Seed")

    # ------------------------------------------------------------
    # Path-Based Reconstruction (existing logic)
    # ------------------------------------------------------------

    def reconstruct_path(self, node: Dict[str, Any], depth: int = 0) -> List[str]:
        """
        Reconstructs a node and its children structurally.
        Used for RAW and SUMMARY tiers.
        """
        lines = []
        indent = "  " * depth

        role = node.get("role", "").upper()
        cycle = node.get("cycle", 0)
        seed = node.get("seed") or node.get("content", "[No content]")

        lines.append(f"{indent}[AC-{cycle}] {role}: {seed}")

        for child in node.get("children", []):
            lines.extend(self.reconstruct_node(child, depth + 1))

        return lines

    # ------------------------------------------------------------
    # COMPRESSION-AWARE DISPATCH (Loop 2.2)
    # ------------------------------------------------------------

    def reconstruct_node(self, node: Dict[str, Any], depth: int = 0) -> List[str]:
        """
        Dispatches reconstruction based on compression level.

        Reconstruction is meaning-first and tier-respecting.
        """

        level = node.get("compression_level", CompressionLevel.RAW)

        # RAW and SUMMARY behave structurally
        if level in (CompressionLevel.RAW, CompressionLevel.SUMMARY):
            return self.reconstruct_path(node, depth)

        # SEED: expand auric seed only
        if level == CompressionLevel.SEED:
            indent = "  " * depth
            expanded = self.expand_seed(node.get("seed"))
            role = node.get("role", "").upper()
            cycle = node.get("cycle", 0)
            return [f"{indent}[AC-{cycle}] {role}: {expanded}"]

        # SIGIL_ONLY: honest boundary
        if level == CompressionLevel.SIGIL_ONLY:
            indent = "  " * depth
            role = node.get("role", "").upper()
            cycle = node.get("cycle", 0)
            return [
                f"{indent}[AC-{cycle}] {role}: [Sigil Anchor — reconstruction required]"
            ]

        # Defensive fallback
        return ["[Unrecognized compression level]"]

    # ------------------------------------------------------------
    # Full Tree Reconstruction
    # ------------------------------------------------------------

    def reconstruct_full(self, tree: Dict[str, Any]) -> str:
        """
        Reconstructs the entire memory tree into a readable summary,
        respecting compression levels.
        """
        lines = self.reconstruct_node(tree)
        return "\n".join(lines)
