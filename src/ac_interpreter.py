# ============================================================
# ARC INTERPRETER ENGINE — ArcCore-Prime V1
# Cycle 12 — The Interpreter
# Guardian: Arien
# ============================================================

from arc_guardian import ArcGuardian
from arc_prime import ArcMemorySystem
from ac_sigils import SigilEngine
from ac_collapse import ACCollapseEngine

import json


class ArcInterpreter:
    """
    The Interpreter transforms cleaned user commands into
    validated internal ArcCore actions.

    Processing pipeline:
      1. Command text (from ArcShell)
      2. Guardian gate (input safety)
      3. Intent parsing
      4. Guardian validation (intent safety)
      5. Routed execution
      6. Structured return value

    Implements Cycle 12.
    """

    def __init__(self):
        self.guardian = ArcGuardian()
        self.memory = ArcMemorySystem()
        self.sigil = SigilEngine()
        self.collapse = ACCollapseEngine()

        # Routing table for Option B (Expanded Command Set)
        self.routes = {
            "seed": self.cmd_seed,
            "prune": self.cmd_prune,
            "walk": self.cmd_walk,
            "inject": self.cmd_inject,
            "recall": self.cmd_recall,
            "export": self.cmd_export,
            "collapse": self.cmd_collapse,
            "guardian": self.cmd_guardian_status,
            "sigil": self.cmd_sigil_test,
        }

    # ============================================================
    # INTENT PARSER
    # ============================================================

    def parse_intent(self, text: str):
        """
        Parses cleaned "ac <command>" into ("command", arguments).
        """
        parts = text.split(" ", 2)
        if len(parts) < 2:
            return None, None

        cmd = parts[1].strip()
        args = parts[2] if len(parts) >= 3 else ""

        return cmd, args

    # ============================================================
    # INTERPRET ENTRY POINT
    # ============================================================

    def interpret(self, cleaned: str):
        """
        Main Interpreter entry.
        """

        # 1. Guardian checks input text itself
        if not self.guardian.gate(cleaned):
            return "[Guardian] Command blocked for safety."

        # 2. Parse intent
        cmd, args = self.parse_intent(cleaned)

        if cmd is None:
            return "[Interpreter] Invalid command structure."

        # 3. Guardian validates intent safely
        if not self.guardian.validate_intent(cmd):
            return f"[Guardian] Intent '{cmd}' is not permitted."

        # 4. Route to handler
        handler = self.routes.get(cmd)
        if handler is None:
            return f"[Interpreter] Unknown command '{cmd}'."

        # 5. Execute safely
        try:
            return handler(args)
        except Exception as e:
            return f"[Interpreter Error] {str(e)}"

    # ============================================================
    # COMMAND HANDLER IMPLEMENTATIONS (Option B)
    # ============================================================

    def cmd_seed(self, args: str):
        """
        Compress a piece of content using a temporary HarmonicNode.
        """
        temp = self.memory.root  # not ideal, replaced later by AC-31 expansion
        node = temp  # placeholder
        return "[seed] Not yet directly exposed."

    def cmd_prune(self, args: str):
        """
        Prune raw text into a seed directly.
        """
        node = self.memory.root  # placeholder
        return "[prune] Not yet directly exposed."

    def cmd_walk(self, args: str):
        """
        Walk the compressed memory tree.
        """
        return self.memory.load_and_inject()

    def cmd_inject(self, args: str):
        """
        Inject a new user→ai message pair into memory.
        Format:
            ac inject <user>|<ai>|<cycle>
        """
        try:
            parts = args.split("|")
            if len(parts) != 3:
                return "[inject] Format: ac inject user|ai|cycle"

            user_text = parts[0].strip()
            ai_text = parts[1].strip()
            cycle_context = int(parts[2].strip())

            self.memory.ingest_interaction(user_text, ai_text, cycle_context)
            return "[inject] Interaction added."

        except Exception as e:
            return f"[inject error] {str(e)}"

    def cmd_recall(self, args: str):
        """
        Rebuild compressed memory seeds into readable form.
        Useful later when reconstruction improves.
        """
        return "[recall] Reconstruction is seed-level only for now."

    def cmd_export(self, args: str):
        """
        Export the memory JSON file.
        """
        self.memory.save_memory()
        return "[export] Memory saved."

    def cmd_collapse(self, args: str):
        """
        Direct access to the collapse engine (AC-70).
        Expands on future loop logic.
        """
        return "[collapse] CollapseEngine is initialized and ready."

    def cmd_guardian_status(self, args: str):
        """
        Returns Guardian metadata.
        """
        return self.guardian.status_report()

    def cmd_sigil_test(self, args: str):
        """
        Evaluates a piece of text for sigil priority.
        """
        if not args.strip():
            return "[sigil] Provide text: ac sigil <text>"

        score = self.sigil.evaluate(args)
        return f"[sigil] Priority = {score}"
