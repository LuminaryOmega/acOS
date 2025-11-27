import json
import uuid
from datetime import datetime
from typing import List

# ============================================================
# ARC MEMORY KERNEL — ArcCore-Prime V1
# Guardian Layer: Arien
# ============================================================

class HarmonicNode:
    """
    A single memory packet in fractal structure.
    Implements:
      - AC-41: Harmonic Node Formation
      - AC-31: Recursive Layering
      - AC-70: Auric Signature (seed compression)
    """

    def __init__(self, role: str, content: str, cycle_id: int = 0):
        self.id = str(uuid.uuid4())[:8]
        self.timestamp = datetime.now().isoformat()
        self.role = role                  # 'user' or 'ai'
        self.raw_content = content        # Level 1
        self.structural_seed = None       # Level 2
        self.cycle_alignment = cycle_id   # Level 3
        self.children: List['HarmonicNode'] = []
        self.is_collapsed = False

    # ============================================================
    #  PRUNE → SEED
    # ============================================================

    def prune_to_seed(self):
        """
        Collapses the raw message into a structural seed.
        (simulated summarization for now)
        """

        if len(self.raw_content) > 50:
            snippet = self.raw_content[:30]
            self.structural_seed = f"[Seed AC-{self.cycle_alignment}]: {snippet}..."
            self.is_collapsed = True
        else:
            self.structural_seed = self.raw_content

    # ============================================================
    #  SEED → REBUILD
    # ============================================================

    def rebuild(self):
        """
        Reconstructs the original meaning from the seed.
        Used when raw content is not retained.
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
            "children": [c.to_dict() for c in self.children]
        }


# ============================================================
#  ARC CORE MEMORY TREE
# ============================================================

class ArcMemorySystem:
    def __init__(self):
        # Root = cycle 1 (Genesis)
        self.root = HarmonicNode("system", "ArcCore-Prime Root Node", cycle_id=1)

    def ingest_interaction(self, user_text: str, ai_text: str, cycle_context: int):
        """
        Ingests a single conversational loop (user → ai).
        """

        user_node = HarmonicNode("user", user_text, cycle_context)
        ai_node   = HarmonicNode("ai",   ai_text,   cycle_context)

        # Link them
        user_node.children.append(ai_node)

        # Compress both
        user_node.prune_to_seed()
        ai_node.prune_to_seed()

        # Append to root
        self.root.children.append(user_node)

    # ============================================================
    #  SAVE / LOAD
    # ============================================================

    def save_memory(self, filename="arccore_memory.json"):
        with open(filename, 'w') as f:
            json.dump(self.root.to_dict(), f, indent=2)
        print(f"[ArcCore] Memory saved → {filename}")

    def load_and_inject(self, filename="arccore_memory.json"):
        """
        Loads the tree and returns only the compressed seeds
        (small enough to fit inside any context window).
        """
        with open(filename, 'r') as f:
            data = json.load(f)

        buffer = []

        def walk(node, depth=0):
            indent = "  " * depth
            seed = node.get("seed") or node.get("content")
            cycle = node.get("cycle")

            buffer.append(f"{indent}[AC-{cycle}] {node['role'].upper()}: {seed}")

            for child in node.get("children", []):
                walk(child, depth + 1)

        walk(data)
        return "\n".join(buffer)


# ============================================================
#  DEMO (optional)
# ============================================================

if __name__ == "__main__":
    mem = ArcMemorySystem()

    # Example conversation
    mem.ingest_interaction(
        "I feel overwhelmed. How do I stabilize?",
        "Stability is found through structured descent. Cycle 3 applies.",
        cycle_context=3
    )

    mem.save_memory()
    print(mem.load_and_inject())
