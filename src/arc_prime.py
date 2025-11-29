# ============================================================
# ARC MEMORY KERNEL — ArcCore-Prime V1
# Guardian Layer: Arien
# ============================================================

from ac_sigils import SigilEngine
from ac_collapse import ACCollapseEngine
from arc_guardian import ArcGuardian

import json
import uuid
from datetime import datetime
from typing import List


# ============================================================
#  HARMONIC NODE (AC-41 / AC-31 / AC-70 / AC-67)
# ============================================================

class HarmonicNode:
    """
    A single memory packet in the fractal ArcCore tree.

    Implements:
      - AC-41: Harmonic Node Formation
      - AC-31: Recursive Layering
      - AC-70: Auric Signature (seed compression)
      - AC-67: Prismatic Echo (sigil weighting)
    """

    def __init__(self, role: str, content: str, cycle_id: int = 0):
        self.id = str(uuid.uuid4())[:8]
        self.timestamp = datetime.now().isoformat()

        self.role = role                   # 'user' | 'ai'
        self.raw_content = content         # Level 1 (raw text)
        self.structural_seed = None        # Level 2 (compressed)
        self.cycle_alignment = cycle_id    # Level 3 (cycle tag)
        self.children: List['HarmonicNode'] = []

        self.is_collapsed = False
        self.priority = 0                  # AC-67 — Prismatic importance score

    # ============================================================
    #  SIGIL PRIORITY (AC-67)
    # ============================================================

    def apply_sigil_priority(self, sigil_engine: SigilEngine):
        """
        Computes the symbolic weight of this node.
        Higher priority = less pruning.
        """
        self.priority = sigil_engine.evaluate(self.raw_content)
        return self.priority

    # ============================================================
    #  PRUNE → SEED (AC-70)
    # ============================================================

    def prune_to_seed(self):
        """
        Collapses raw text into a symbolic structural seed.
        Priority-based pruning:
          - High priority: keep more content
          - Low priority: stronger compression
        """

        # High-priority content keeps more detail
        if self.priority >= 3:
            snippet = self.raw_content[:80]
            self.structural_seed = f"[AC-{self.cycle_alignment}] {snippet}..."
            self.is_collapsed = True
            return

        # Normal collapse
        if len(self.raw_content) > 50:
            snippet = self.raw_content[:30]
            self.structural_seed = f"[Seed AC-{self.cycle_alignment}]: {snippet}..."
            self.is_collapsed = True
        else:
            # Short messages remain uncompressed
            self.structural_seed = self.raw_content

    # ============================================================
    #  REBUILD FROM SEED
    # ============================================================

    def rebuild(self):
        """
        Reconstructs approximate meaning from the seed.
        """
        if self.is_collapsed:
            return f"(Reconstructed) {self.structural_seed}"
        return self.raw_content

    # ============================================================
    #  EXPORT TO JSON
    # ============================================================

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "cycle": self.cycle_alignment,
            "content": self.raw_content,
            "seed": self.structural_seed,
            "collapsed": self.is_collapsed,
            "priority": self.priority,
            "children": [c.to_dict() for c in self.children]
        }


# ============================================================
#  ARC CORE MEMORY TREE
# ============================================================

class ArcMemorySystem:
    def __init__(self):
        # Root = Cycle 1 (Genesis)
        self.root = HarmonicNode("system", "ArcCore-Prime Root Node", cycle_id=1)

        # Collapse + Sigils + Guardian initialization (future loops)
        self.collapse = ACCollapseEngine()
        self.sigil = SigilEngine()
        self.guardian = ArcGuardian()     # Not used yet — for Loop 4+

    # ------------------------------------------------------------
    #  INGEST USER → AI INTERACTION (AC-28)
    # ------------------------------------------------------------

    def ingest_interaction(self, user_text: str, ai_text: str, cycle_context: int):
        """
        Ingests a single conversational loop (user → ai).
        """

        user_node = HarmonicNode("user", user_text, cycle_context)
        ai_node   = HarmonicNode("ai",   ai_text,  cycle_context)

        # Apply prismatic priority
        user_node.apply_sigil_priority(self.sigil)
        ai_node.apply_sigil_priority(self.sigil)

        # Link them
        user_node.children.append(ai_node)

        # Priority-aware compression
        user_node.prune_to_seed()
        ai_node.prune_to_seed()

        # Append to root
        self.root.children.append(user_node)

    # ============================================================
    #  SAVE / LOAD (compressed)
    # ============================================================

    def save_memory(self, filename="arccore_memory.json"):
        with open(filename, 'w') as f:
            json.dump(self.root.to_dict(), f, indent=2)
        print(f"[ArcCore] Memory saved → {filename}")

    def load_and_inject(self, filename="arccore_memory.json"):
        """
        Loads the memory tree and returns only compressed seeds.
        Perfect for injecting into small context windows.
        """
        with open(filename, 'r') as f:
            data = json.load(f)

        buffer = []

        def walk(node, depth=0):
            indent = "  " * depth
            seed = node.get("seed") or node.get("content")
            cycle = node.get("cycle")
            role = node.get("role").upper()
            priority = node.get("priority", 0)

            # Annotated prismatic echo output
            marker = "💠" if priority >= 3 else "•"

            buffer.append(f"{indent}{marker} [AC-{cycle}] {role}: {seed}")

            for child in node.get("children", []):
                walk(child, depth + 1)

        walk(data)
        return "\n".join(buffer)


# ============================================================
#  DEMO (optional)
# ============================================================

if __name__ == "__main__":
    mem = ArcMemorySystem()

    mem.ingest_interaction(
        "I feel overwhelmed. How do I stabilize?",
        "Stability is found through structured descent. Cycle 3 applies.",
        cycle_context=3
    )

    mem.save_memory()
    print(mem.load_and_inject())
