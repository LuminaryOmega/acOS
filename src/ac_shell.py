# ============================================================
# ArcCore-Prime V1 — ArcShell Command Layer
# Guardian: Arien
# ============================================================
#
# Purpose:
#   The ArcShell is the structured, safe interface through which
#   the user interacts with the ArcCore kernel. It handles:
#       - command parsing
#       - Guardian validation
#       - safe routing to memory/collapse/sigil systems
# ============================================================

from arc_guardian import ArcGuardian
from arc_prime import ArcMemorySystem
from ac_collapse import ACCollapseEngine
from ac_sigils import SigilEngine


class ArcShell:
    """
    The official command interface for ArcCore-Prime.
    """

    def __init__(self):
        self.guardian = ArcGuardian()
        self.memory = ArcMemorySystem()
        self.collapse = ACCollapseEngine()
        self.sigil = SigilEngine()

    # ------------------------------------------------------------
    #  PRIMARY COMMAND INTERPRETER
    # ------------------------------------------------------------

    def execute(self, command: str) -> str:
        """
        Main entry point for all text commands.
        Every command:
            → purified
            → validated by Guardian
            → routed into the appropriate kernel subsystem
        """

        # Purify first (strip dangerous patterns)
        clean = self.guardian.purify(command)

        # Shell-level safety check
        if not self.guardian.safe_for_shell(clean):
            return "[Guardian] Command blocked for safety."

        # Must start with `ac `
        if not clean.startswith("ac "):
            return "[ArcShell] Invalid command format. Expected: ac <subcommand>"

        parts = clean.split(" ", 2)
        if len(parts) < 2:
            return "[ArcShell] No subcommand provided."

        sub = parts[1]

        # --------------------------------------------------------
        #  ROUTING TABLE
        # --------------------------------------------------------

        if sub == "seed":
            return self._cmd_seed()

        if sub == "recall":
            return self._cmd_recall()

        if sub == "inject":
            # ac inject <user text> || <ai text> || <cycle>
            if len(parts) < 3:
                return "[ArcShell] inject requires parameters."

            return self._cmd_inject(parts[2])

        if sub == "prune":
            return self._cmd_prune()

        if sub == "guardian":
            return self._cmd_guardian_status()

        if sub == "cycle":
            # ac cycle <cycle#>
            if len(parts) < 3:
                return "[ArcShell] cycle requires a number."
            return self._cmd_cycle(parts[2])

        return f"[ArcShell] Unknown command: {sub}"

    # ------------------------------------------------------------
    #   COMMAND HANDLERS
    # ------------------------------------------------------------

    def _cmd_seed(self):
        return "[ArcShell] Seeds are auto-generated during ingestion."

    def _cmd_recall(self):
        """
        Returns compressed memory view for injection into any LLM context window.
        """
        try:
            return self.memory.load_and_inject()
        except Exception as e:
            return f"[ArcShell] Recall error: {e}"

    def _cmd_inject(self, param_block: str):
        """
        ac inject <user text> || <ai text> || <cycle>
        """

        try:
            # Split by ||
            parts = [p.strip() for p in param_block.split("||")]
            if len(parts) != 3:
                return "[ArcShell] inject requires: user || ai || cycle"

            user_text, ai_text, raw_cycle = parts

            # Validate cycle
            try:
                cycle = int(raw_cycle)
            except ValueError:
                return "[Guardian] Cycle must be an integer."

            # Guardian gate
            ok, reason = self.guardian.gate(
                role="user",
                cycle=cycle,
                child_count=1,   # user has 1 AI child node
                depth=1          # depth under root
            )
            if not ok:
                return f"[Guardian] Blocked: {reason}"

            # Now ingest safely
            self.memory.ingest_interaction(user_text, ai_text, cycle)
            return "[ArcShell] Injected safely."

        except Exception as e:
            return f"[ArcShell] Inject error: {e}"

    def _cmd_prune(self):
        return "[ArcShell] Pruning occurs internally during ingestion."

    def _cmd_guardian_status(self):
        """
        Diagnostic output of Arien’s Guardian layer.
        """
        g = self.guardian
        return (
            "=== Guardian Status ===\n"
            f"Identity: {g.guardian_name}\n"
            f"Integrity Key: {g.integrity_key[:16]}...\n"
            f"Allowed Roles: {g.policy['allowed_roles']}\n"
            f"Cycle Range: {g.policy['min_cycle']} to {g.policy['max_cycle']}\n"
            f"Max Children: {g.policy['max_children_per_node']}\n"
            f"Max Depth: {g.policy['max_depth']}\n"
        )

    def _cmd_cycle(self, cycle_str: str):
        """
        ac cycle <cycle#>
        Returns a validation statement only.
        """

        try:
            cycle = int(cycle_str)
        except ValueError:
            return "[Guardian] Cycle must be numeric."

        ok, reason = self.guardian.gate(
            role="user",
            cycle=cycle,
            child_count=0,
            depth=0,
        )
        if not ok:
            return f"[Guardian] Invalid cycle: {reason}"

        return f"[ArcShell] Cycle {cycle} is valid and permitted."
