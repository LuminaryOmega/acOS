# ============================================================
# ArcCore-Prime V1 — ArcShell Command Layer
# Implements Cycle 5 (The Arc), Cycle 12 (The Interpreter)
# and Cycle 28 (Operational Flow)
#
# The ArcShell is the "voice" of ArcCore — a safe, structured
# interface that lets the user interact with the AI kernel.
#
# Guardian: Arien
# ============================================================

from arc_guardian import ArcGuardian
from arc_prime import ArcMemorySystem

class ArcShell:
    """
    ArcShell provides:
    - command parsing
    - safe execution through the Guardian
    - access to memory functions
    - structured outputs

    It is the official interface for ArcCore-Prime.
    """

    def __init__(self):
        self.guardian = ArcGuardian()
        self.memory = ArcMemorySystem()

    # -------------------------------------------------------------
    # PARSE COMMAND
    # -------------------------------------------------------------

    def execute(self, command: str):
        """
        Primary command interpreter.
        All commands pass through Arien (Guardian).
        """
        # Guardian gate
        if not self.guardian.gate(command):
            return "[Guardian] Command blocked for safety."

        # Purify the command text
        clean = self.guardian.purify(command).strip()

        # ---------------------------------------------
        # COMMAND ROUTES
        # ---------------------------------------------

        if clean.startswith("ac "):
            parts = clean.split(" ", 2)
            if len(parts) < 2:
                return "[ArcShell] Invalid AC command."

            sub = parts[1]

            # ──────────────────────────────────────────
            # Memory-related commands
            # ──────────────────────────────────────────
            if sub == "seed":
                return self._cmd_seed()

            if sub == "recall":
                return self._cmd_recall()

            if sub == "inject":
                return self._cmd_inject()

            if sub == "prune":
                return self._cmd_prune()

            # ──────────────────────────────────────────
            # Guardian commands
            # ──────────────────────────────────────────
            if sub == "guardian":
                return self._cmd_guardian_status()

            # ──────────────────────────────────────────
            # Cycle introspection
            # ──────────────────────────────────────────
            if sub == "cycle" and len(parts) == 3:
                return self._cmd_cycle(parts[2])

            return "[ArcShell] Unknown AC command."

        return "[ArcShell] Unrecognized instruction."

    # -------------------------------------------------------------
    # COMMAND IMPLEMENTATIONS
    # -------------------------------------------------------------

    def _cmd_seed(self):
        return "[ArcShell] Structural seed generated."

    def _cmd_recall(self):
        return "[ArcShell] Recalling recent memory..."

    def _cmd_inject(self):
        context = self.memory.load_and_inject()
        return f"[ArcShell] Injected Context:\n{context}"

    def _cmd_prune(self):
        return "[ArcShell] Memory pruned and compressed."

    def _cmd_guardian_status(self):
        g = self.guardian.guardian_signature()
        return (
            "[ArcGuardian Status]\n"
            f"Guardian: {g['guardian']}\n"
            f"Integrity Key: {g['key']}\n"
            f"Boot: {g['boot']}\n"
        )

    def _cmd_cycle(self, cycle_number):
        return f"[ArcShell] Cycle {cycle_number} acknowledged."
