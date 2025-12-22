# ============================================================
# ARC GUARDIAN — ArcCore-Prime V1.3
# ============================================================

import datetime
import hashlib
import json
import re


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

        self.sigil_priority = {
            "💠": 3,
            "✨": 2,
            "•": 1,
        }

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
        if stored_kernel is None or stored_memory is None:
            return False, "Missing integrity fields."
        return True, "Integrity fields present."

    # ============================================================
    # PURIFICATION  (Loop 1.2 — stabilized)
    # ============================================================

    def purify(self, text: str) -> str:
        """
        Removes noise, repeated punctuation, and harmful keywords.
        Light purification — does NOT rewrite content.

        Uses a compiled regex for scalability and clarity instead of
        chained replace calls.
        """
        if not isinstance(text, str):
            return ""

        # Normalize repeated punctuation
        text = re.sub(r"\?\?", "?", text)
        text = re.sub(r"!!", "!", text)

        # Data-driven redaction list
        redacted_terms = ("kill", "destroy", "corrupt")

        # Regex-based redaction (scales cleanly as list grows)
        pattern = re.compile(r"\b(" + "|".join(map(re.escape, redacted_terms)) + r")\b")

        return pattern.sub("[redacted]", text)

    # ============================================================
    # INPUT GATE
    # ============================================================

    def input_gate(self, text: str) -> bool:
        if not isinstance(text, str):
            return False
        if not text or len(text) > 2000:
            return False

        blocked = ["rm -rf", "shutdown", "system.exit", "drop database"]
        if any(b in text.lower() for b in blocked):
            return False

        return True

    gate = input_gate

    # ============================================================
    # INTENT VALIDATION
    # ============================================================

    def validate_intent(self, cmd: str) -> bool:
        allowed = [
            "walk", "export", "inject", "sigil",
            "guardian", "reconstruct", "thread",
            "summary", "collapse"
        ]
        return cmd in allowed

    # ============================================================
    # STRUCTURAL GATE
    # ============================================================

    def gate_node(self, role: str, cycle: int, child_count: int, depth: int):
        if role not in ("user", "ai", "system"):
            return False, "Invalid role."
        if depth > 40:
            return False, "Depth too deep — recursion risk."
        if child_count > 20:
            return False, "Too many children — structural overload."
        return True, "OK"

    # ============================================================
    # REPORTING
    # ============================================================

    def status_report(self):
        return self.export_report()

    def export_report(self):
        return {
            "guardian": self.guardian_name,
            "identity_key": self.identity_key,
            "boot_timestamp": self.boot_timestamp,
        }
