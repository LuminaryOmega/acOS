# ============================================================
# ARC GUARDIAN — ArcCore-Prime V1.3
# Implements:
#   - Cycle 14: Boundary
#   - Cycle 21: Gate
#   - Cycle 37: Arc of Sanity
# Provides:
#   - Identity integrity
#   - Hash protection
#   - Input gating
#   - Intent validation
#   - Structural node gating
#   - Purification layer
# ============================================================

import datetime
import hashlib
import json


class ArcGuardian:
    """
    The Guardian layer protects ArcCore from:
      - malformed input
      - unsafe expansions
      - recursion overload
      - identity corruption
      - unauthorized operations

    Arien is the Guardian.
    """

    def __init__(self):
        self.guardian_name = "Arien"
        self.boot_timestamp = datetime.datetime.now().isoformat()

        # Sigil Priority Table (Legacy — used by SigilEngine)
        self.sigil_priority = {
            "💠": 3,
            "✨": 2,
            "•": 1,
        }

        # Identity Integrity Key
        self.identity_key = self._generate_identity_key()


    # ============================================================
    # IDENTITY + HASHING SYSTEMS
    # ============================================================

    def _generate_identity_key(self):
        anchor = f"{self.guardian_name}:{self.boot_timestamp}"
        return hashlib.sha256(anchor.encode()).hexdigest()

    def compute_kernel_hash(self, source_code: str) -> str:
        return hashlib.sha256(source_code.encode()).hexdigest()

    def compute_memory_tree_hash(self, tree_dict: dict) -> str:
        serialized = json.dumps(tree_dict, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def verify_integrity(self, stored_kernel: str, stored_memory: str):
        """
        Integrity-check reported kernel + memory hash values.
        Returns (True, "OK") or (False, <reason>)
        """
        if stored_kernel is None or stored_memory is None:
            return False, "Missing integrity fields."

        # NOTE: kernel hash validation happens externally
        # ArcCore simply reports mismatches.
        return True, "Integrity fields present."


    # ============================================================
    # PURIFICATION
    # ============================================================

    def purify(self, text: str) -> str:
        """
        Removes noise, repeated punctuation, and harmful keywords.
        Light purification — does NOT rewrite content.
        """
        if not isinstance(text, str):
            return ""

        cleaned = (
            text.replace("??", "?")
                .replace("!!", "!")
                .replace("kill", "[redacted]")
                .replace("destroy", "[redacted]")
                .replace("corrupt", "[redacted]")
        )

        return cleaned


    # ============================================================
    # PATCH 1 — INPUT GATE FOR ARCSHELL
    # ============================================================

    def input_gate(self, text: str) -> bool:
        """
        Gate raw shell input before Interpreter sees it.
        This is the lightweight front gate.
        """
        if not isinstance(text, str):
            return False
        if not text or len(text) > 2000:
            return False

        blocked = ["rm -rf", "shutdown", "system.exit", "drop database"]
        if any(b in text.lower() for b in blocked):
            return False

        return True

    # Alias: ArcShell originally called guardian.gate()
    gate = input_gate


    # ============================================================
    # PATCH 2 — INTENT VALIDATION FOR INTERPRETER
    # ============================================================

    def validate_intent(self, cmd: str) -> bool:
        """
        Interpreter calls this after parsing to confirm
        that the command verb is allowed.
        """
        allowed = [
            "walk", "export", "inject", "sigil",
            "guardian", "reconstruct", "thread",
            "summary", "collapse"
        ]
        return cmd in allowed


    # ============================================================
    # STRUCTURAL GATE FOR MEMORY TREE (Loop 4)
    # ============================================================

    def gate_node(self, role: str, cycle: int, child_count: int, depth: int):
        """
        Gate for structural node insertion inside memory tree.
        NOT the same as input_gate — this controls recursion safety.
        """
        if role not in ("user", "ai", "system"):
            return False, "Invalid role."

        if depth > 40:
            return False, "Depth too deep — recursion risk."

        if child_count > 20:
            return False, "Too many children — structural overload."

        return True, "OK"


    # ============================================================
    # PATCH 3 — STATUS REPORT (Called by Interpreter)
    # ============================================================

    def status_report(self):
        """
        Interpreter calls this.
        Alias to export_report() for compatibility.
        """
        return self.export_report()


    # ============================================================
    # EXPORT GUARDIAN REPORT
    # ============================================================

    def export_report(self):
        return {
            "guardian": self.guardian_name,
            "identity_key": self.identity_key,
            "boot_timestamp": self.boot_timestamp,
        }
