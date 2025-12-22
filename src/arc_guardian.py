# ============================================================
# ARC GUARDIAN — ArcCore-Prime V1.4
# Implements:
#   - Cycle 14: Boundary
#   - Cycle 21: Gate
#   - Cycle 37: Arc of Sanity
#
# Loop 1.4:
#   - String interning
#   - Governance clarity (RBAC-lite)
#   - Redaction hardening (compiled regex)
# ============================================================

import datetime
import hashlib
import json
import re
import sys


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
        self.guardian_name = sys.intern("Arien")
        self.boot_timestamp = datetime.datetime.now().isoformat()

        # Sigil Priority Table (Legacy — used by SigilEngine)
        self.sigil_priority = {
            "💠": 3,
            "✨": 2,
            "•": 1,
        }

        # Identity Integrity Key
        self.identity_key = self._generate_identity_key()

        # Loop 1.4 — compiled redaction regex (deterministic, auditable)
        self._redacted_terms = ("kill", "destroy", "corrupt")
        self._redaction_pattern = re.compile(
            r"\b(" + "|".join(map(re.escape, self._redacted_terms)) + r")\b"
        )

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

        # NOTE:
        # Kernel hash validation is computed externally.
        # Guardian reports integrity state; it does not override it.
        return True, "Integrity fields present."

    # ============================================================
    # PURIFICATION  (Loop 1.4 hardened)
    # ============================================================

    def purify(self, text: str) -> str:
        """
        Removes noise, repeated punctuation, and harmful keywords.
        Light purification — does NOT rewrite content.

        Loop 1.4:
        - Uses compiled regex instead of chained replace
        - Deterministic and scalable
        """
        if not isinstance(text, str):
            return ""

        # Normalize repeated punctuation
        text = re.sub(r"\?\?", "?", text)
        text = re.sub(r"!!", "!", text)

        # Redact harmful keywords (exact-match, word-boundary)
        return self._redaction_pattern.sub("[redacted]", text)

    # ============================================================
    # PATCH 1 — INPUT GATE (Front Gate)
    # ============================================================

    def input_gate(self, text: str) -> bool:
        """
        Gate raw shell or user input before interpreter access.
        Lightweight, fast, non-semantic.
        """
        if not isinstance(text, str):
            return False
        if not text or len(text) > 2000:
            return False

        blocked = ("rm -rf", "shutdown", "system.exit", "drop database")
        if any(b in text.lower() for b in blocked):
            return False

        return True

    # Backward-compatible alias
    gate = input_gate

    # ============================================================
    # PATCH 2 — INTENT VALIDATION (Interpreter Gate)
    # ============================================================

    def validate_intent(self, cmd: str) -> bool:
        """
        Validates parsed command verbs.
        Governance note:
        - This is a whitelist, not inference.
        """
        allowed = {
            "walk", "export", "inject", "sigil",
            "guardian", "reconstruct", "thread",
            "summary", "collapse"
        }
        return cmd in allowed

    # ============================================================
    # STRUCTURAL GATE (Memory Tree Governance)
    # ============================================================

    def gate_node(self, role: str, cycle: int, child_count: int, depth: int):
        """
        Structural gate for memory tree mutation.
        Loop 1.4 governance clarification:
        - Guardian is sole authority
        - No policy inference happens outside this layer
        """
        role = sys.intern(role)

        if role not in ("user", "ai", "system"):
            return False, "Invalid role."

        if depth > 40:
            return False, "Depth too deep — recursion risk."

        if child_count > 20:
            return False, "Too many children — structural overload."

        return True, "OK"

    # ============================================================
    # STATUS / REPORTING
    # ============================================================

    def status_report(self):
        return self.export_report()

    def export_report(self):
        return {
            "guardian": self.guardian_name,
            "identity_key": self.identity_key,
            "boot_timestamp": self.boot_timestamp,
        }
