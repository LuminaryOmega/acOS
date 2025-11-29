# ============================================================
# ARC MEMORY KERNEL — ArcCore-Prime V1.1
# Loop 4.E: Integrity Hashing + Guardian-Gated Safety
# Guardian Layer: Arien
# ============================================================

from ac_sigils import SigilEngine
from ac_collapse import ACCollapseEngine
from arc_guardian import ArcGuardian

import json
import uuid
import inspect
from datetime import datetime
from typing import List


# ============================================================
#  HARMONIC NODE  (AC-41 / AC-31 / AC-70 / AC-67)
# ============================================================

class HarmonicNode:
    """
    A single memory packet in the fractal ArcCore tree.
    """

    def __init__(self, role: str, content: str, cycle_id: int = 0):
        self.id = str(uuid.uuid4())[:8]
        self.timestamp = datetime.now().isoformat()

        self.role = role
        self.raw_content = content
        self.structural_seed = None
        self.cycle_alignment = cycle_id
        self.children: List['HarmonicNode'] = []

        self.is_collapsed = False
        self.priority = 0  # AC-67 Prismatic Echo score

    # ------------------------------------------------------------
    #  SIGIL PRIORITY (AC-67)
    # ------------------------------------------------------------

    def apply_sigil_priority(self, sigil_engine: SigilEngine):
        self.priority = sigil_engine.evaluate(self.raw_content)
        return self.priority

    # ------------------------------------------------------------
    #  PRUNE → SEED (AC-70)
    # ------------------------------------------------------------

    def prune_to_seed(self):
        if self.priority >= 3:
            snippet = self.raw_content[:80]
            self.structural_seed = f"[AC-{self.cycle_alignment}] {snippet}..."
            self.is_collapsed = True
            return

        if len(self.raw_content) > 50:
            snippet = self.raw_content[:30]
            self.structural_seed = f"[Seed AC-{self.cycle_alignment}]: {snippet}..."
            self.is_collapsed = True
        else:
            self.structural_seed = self.raw_content

    # ------------------------------------------------------------
    #  REBUILD
    # ------------------------------------------------------------

    def rebuild(self):
        if self.is_collapsed:
            return f"(Reconstructed) {self.structural_seed}"
        return self.raw_content

    # ------------------------------------------------------------
    #  EXPORT
    # ------------------------------------------------------------

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
#  ARC MEMORY TREE (AC-28)
# ============================================================

class ArcMemorySystem:
    def __init__(self):
        self.root = HarmonicNode("system", "ArcCore-Prime Root Node", cycle_id=1)

        self.collapse = ACCollapseEngine()
        self.sigil = SigilEngine()
        self.guardian = ArcGuardian()

        # Compute kernel integrity hash at boot
        import arc_prime
        kernel_source = inspect.getsource(arc_prime)
        self.kernel_hash = self.guardian.compute_kernel_hash(kernel_source)

        # Will be updated whenever memory changes
        self.memory_hash = None

    # ------------------------------------------------------------
    #  INGEST LOOP
    # ------------------------------------------------------------

    def ingest_interaction(self, user_text: str, ai_text: str, cycle_context: int):
        # Purify inputs
        clean_user = self.guardian.purify(user_text)
        clean_ai = self.guardian.purify(ai_text)

        user_node = HarmonicNode("user", clean_user, cycle_context)
        ai_node   = HarmonicNode("ai",   clean_ai,   cycle_context)

        # Priority (AC-67)
        user_node.apply_sigil_priority(self.sigil)
        ai_node.apply_sigil_priority(self.sigil)

        # Structural gate
        ok_u, msg_u = self.guardian.gate(user_node.role, user_node.cycle_alignment, 1, depth=1)
        ok_a, msg_a = self.guardian.gate(ai_node.role,   ai_node.cycle_alignment,   0, depth=2)

        if not ok_u:
            raise RuntimeError(f"[Guardian] User-node rejected: {msg_u}")
        if not ok_a:
            raise RuntimeError(f"[Guardian] AI-node rejected: {msg_a}")

        # Link
        user_node.children.append(ai_node)

        # Collapse
        user_node.prune_to_seed()
        ai_node.prune_to_seed()

        # Append to tree
        self.root.children.append(user_node)

        # Update memory tree integrity hash
        self.memory_hash = self.guardian.compute_memory_tree_hash(self.root.to_dict())

    # ============================================================
    #  SAVE MEMORY (with integrity stamps)
    # ============================================================

    def save_memory(self, filename="arccore_memory.json"):
        tree = self.root.to_dict()

        integrity_block = {
            "kernel_hash": self.kernel_hash,
            "memory_hash": self.memory_hash,
            "guardian": self.guardian.guardian_name,
            "identity_key": self.guardian.identity_key,
            "timestamp": datetime.now().isoformat()
        }

        payload = {
            "integrity": integrity_block,
            "tree": tree
        }

        with open(filename, 'w') as f:
            json.dump(payload, f, indent=2)

        print(f"[ArcCore] Memory + Integrity saved → {filename}")

    # ============================================================
    #  LOAD + INJECT (with verification)
    # ============================================================

    def load_and_inject(self, filename="arccore_memory.json"):
        with open(filename, 'r') as f:
            payload = json.load(f)

        integrity = payload.get("integrity", {})
        tree = payload.get("tree", {})

        stored_kernel = integrity.get("kernel_hash")
        stored_mem = integrity.get("memory_hash")

        ok, msg = self.guardian.verify_integrity(stored_kernel, stored_mem)

        status = "OK" if ok else f"WARNING — {msg}"

        buffer = [f"[Integrity: {status}]"]

        # Walk compressed seeds
        def walk(node, depth=0):
            indent = "  " * depth
            seed = node.get("seed") or node.get("content")
            cycle = node.get("cycle")
            role = node.get("role", "").upper()
            priority = node.get("priority", 0)
            marker = "💠" if priority >= 3 else "•"

            buffer.append(f"{indent}{marker} [AC-{cycle}] {role}: {seed}")

            for child in node.get("children", []):
                walk(child, depth + 1)

        walk(tree)
        return "\n".join(buffer)


# ============================================================
#  DEMO
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
