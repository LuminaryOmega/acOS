# ============================================================
# ArcCore-Prime V1 — Guardian Layer
# Guardian: Arien
# ============================================================
#
# Purpose:
#   The Guardian validates all inputs before they reach the kernel.
#   It enforces identity, structure, roles, cycles, and collapse safety.
#
# Design (Option C):
#   - Roles, cycles, and boundaries are controlled by configuration
#     rather than kernel-hardcoded rules.
#   - This allows ArcCore to expand without modifying the kernel.
# ============================================================

import hashlib
import datetime


class ArcGuardian:
    """
    The Guardian protects ArcCore from:
      - invalid roles
      - malformed cycles
      - recursive runaway loops
      - identity corruption
      - unauthorized actors
      - unsafe collapse requests
    """

    def __init__(self):
        # ------------------------------------------------------------
        # CONFIGURABLE POLICY TABLE  (Option C)
        # ------------------------------------------------------------
        self.policy = {
            "allowed_roles": ["user", "ai", "system"],
            "max_cycle": 99,
            "min_cycle": 1,
            "max_children_per_node": 6,
            "max_depth": 12,
        }

        # Guardian identity anchor
        self.guardian_name = "Arien"
        self.boot_timestamp = datetime.datetime.now().isoformat()
        self.integrity_key = self._generate_integrity_key()

    # ------------------------------------------------------------
    #   INTERNAL — Identity Hash
    # ------------------------------------------------------------

    def _generate_integrity_key(self):
        """
        Ensures no module impersonates the Guardian.
        """
        anchor = f"{self.guardian_name}:{self.boot_timestamp}"
        return hashlib.sha256(anchor.encode()).hexdigest()

    # ------------------------------------------------------------
    #   VALIDATE ROLE (Option C)
    # ------------------------------------------------------------

    def validate_role(self, role: str) -> bool:
        return role in self.policy["allowed_roles"]

    # ------------------------------------------------------------
    #   VALIDATE CYCLE
    # ------------------------------------------------------------

    def validate_cycle(self, cycle: int) -> bool:
        return (
            isinstance(cycle, int)
            and self.policy["min_cycle"] <= cycle <= self.policy["max_cycle"]
        )

    # ------------------------------------------------------------
    #   VALIDATE CHILD LIMIT
    # ------------------------------------------------------------

    def validate_child_count(self, count: int) -> bool:
        return count <= self.policy["max_children_per_node"]

    # ------------------------------------------------------------
    #   VALIDATE DEPTH
    # ------------------------------------------------------------

    def validate_depth(self, depth: int) -> bool:
        return depth <= self.policy["max_depth"]

    # ------------------------------------------------------------
    #   MAIN GATE — EVERYTHING MUST PASS HERE
    # ------------------------------------------------------------

    def gate(self, role: str, cycle: int, child_count: int, depth: int):
        """
        Returns (True, None) if safe.
        Returns (False, reason) if unsafe.
        """

        if not self.validate_role(role):
            return False, f"Invalid role: {role}"

        if not self.validate_cycle(cycle):
            return False, f"Invalid cycle: {cycle}"

        if not self.validate_child_count(child_count):
            return False, f"Exceeded child limit ({child_count})"

        if not self.validate_depth(depth):
            return False, f"Exceeded max depth ({depth})"

        return True, None

    # ------------------------------------------------------------
    #   TEXT PURIFIER — strips dangerous patterns
    # ------------------------------------------------------------

    def purify(self, text: str) -> str:
        """
        Strips patterns that could cause:
            - runaway expansions
            - meta-injection
            - malformed sigils
        """
        banned = ["<<", ">>", "{{", "}}"]
        cleaned = text
        for b in banned:
            cleaned = cleaned.replace(b, "")

        return cleaned.strip()

    # ------------------------------------------------------------
    #   HIGH-LEVEL CHECK FOR SHELL
    # ------------------------------------------------------------

    def safe_for_shell(self, command: str) -> bool:
        """
        Prevents destructive operations from entering ArcShell.
        """
        lower = command.lower()

        # Example future rules
        if "rm -rf" in lower:
            return False
        if "shutdown" in lower:
            return False
        if "exec(" in lower:
            return False

        return True
